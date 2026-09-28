#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CAMS 750問 -> Obsidian Vault（Markdownノート）を生成する.

- 1問 = 1ノート。ドメイン/サブカテゴリのフォルダに配置。
- YAML frontmatter に id/domain/subcat/theme/importance/answer/status/tags。
  status は data/study_progress.json（得意/苦手記録）と同期。
- 本文: 問題 → ? → 正解（空行なしの1ブロック＝SRカード） → 図解 → 解説 → 覚え方/ひっかけ → 空雨傘
        → 選択肢別正誤 → 邦銀メモ → 規制根拠(表) → 関連リンク。
  ⇒ Spaced Repetition プラグインのカード。タグ CAMS/<sc> でサブカテゴリ別デッキになる。
- 各サブカテゴリに MOC(目次)、Vault直下に README を生成。
使い方: python3 build/obsidian.py [--out DIR] [--sc 1-1 ...]
"""
import os, sys, json, glob, re, argparse, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK_DIR = os.path.join(ROOT, "data", "decks_official")
PROG = os.path.join(ROOT, "data", "study_progress.json")

DOMAIN_NAME = {"1":"暗号・認証・PKI","2":"NW・クラウド・ゼロトラスト","3":"Web/アプリ脆弱性","4":"AIセキュリティ・LLM","5":"攻撃手法・IR","6":"マネジメント・法規","7":"AI駆動型攻撃"}
STATUS_JP = {"strong":"得意","weak":"苦手","learning":"学習中","unseen":"未学習"}

def load_prog():
    if os.path.exists(PROG):
        try: return json.load(open(PROG, encoding="utf-8"))
        except Exception: return {}
    return {}

def status_of(rec):
    if not rec or rec.get("correct",0)+rec.get("wrong",0)==0: return "unseen"
    s=rec.get("streak",0)
    if s<=-1: return "weak"
    if s>=2: return "strong"
    return "learning"

def safe(s):
    s=re.sub(r'[\\/:*?"<>|#^\[\]]', "", str(s))
    return s.strip().replace("\n"," ")[:60]

def bullets(items, prefix="- "):
    if not items: return ""
    if isinstance(items,str): items=[items]
    return "\n".join(prefix+str(x) for x in items)

def note_md(q, deck, prog, images=False, with_en=False):
    qid=str(q.get("id")); sc=deck["_sc"]; dom=sc.split("-")[0]
    st=status_of(prog.get(qid))
    letters=q.get("answer_letters",[]) or []
    ans_set="".join(letters)
    choices=q.get("choices_jp",[]) or []
    labels="アイウエオ"
    # frontmatter
    fm=["---",
        f"id: {qid}",
        f'domain: {dom}',
        f'subcat: "{sc}"',
        f'theme: "{safe(deck.get("topic_jp",""))}"',
        f'tag: "{safe(q.get("tag",""))}"',
        f'importance: "{q.get("importance","")}"',
        f'freq: {q.get("freq","")}',
        f'answer: "{ans_set}"',
        f'status: {STATUS_JP[st]}',
        f'tags: [SC/{sc}, domain{dom}, sc{sc.replace("-","_")}]',
        "---",""]
    L=fm
    L.append(f"# Q{qid} · {q.get('tag','')}")
    L.append("")
    L.append(f"サブカテゴリ **{sc} {DOMAIN_NAME[dom]}** ／ テーマ: {deck.get('topic_jp','')} ／ 重要度 {q.get('importance','')}")
    L.append("")
    # Spaced Repetition カード: 問題→?→正解 を空行なしで連続させる（空行でカードが切れる）
    L.append("## 問題")
    L.append("")
    n=len(letters)
    L.append(q.get("q_jp","").replace("\n"," ") + (f"（{n}つ選択）" if n>1 else ""))
    for i,c in enumerate(choices):
        L.append(f"{labels[i]}. {c}")
    L.append("?")
    L.append(f"✅ **正解: {ans_set}** — {q.get('answer_jp','')}")
    L.append("")
    # diagram slide embed
    if images:
        L.append("## 図解")
        L.append(f"![[Q{int(qid):04d}_diagram.png]]"); L.append("")
    if q.get("explain_jp"):
        L.append("## 解説")
        L.append(q["explain_jp"]); L.append("")
    # English (collapsible)
    if with_en and (q.get("q_en") or q.get("explain_en")):
        L.append("> [!info]- English")
        if q.get("q_en"): L.append("> **Q.** "+q["q_en"].replace("\n"," "))
        for i,c in enumerate(q.get("choices_en",[]) or []):
            L.append(f"> - {labels[i]}. {c}")
        if q.get("explain_en"):
            L.append(">")
            L.append("> **Explanation.** "+q["explain_en"].replace("\n"," "))
        L.append("")
    if q.get("mnemonic") or q.get("hint_jp"):
        L.append("> [!tip] 覚え方")
        if q.get("hint_jp"): L.append("> "+q["hint_jp"])
        if q.get("mnemonic"): L.append("> "+q["mnemonic"])
        L.append("")
    if q.get("trap"):
        L.append("> [!warning] ひっかけ")
        L.append("> "+q["trap"]); L.append("")
    # sky-rain-umbrella
    if q.get("sky") or q.get("rain") or q.get("umbrella"):
        L.append("## 空-雨-傘")
        if q.get("sky"): L.append("**☁ 空（事実）**\n"+bullets(q["sky"]))
        if q.get("rain"): L.append("**🌧 雨（解釈）**\n"+bullets(q["rain"]))
        if q.get("umbrella"): L.append("**☂ 傘（対応）**\n"+bullets(q["umbrella"]))
        L.append("")
    # option-by-option
    opts=q.get("options") or []
    if opts:
        L.append("## 選択肢別 正誤")
        L.append("| | 正誤 | 理由 |")
        L.append("|---|---|---|")
        for o in opts:
            mk="✅" if o.get("correct") else "❌"
            L.append(f"| {o.get('letter','')} | {mk} | {str(o.get('reason','')).replace(chr(10),' ')} |")
        L.append("")
    if q.get("bank_notes"):
        L.append("## 実務メモ")
        L.append(bullets(q["bank_notes"])); L.append("")
    if q.get("reg_detail"):
        L.append("## 規制根拠")
        L.append("| 規制 | ポイント |")
        L.append("|---|---|")
        for r in q["reg_detail"]:
            L.append(f"| {r.get('reg','')} | {str(r.get('point','')).replace(chr(10),' ')} |")
        L.append("")
    elif q.get("related_regs"):
        L.append("## 規制根拠")
        L.append(bullets(q["related_regs"])); L.append("")
    if q.get("case"):
        L.append("> [!example] 出題傾向\n> "+q["case"]); L.append("")
    if q.get("related"):
        L.append(f"**関連**: {q['related']}"); L.append("")
    L.append("---")
    L.append(f"#domain{dom} #sc{sc.replace('-','_')} #{STATUS_JP[st]}")
    return "\n".join(L)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT,"output","SC_Obsidian_Vault"))
    ap.add_argument("--sc", nargs="*")
    ap.add_argument("--images", action="store_true", help="図解スライドPNGを埋め込む")
    ap.add_argument("--en", action="store_true", help="英語(q_en/explain_en)を併記")
    ap.add_argument("--img-src", default=os.path.join(ROOT,".render","attachments"),
                    help="Q<id>_diagram.png の置き場（--images時にVaultへコピー）")
    a=ap.parse_args()
    prog=load_prog()
    import shutil
    att=os.path.join(a.out,"_attachments")
    if a.images: os.makedirs(att, exist_ok=True)
    decks=[]
    for f in sorted(glob.glob(os.path.join(DECK_DIR,"dt_*.json"))):
        sc=re.search(r"dt_(\d+)_",f).group(1)
        if a.sc and sc not in a.sc: continue
        d=json.load(open(f,encoding="utf-8")); d["_sc"]=sc; decks.append(d)
    total=0; by_sc={}; nimg=0
    for d in decks:
        sc=d["_sc"]; dom=sc.split("-")[0]
        folder=os.path.join(a.out, f"{dom}_{DOMAIN_NAME[dom]}", f"{sc}")
        os.makedirs(folder, exist_ok=True)
        by_sc.setdefault(sc, [])
        for q in d.get("questions",[]):
            qid=str(q.get("id"))
            fn=f"Q{int(qid):04d} {safe(q.get('tag','') or 'question')}.md"
            open(os.path.join(folder,fn),"w",encoding="utf-8").write(
                note_md(q,d,prog,images=a.images,with_en=a.en))
            if a.images:
                src=os.path.join(a.img_src, f"Q{int(qid):04d}_diagram.png")
                if os.path.exists(src):
                    shutil.copy(src, os.path.join(att, f"Q{int(qid):04d}_diagram.png")); nimg+=1
            by_sc[sc].append((qid, q.get("tag",""), d.get("topic_jp","")))
            total+=1
    # MOC per subcat
    for sc,items in by_sc.items():
        dom=sc.split("-")[0]
        folder=os.path.join(a.out, f"{dom}_{DOMAIN_NAME[dom]}", f"{sc}")
        moc=[f"# {sc} {DOMAIN_NAME[dom]} — 目次（{len(items)}問）",""]
        moc.append("```dataview")
        moc.append(f'table importance as 重要度, status as 状態')
        moc.append(f'from #sc{sc.replace("-","_")}')
        moc.append('sort status asc')
        moc.append("```")
        moc.append("")
        for qid,tag,topic in items:
            moc.append(f"- [[Q{int(qid):04d} {safe(tag)}|Q{qid}]] — {tag}")
        open(os.path.join(folder,f"_MOC {sc}.md"),"w",encoding="utf-8").write("\n".join(moc))
    # README
    rd=["# SC予想 Obsidian Vault","",
        f"生成: {datetime.date.today().isoformat()} ／ {total}問",""
        ,"## 使い方",
        "- フォルダはドメイン→サブカテゴリの順。各 `_MOC` が目次。",
        "- 各ノートの「問題→?→正解」が **Spaced Repetition** のカード（デッキ SC → 分野別）。",
        "- frontmatter の `status`（得意/苦手/学習中/未学習）は学習ツールと同期。",
        "- Dataview で苦手だけ抽出可能:",
        "",
        "```dataview","table subcat, importance, status","from #SC","where status = \"苦手\"","```",""]
    open(os.path.join(a.out,"README.md"),"w",encoding="utf-8").write("\n".join(rd))
    print(f"生成 {total}問 -> {a.out}" + (f" / 図解画像 {nimg}枚" if a.images else ""))

main()
