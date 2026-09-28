#!/usr/bin/env python3
"""指定スライドを先頭に並べ替えたコピーを作る（macOS qlmanage で1枚だけ描画確認する用）。
使い方: python3 build/rs.py IN.pptx 9 OUT.pptx   →  9枚目を先頭にした OUT.pptx
※ qlmanage/open は macOS 専用。クラウド(Linux)では使えない（生成・整合性チェックは可能）。
"""
import sys, shutil
from pptx import Presentation
src, idx, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
shutil.copy(src, out)
p = Presentation(out)
xml = p.slides._sldIdLst
ids = list(xml)
tgt = ids[idx - 1]
xml.remove(tgt); xml.insert(0, tgt)
p.save(out)
print("reordered", idx)
