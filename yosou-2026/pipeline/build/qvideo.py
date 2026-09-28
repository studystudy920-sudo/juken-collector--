#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1問=1動画（読み上げ版）を作る.

各問のスライド4枚（①問題 ②図解 ③解答 ④実務）を画像化し、問題データから
ナレーション原稿を作って edge-tts（ja-JP-NanamiNeural）で音声化、ffmpeg で MP4 にする。
問題スライドの後には考える間（--think 秒）を入れる。

使い方:
  python3 build/qvideo.py --ids 9 24           # 指定問題
  python3 build/qvideo.py --sc 1-1             # サブカテゴリ単位
  python3 build/qvideo.py --all                # 全750問
  オプション: --out DIR  --voice ja-JP-NanamiNeural  --rate +0%  --think 4  --jobs 6
出力: <OUT>/<sc>/Q<id4桁>_<タグ>.mp4 と、同名の .txt（読み上げ原稿）
"""
import os, re, sys, json, glob, asyncio, argparse, subprocess, shutil, ssl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK_DIR = os.path.join(ROOT, "data", "decks_official")
BUILD = os.path.join(ROOT, "build", "build_biz30.py")
CACHE = os.path.join(ROOT, ".render")
os.environ.setdefault("HOME", CACHE)
INTRO, PER = 7, 4                      # イントロ7枚、1問4枚
W, H = 1440, 1080                      # デッキは 4:3

# ---------- 原稿 ----------
ROMAN = {"I":1,"II":2,"III":3,"IV":4,"V":5,"VI":6,"VII":7,"VIII":8,"IX":9,"X":10}

def clean(s):
    s = str(s or "")
    s = re.sub(r"【[^】]*】", "", s)
    s = re.sub(r"[💡📌🧠⚠️✅❌☁🌧☂※]", "", s)
    s = re.sub(r"(?<![A-Za-z])R\.(\d+)", r"勧告\1", s)
    s = re.sub(r"(?<![A-Za-z])(VIII|VII|VI|IV|IX|III|II|I|V|X)-(\d+)", lambda m: f"{ROMAN[m.group(1)]}の{m.group(2)}", s)
    s = re.sub(r"(?<=[A-Z])-(?=[A-Z])", "", s)
    s = re.sub(r"(?<=[ァ-ヶー])・(?=[ァ-ヶー])", "", s)       # マネー・ローンダリング
    s = s.replace("→", "、次に").replace("＝", "は").replace("⇒", "、つまり")
    s = re.sub(r"[『』「」“”\"]", "、", s)
    s = re.sub(r"[（(]", "、", s); s = re.sub(r"[）)]", "、", s)
    s = re.sub(r"[／/・]", "、", s)
    s = re.sub(r"^[①-⑳]\s*", "", s)
    s = re.sub(r"、\s*、+", "、", s); s = re.sub(r"、([。？！、])", r"\1", s)
    s = re.sub(r"^、|、$", "", s)
    s = re.sub(r"\s+", " ", s).strip(" 、")
    return s

def label(s):
    return clean(re.sub(r"[（(][^）)]*[）)]", "", str(s or "")))

def sent(s):
    s = clean(s)
    return s if not s or s[-1] in "。？！" else s + "。"

def narration(q, deck_topic):
    L = "アイウエオ"
    letters = q.get("answer_letters") or []
    # ① 問題
    p1 = [f"問題です。テーマは、{clean(q.get('tag',''))}。", sent(q.get("q_jp"))]
    for i, c in enumerate(q.get("choices_jp") or []):
        p1.append(f"{L[i]}。{sent(c)}")
    p1.append("少し考えてみましょう。")
    # ② 図解
    d = q.get("diagram") or {}
    p2 = [f"図解です。{sent(d.get('title',''))}"]
    nodes = [n for layer in d.get("layers", []) for n in layer]
    lab = {n.get("id"): label(n.get("label")) for n in nodes}
    if nodes:
        p2.append("登場するのは、" + "、".join(lab[n["id"]] for n in nodes[:8]) + "です。")
    for e in (d.get("edges") or [])[:4]:
        if e.get("label"):
            p2.append(f"{lab.get(e.get('from'),'')}から{lab.get(e.get('to'),'')}へ、{sent(e['label'])}")
    if d.get("caption"):
        p2.append("ポイントは、" + sent(d["caption"]))
    # ③ 解答
    p3 = [f"正解は、{'と'.join(letters)}。{sent(q.get('answer_jp'))}", sent(q.get("explain_jp"))]
    wrong = [o for o in (q.get("options") or []) if not o.get("correct")]
    if wrong:
        p3.append("ほかの選択肢も確認します。")
        for o in wrong:
            p3.append(f"{o.get('letter','')}は、{sent(o.get('reason'))}")
    # ④ 実務
    p4 = ["実務と試験のポイントです。"]
    if q.get("trap"):     p4.append("ひっかけに注意。" + sent(q["trap"]))
    if q.get("mnemonic"): p4.append("覚え方。" + sent(q["mnemonic"]))
    for b in (q.get("bank_notes") or [])[:3]:
        p4.append(sent(b))
    if q.get("case"):     p4.append(sent(q["case"]))
    p4.append("以上です。")
    return [" ".join(x for x in p if x) for p in (p1, p2, p3, p4)]

# ---------- スライド画像 ----------
def deck_pdf(f, d):
    base = os.path.splitext(os.path.basename(f))[0]
    pptx, pdf = os.path.join(CACHE, base + ".pptx"), os.path.join(CACHE, base + ".pdf")
    if not os.path.exists(pptx):
        subprocess.run([sys.executable, BUILD, f, pptx, d.get("topic_jp", "")], check=True, capture_output=True)
    if not os.path.exists(pdf):
        subprocess.run(["soffice", "--headless", "--norestore", "--nologo", f"-env:UserInstallation=file://{CACHE}/lo",
                        "--convert-to", "pdf", "--outdir", CACHE, pptx], capture_output=True)
    return pdf

def slide_pngs(pdf, idx, tmp):
    import fitz
    doc = fitz.open(pdf); out = []
    for k in range(4):
        pg = doc[INTRO + PER * idx + k]
        z = W / pg.rect.width
        p = os.path.join(tmp, f"s{k}.png"); pg.get_pixmap(matrix=fitz.Matrix(z, z)).save(p); out.append(p)
    return out

# ---------- 音声 ----------
def tts_ssl():
    ca = "/root/.ccr/ca-bundle.crt"         # クラウド環境のプロキシ証明書
    if os.path.exists(ca):
        import edge_tts.communicate as c
        c._SSL_CTX = ssl.create_default_context(cafile=ca)

async def tts(text, path, voice, rate, sem):
    import edge_tts
    async with sem:
        for t in range(4):
            try:
                await edge_tts.Communicate(text, voice, rate=rate).save(path)
                if os.path.getsize(path) > 0: return
            except Exception as e:
                err = e
            await asyncio.sleep(2 * (t + 1))
        raise RuntimeError(f"TTS失敗: {path}: {err}")

# ---------- 動画 ----------
def ff(*a):
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], capture_output=True, text=True)
    if r.returncode: raise RuntimeError(r.stderr[-400:])

def make_video(pngs, mp3s, pads, out, tmp):
    segs = []
    for i, (img, mp3, pad) in enumerate(zip(pngs, mp3s, pads)):
        seg = os.path.join(tmp, f"seg{i}.mp4")
        ff("-loop", "1", "-framerate", "1", "-i", img, "-i", mp3,
           "-af", f"apad=pad_dur={pad}", "-c:v", "libx264", "-tune", "stillimage", "-crf", "28",
           "-vf", f"scale={W}:{H}", "-pix_fmt", "yuv420p", "-r", "1", "-c:a", "aac", "-b:a", "48k", "-ar", "24000", "-shortest", seg)
        segs.append(seg)
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", out)

def safe(s):
    return re.sub(r'[\\/:*?"<>|#^\[\]]', "", str(s)).strip()[:40]

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", nargs="*"); ap.add_argument("--sc", nargs="*"); ap.add_argument("--all", action="store_true")
    ap.add_argument("--out", default=os.path.join(ROOT, "output", "SC_1問1動画"))
    ap.add_argument("--voice", default="ja-JP-NanamiNeural"); ap.add_argument("--rate", default="-8%")
    ap.add_argument("--think", type=float, default=6.0); ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    tts_ssl(); os.makedirs(CACHE, exist_ok=True)
    targets = []
    for f in sorted(glob.glob(os.path.join(DECK_DIR, "dt_*.json"))):
        sc = re.search(r"dt_(\d+)_", f).group(1); d = json.load(open(f, encoding="utf-8"))
        for i, q in enumerate(d["questions"]):
            if a.all or (a.sc and sc in a.sc) or (a.ids and str(q["id"]) in a.ids):
                targets.append((f, sc, d, i, q))
    sem = asyncio.Semaphore(a.jobs); done = 0
    for f, sc, d, idx, q in targets:
        qid = int(q["id"]); odir = os.path.join(a.out, sc); os.makedirs(odir, exist_ok=True)
        name = f"Q{qid:04d}_{safe(q.get('tag',''))}"
        out = os.path.join(odir, name + ".mp4")
        if os.path.exists(out): done += 1; continue
        tmp = os.path.join(CACHE, "qv", str(qid)); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
        texts = narration(q, d.get("topic_jp", ""))
        open(os.path.join(odir, name + ".txt"), "w", encoding="utf-8").write(
            "\n\n".join(f"[{t}]\n{x}" for t, x in zip(["問題", "図解", "解答", "実務"], texts)))
        mp3s = [os.path.join(tmp, f"n{k}.mp3") for k in range(4)]
        await asyncio.gather(*(tts(t, m, a.voice, a.rate, sem) for t, m in zip(texts, mp3s)))
        pngs = slide_pngs(deck_pdf(f, d), idx, tmp)
        make_video(pngs, mp3s, [a.think, 1.3, 1.3, 1.5], out, tmp)
        shutil.rmtree(tmp, ignore_errors=True); done += 1
        print(f"[{done}/{len(targets)}] {out}", flush=True)

asyncio.run(main())
