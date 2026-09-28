#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""動画＋Claude対話の学習ページ（Artifact 用）をサブカテゴリ単位で生成する.

  python3 build/qstudio.py 1-1
出力: output/qstudio_<sc>/index.html と v/Q<id4桁>.mp4（qvideo.py の出力をコピー）
公開: Artifact に index.html を、v/*.mp4 を files として（64MB/回 の上限で分割）公開する。
ページは capabilities {sample:{}, db:{}} を使う（Claude への質問・得意/苦手の記録）。
"""
import os, sys, re, json, glob, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK_DIR = os.path.join(ROOT, "data", "decks_official")
VID_DIR = os.path.join(ROOT, "output", "SC_1問1動画")
TEMPLATE = os.path.join(ROOT, "build", "qstudio_template.html")

def main():
    sc = sys.argv[1] if len(sys.argv) > 1 else "1-1"
    out = os.path.join(ROOT, "output", f"qstudio_{sc}")
    os.makedirs(os.path.join(out, "v"), exist_ok=True)
    mlist = json.load(open(os.path.join(ROOT, "data", "manifest.json"), encoding="utf-8"))
    man = {e["json"]: e for e in mlist}
    sc_name = next((e["subcat_folder"].split("_", 1)[1] for e in mlist if e["subcat"] == sc), "")
    files = sorted(glob.glob(os.path.join(DECK_DIR, f"dt_{sc}_*.json")),
                   key=lambda f: int(re.search(r"_(\d+)\.json$", f).group(1)))
    qs, missing = [], []
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        theme = re.sub(r"^.*?：", "", d.get("topic_jp", ""))
        label = man.get(os.path.basename(f), {}).get("label", "")
        for q in d["questions"]:
            qid = int(q["id"])
            src = glob.glob(os.path.join(VID_DIR, sc, f"Q{qid:04d}_*.mp4"))
            if src:
                shutil.copy(src[0], os.path.join(out, "v", f"Q{qid:04d}.mp4"))
            else:
                missing.append(qid)
            qs.append({
                "id": qid, "theme": theme, "deck": label, "tag": q.get("tag", ""),
                "imp": q.get("importance", ""), "q": q.get("q_jp", ""), "choices": q.get("choices_jp", []),
                "ans": q.get("answer_letters", []), "ansText": q.get("answer_jp", ""),
                "explain": q.get("explain_jp", ""), "trap": q.get("trap", ""),
                "mnemonic": q.get("mnemonic", ""), "hint": q.get("hint_jp", ""),
                "reasons": [{"l": o.get("letter"), "ok": bool(o.get("correct")), "r": o.get("reason", "")}
                            for o in (q.get("options") or [])],
                "bank": (q.get("bank_notes") or [])[:4], "case": q.get("case", ""),
                "related": q.get("related", ""), "video": f"v/Q{qid:04d}.mp4" if src else "",
            })
    data = {"sc": sc, "scName": sc_name, "questions": qs}
    html = open(TEMPLATE, encoding="utf-8").read()
    html = html.replace("__SC__", sc).replace("__SCNAME__", sc_name)
    html = html.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
    size = sum(os.path.getsize(p) for p in glob.glob(os.path.join(out, "v", "*.mp4")))
    print(f"{sc}: {len(qs)}問 / 動画 {len(qs)-len(missing)}本 {size/1048576:.1f}MB -> {out}")
    if missing:
        print("動画なし:", missing)

main()
