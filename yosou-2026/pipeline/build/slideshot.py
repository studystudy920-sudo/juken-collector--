#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""問題id -> 該当デッキの該当スライドを PNG 化する.

使い方:
  python3 build/slideshot.py <qid> [--kind q|diagram|answer|practice|all]
出力: <RENDER_DIR>/q<qid>_<kind>.png のパスを stdout に1行ずつ表示。
仕組み: 該当 dt_*.json をビルド -> soffice で PDF 化 -> PyMuPDF で該当ページを PNG。
デッキ単位で pptx/pdf をキャッシュ（同デッキの別問題は再ビルドしない）。
"""
import os, sys, json, glob, re, subprocess, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK_DIR = os.path.join(ROOT, "data", "decks_official")
BUILD = os.path.join(ROOT, "build", "build_biz30.py")
RENDER = os.environ.get("RENDER_DIR", os.path.join(ROOT, ".render"))
os.makedirs(RENDER, exist_ok=True)
os.environ.setdefault("HOME", RENDER)

INTRO = 7          # 表紙/マップ/基礎概念4/コツ
PER = 4            # 1問=4枚
KIND_OFF = {"q":0, "diagram":1, "answer":2, "practice":3}

def find_deck(qid):
    qid = str(qid)
    for f in sorted(glob.glob(os.path.join(DECK_DIR, "dt_*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for i, q in enumerate(d.get("questions", [])):
            if str(q.get("id")) == qid:
                return f, i, d
    return None, None, None

def ensure_pdf(deckfile, label):
    base = os.path.splitext(os.path.basename(deckfile))[0]
    pptx = os.path.join(RENDER, base + ".pptx")
    pdf = os.path.join(RENDER, base + ".pdf")
    if not os.path.exists(pptx):
        subprocess.run([sys.executable, BUILD, deckfile, pptx, label],
                       check=True, capture_output=True, text=True)
    if not os.path.exists(pdf) or os.path.getmtime(pdf) < os.path.getmtime(pptx):
        r = subprocess.run(["soffice","--headless","--norestore","--nologo",
              f"-env:UserInstallation=file://{RENDER}/lo",
              "--convert-to","pdf","--outdir",RENDER, pptx],
              capture_output=True, text=True)
        if not os.path.exists(pdf):
            sys.exit("PDF変換失敗: " + r.stderr[-300:])
    return pdf

def render(qid, kinds):
    import fitz
    deckfile, idx, d = find_deck(qid)
    if deckfile is None:
        sys.exit(f"qid {qid} が見つかりません")
    label = d.get("topic_jp", "")
    pdf = ensure_pdf(deckfile, label)
    doc = fitz.open(pdf)
    base_page = INTRO + PER * idx      # 0-indexed: 問題スライド
    out = []
    for k in kinds:
        pno = base_page + KIND_OFF[k]
        pg = doc[pno]
        pix = pg.get_pixmap(matrix=fitz.Matrix(2, 2))
        p = os.path.join(RENDER, f"q{qid}_{k}.png")
        pix.save(p)
        out.append(p)
    return out

ap = argparse.ArgumentParser()
ap.add_argument("qid")
ap.add_argument("--kind", default="q")
a = ap.parse_args()
kinds = list(KIND_OFF) if a.kind == "all" else a.kind.split(",")
for p in render(a.qid, kinds):
    print(p)
