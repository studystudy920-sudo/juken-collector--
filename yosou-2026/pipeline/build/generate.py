#!/usr/bin/env python3
"""全182デッキ（ビジカ3.0ピクトグラム版）を data/manifest.json に従って再生成する。
使い方:  python3 build/generate.py            # 全182本
         python3 build/generate.py 1-2        # 指定サブカテゴリのみ
出力先:  output/ビジカ3.0版/<ドメイン>/<サブカテゴリ>/CAMS_<sc>_<nn>_<theme>.pptx
"""
import os, json, subprocess, sys

ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA  = os.path.join(ROOT, "data", "decks_official")
MAN   = os.path.join(ROOT, "data", "manifest.json")
OUT   = os.path.join(ROOT, "output", "ビジカ3.0版")
BUILD = os.path.join(ROOT, "build", "build_biz30.py")

man = json.load(open(MAN, encoding="utf-8"))
only = sys.argv[1] if len(sys.argv) > 1 else None
if only:
    man = [e for e in man if e["subcat"] == only]

ok, fail = 0, []
for e in man:
    jp = os.path.join(DATA, e["json"])
    outdir = os.path.join(OUT, e["domain_folder"], e["subcat_folder"])
    os.makedirs(outdir, exist_ok=True)
    outp = os.path.join(outdir, e["out_filename"])
    r = subprocess.run([sys.executable, BUILD, jp, outp, e["label"]],
                       capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(outp):
        ok += 1
    else:
        fail.append((e["out_filename"], r.stderr[-300:]))

print(f"生成 {ok}/{len(man)} 本")
nq = sum(e["n_questions"] for e in man)
print(f"問題数 {nq}（スライド = 8 + 4×問題数 / デッキ）")
for fn, err in fail[:20]:
    print("FAIL", fn, "::", err)
