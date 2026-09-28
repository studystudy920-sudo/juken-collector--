#!/usr/bin/env python3
# CAMSスクリプト群を SC(情報処理安全確保支援士) 向けに一括適合するパッチ
import re, io, os
B = "/home/user/juken-collector--/yosou-2026/pipeline/build"

def patch(fn, repls, count_check=True):
    p = os.path.join(B, fn)
    s = open(p, encoding="utf-8").read()
    for old, new in repls:
        if old not in s:
            print(f"  !! NOT FOUND in {fn}: {old[:50]!r}")
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8").write(s)
    print(f"patched {fn}")

# ---------- build_biz30.py ----------
bb = os.path.join(B, "build_biz30.py")
s = open(bb, encoding="utf-8").read()

s = s.replace('HEAD="Yu Gothic"; BODY="Yu Gothic"; JPF="Yu Gothic"',
              'HEAD="IPAPGothic"; BODY="IPAPGothic"; JPF="IPAPGothic"')
s = s.replace('para(f,"CAMS EXAM PREP  —  "+LABEL+"   |   AML/CFT",8.5,GREY,first=True)',
              'para(f,"SC EXAM PREP  —  "+LABEL+"   |   情報処理安全確保支援士",8.5,GREY,first=True)')
s = s.replace('para(f,"CAMS 試験対策"+(("  "+DLABEL) if DLABEL else ""),26,DARK,bold=True,font=HEAD,first=True)',
              'para(f,"SC 予想演習"+(("  "+DLABEL) if DLABEL else ""),26,DARK,bold=True,font=HEAD,first=True)')
s = s.replace('para(f3,"収録：概念6枚（学習マップ／関係図／比較表／用語集／規制マトリクス／試験のコツ）＋ 各問3枚",11,GREY,first=True)',
              'para(f3,"収録：概念6枚（学習マップ／中核構造図／比較表／用語集／規格マトリクス／試験のコツ）＋ 各問4枚",11,GREY,first=True)')
# glossary subtitle
s = s.replace('header(s,"③","基礎概念 — 必須用語集","PTA・コルレスを解く8用語",TEAL,"CONCEPT")',
              'header(s,"③","基礎概念 — 必須用語集",d["topic_jp"]+" の頻出用語",TEAL,"CONCEPT")')
# comparison subtitle + header cells
s = s.replace('header(s,"②","基礎概念 — 混同概念 比較表","正常・低リスク vs 疑わしい・高リスク",TEAL,"CONCEPT")',
              'header(s,"②","基礎概念 — 混同しやすい概念 比較表","正しい・安全 と 誤り・危険 の対比",TEAL,"CONCEPT")')
s = s.replace('data=[["対象概念","🟢 正常・低リスク",("🔴 疑わしい・高リスク（検知の核心）",WHITE,True)]]',
              'data=[["対象概念","🟢 正しい・安全",("🔴 誤り・危険（要注意）",WHITE,True)]]')
# reg matrix subtitle + callout
s = s.replace('header(s,"④","基礎概念 — 規制マトリクス","コルレス／PTA に関わる主要規制",TEAL,"CONCEPT")',
              'header(s,"④","基礎概念 — 規格・法令マトリクス",d["topic_jp"]+" に関わる主要な規格・法令",TEAL,"CONCEPT")')
s = s.replace('''callout(s,0.5,7.15,12.3,1.05,"💡","各規制は独立せず連動する。",
        "例）越境コルレスは FATF R.13 がEDDを要求し、米国拠点は PATRIOT Act §312/313、本邦は犯収法・監督指針III-3 が同時に発動する。",AMBER,LAMBER)''',
              'callout(s,0.5,7.15,12.3,1.05,"💡","規格・法令は独立せず連動する。",d["shared"].get("map_summary",""),AMBER,LAMBER)')
# 実務 slide header + left panel title
s = s.replace('s=slide(); header(s,"📋",f"実務・規制 Q{q[\'no\']}","邦銀視点メモ・規制論点・実例・ひっかけ",AMBER,f"Q{q[\'no\']}/5")',
              's=slide(); header(s,"📋",f"実務・規格 Q{q[\'no\']}","実務メモ・規格論点・実例・ひっかけ",AMBER,f"Q{q[\'no\']}/5")')
s = s.replace('para(hf,"📝 邦銀視点 実務チェックポイント",12,NAVY2,bold=True,first=True)',
              'para(hf,"📝 実務チェックポイント",12,NAVY2,bold=True,first=True)')

