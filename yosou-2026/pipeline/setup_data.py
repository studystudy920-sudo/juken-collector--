#!/usr/bin/env python3
# JSON完成後: pipeline/data/dt_*.json を decks_official へ配置し、manifest.json を生成する
import json, os, glob, shutil, re
ROOT = "/home/user/juken-collector--/yosou-2026/pipeline"
DATA = os.path.join(ROOT, "data")
DECKS = os.path.join(DATA, "decks_official")
os.makedirs(DECKS, exist_ok=True)

NAMES = {
 "1": ("暗号認証PKI", "暗号・認証・PKI"),
 "2": ("NWゼロトラスト", "ネットワーク・クラウド・ゼロトラスト"),
 "3": ("Webアプリ脆弱性", "Web/アプリケーション脆弱性"),
 "4": ("AIセキュリティ", "AIセキュリティ・LLM"),
 "5": ("攻撃手法IR", "マルウェア・攻撃手法・インシデント対応"),
 "6": ("マネジメント法規", "セキュリティマネジメント・法規"),
 "7": ("AI駆動型攻撃", "AI駆動型サイバー攻撃・フロンティアAI"),
}

# move dt_*.json from data/ root into decks_official/
for f in glob.glob(os.path.join(DATA, "dt_*.json")):
    shutil.move(f, os.path.join(DECKS, os.path.basename(f)))

manifest = []
for n in ["1","2","3","4","5","6","7"]:
    fp = os.path.join(DECKS, f"dt_{n}_1.json")
    if not os.path.exists(fp):
        print("MISSING:", fp); continue
    d = json.load(open(fp, encoding="utf-8"))
    nq = len(d.get("questions", []))
    short, full = NAMES[n]
    manifest.append({
        "subcat": n,
        "json": f"dt_{n}_1.json",
        "domain_folder": f"{n}_{full}",
        "subcat_folder": f"{n}_{short}",
        "out_filename": f"SC_{n}_{short}.pptx",
        "label": f"{n} {full}",
        "n_questions": nq,
    })
    print(f"dt_{n}_1.json : {nq}問  ({full})")

json.dump(manifest, open(os.path.join(DATA, "manifest.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("manifest.json:", len(manifest), "decks")
