#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全問（または指定サブカテゴリ）の指定スライドを一括PNG化する.
soffice は全pptxを1回でPDF化（起動コスト償却）。出力: <OUT>/Q<id4桁>_<kind>.png
使い方: python3 build/render_all.py --kind diagram --out <DIR> [--sc 1-1 ...]
"""
import os,sys,json,glob,re,subprocess,argparse,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK_DIR=os.path.join(ROOT,"data","decks_official")
BUILD=os.path.join(ROOT,"build","build_biz30.py")
CACHE=os.path.join(ROOT,".render")
os.makedirs(CACHE,exist_ok=True)
os.environ.setdefault("HOME",CACHE)
INTRO=7; PER=4; KIND_OFF={"q":0,"diagram":1,"answer":2,"practice":3}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--kind",default="diagram")
    ap.add_argument("--out",required=True)
    ap.add_argument("--sc",nargs="*")
    ap.add_argument("--zoom",type=float,default=1.5)
    ap.add_argument("--optimize",action="store_true",
                    help="パレットPNGに軽量化（Vault配布用。要 Pillow）")
    ap.add_argument("--opt-scale",type=float,default=0.78)
    ap.add_argument("--opt-colors",type=int,default=56)
    a=ap.parse_args(); os.makedirs(a.out,exist_ok=True)
    kinds=a.kind.split(",")
    decks=[]
    for f in sorted(glob.glob(os.path.join(DECK_DIR,"dt_*.json"))):
        sc=re.search(r"dt_(\d+)_",f).group(1)
        if a.sc and sc not in a.sc: continue
        d=json.load(open(f,encoding="utf-8")); decks.append((f,sc,d))
    # 1) build pptx
    t=time.time(); pptxs=[]
    for f,sc,d in decks:
        base=os.path.splitext(os.path.basename(f))[0]
        pptx=os.path.join(CACHE,base+".pptx")
        if not os.path.exists(pptx):
            subprocess.run([sys.executable,BUILD,f,pptx,d.get("topic_jp","")],
                           check=True,capture_output=True,text=True)
        pptxs.append((base,pptx,d))
    print(f"pptx {len(pptxs)}本 ({time.time()-t:.0f}s)")
    # 2) batch convert to pdf (only missing/stale)
    need=[p for b,p,d in pptxs if not os.path.exists(os.path.join(CACHE,b+".pdf"))
          or os.path.getmtime(os.path.join(CACHE,b+".pdf"))<os.path.getmtime(p)]
    if need:
        t=time.time()
        # convert in chunks to avoid huge argv
        for i in range(0,len(need),40):
            chunk=need[i:i+40]
            subprocess.run(["soffice","--headless","--norestore","--nologo",
                f"-env:UserInstallation=file://{CACHE}/lo",
                "--convert-to","pdf","--outdir",CACHE]+chunk,
                capture_output=True,text=True)
        print(f"pdf変換 {len(need)}本 ({time.time()-t:.0f}s)")
    # 3) extract pages
    import fitz
    t=time.time(); nimg=0
    for base,pptx,d in pptxs:
        pdf=os.path.join(CACHE,base+".pdf")
        if not os.path.exists(pdf): print("PDF無:",base); continue
        doc=fitz.open(pdf)
        for idx,q in enumerate(d.get("questions",[])):
            qid=int(q.get("id"))
            for k in kinds:
                pno=INTRO+PER*idx+KIND_OFF[k]
                if pno>=doc.page_count: continue
                pix=doc[pno].get_pixmap(matrix=fitz.Matrix(a.zoom,a.zoom))
                outp=os.path.join(a.out,f"Q{qid:04d}_{k}.png")
                pix.save(outp); nimg+=1
                if a.optimize:
                    from PIL import Image
                    im=Image.open(outp).convert("RGB")
                    w,h=im.size
                    im=im.resize((int(w*a.opt_scale),int(h*a.opt_scale)),Image.LANCZOS)
                    im.quantize(colors=a.opt_colors,method=Image.FASTOCTREE)\
                      .save(outp,optimize=True)
        doc.close()
    print(f"PNG {nimg}枚 ({time.time()-t:.0f}s) -> {a.out}")
main()