# ----- SLIDE 3: replace hardcoded コルレス/PTA block with concept_diagram-driven -----
start = s.index('# ===================== SLIDE 3:')
end = s.index('# ===================== SLIDE 4:')
new_slide3 = '''# ===================== SLIDE 3: CONCEPT1 — 中核構造図 (JSON) =====================
s=slide(); header(s,"①","基礎概念 — 中核構造図",d["topic_jp"]+" の全体構造と関係",TEAL,"CONCEPT")
_cd=d["shared"].get("concept_diagram")
if not _cd:
    _mn2=[str(x) for x in (d["shared"].get("map_nodes") or []) if str(x).strip()][:5]
    _cd={"title":None,
         "layers":[[{"id":f"m{k}","label":lb}] for k,lb in enumerate(_mn2)],
         "edges":[{"from":f"m{k}","to":f"m{k+1}"} for k in range(len(_mn2)-1)],
         "caption":d["shared"].get("map_summary")}
diagram(s,0.5,1.2,12.35,7.3,_cd,title=bool(_cd.get("title")),panel=True,iconk=1.25)
footer(s,3)

'''
s = s[:start] + new_slide3 + s[end:]

open(bb, "w", encoding="utf-8").write(s)
print("patched build_biz30.py (incl. slide3 rewrite)")

# ---------- qvideo.py ----------
patch("qvideo.py", [
    ('    L = "ABCDEFG"', '    L = "アイウエオ"'),
    ('sc = re.search(r"dt_(\\d+-\\d+)_", f).group(1)', 'sc = re.search(r"dt_(\\d+)_", f).group(1)'),
    ('default=os.path.join(ROOT, "output", "CAMS_1問1動画")', 'default=os.path.join(ROOT, "output", "SC_1問1動画")'),
])

# ---------- render_all.py ----------
patch("render_all.py", [
    ('sc=re.search(r"dt_(\\d+-\\d+)_",f).group(1)', 'sc=re.search(r"dt_(\\d+)_",f).group(1)'),
])

# ---------- obsidian.py ----------
patch("obsidian.py", [
    ('DOMAIN_NAME = {"1":"リスクと手法","2":"枠組み・規制","3":"プログラム構築","4":"ツール・技術"}',
     'DOMAIN_NAME = {"1":"暗号・認証・PKI","2":"NW・クラウド・ゼロトラスト","3":"Web/アプリ脆弱性","4":"AIセキュリティ・LLM","5":"攻撃手法・IR","6":"マネジメント・法規","7":"AI駆動型攻撃"}'),
    ('    labels="ABCDEFG"', '    labels="アイウエオ"'),
    ('sc=re.search(r"dt_(\\d+-\\d+)_",f).group(1)', 'sc=re.search(r"dt_(\\d+)_",f).group(1)'),
    ("f'tags: [CAMS/{sc}, domain{dom}, sc{sc.replace(\"-\",\"_\")}]',",
     "f'tags: [SC/{sc}, domain{dom}, sc{sc.replace(\"-\",\"_\")}]',"),
    ('        L.append("## 邦銀メモ")', '        L.append("## 実務メモ")'),
    ('ap.add_argument("--out", default=os.path.join(ROOT,"output","CAMS_Obsidian_Vault"))',
     'ap.add_argument("--out", default=os.path.join(ROOT,"output","SC_Obsidian_Vault"))'),
    ('rd=["# CAMS 750問 Obsidian Vault","",', 'rd=["# SC予想 Obsidian Vault","",'),
    ('"- 各ノートの「問題→?→正解」が **Spaced Repetition** のカード（デッキ CAMS → 1-1 … 4-4）。",',
     '"- 各ノートの「問題→?→正解」が **Spaced Repetition** のカード（デッキ SC → 分野別）。",'),
    ('"```dataview","table subcat, importance, status","from #CAMS","where status = \\"苦手\\"","```",""]',
     '"```dataview","table subcat, importance, status","from #SC","where status = \\"苦手\\"","```",""]'),
])

# ---------- qstudio.py ----------
patch("qstudio.py", [
    ('VID_DIR = os.path.join(ROOT, "output", "CAMS_1問1動画")',
     'VID_DIR = os.path.join(ROOT, "output", "SC_1問1動画")'),
])

# ---------- obsidian_setup.py: #CAMS -> #SC ----------
osp = os.path.join(B, "obsidian_setup.py")
if os.path.exists(osp):
    t = open(osp, encoding="utf-8").read()
    t2 = t.replace("#CAMS", "#SC").replace("CAMS_Obsidian_Vault", "SC_Obsidian_Vault")
    open(osp, "w", encoding="utf-8").write(t2)
    print("patched obsidian_setup.py")

print("DONE")
