# -*- coding: utf-8 -*-
import json, os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn

BASE="/Users/massa/Library/CloudStorage/OneDrive-個人用/Cowork_作成物/CAMS_OCR"
import sys
IN=sys.argv[1]; OUT=sys.argv[2]; DLABEL=sys.argv[3] if len(sys.argv)>3 else ""
d=json.load(open(IN,encoding="utf-8"))
TOTAL=8+4*len(d["questions"])
LABEL=(d.get("topic_en") or "CAMS")[:64]

# ---- premium palette ----
NAVY=RGBColor(0x16,0x1F,0x4A); NAVY2=RGBColor(0x25,0x31,0x6E); DARK=RGBColor(0x1E,0x26,0x46)
ICE=RGBColor(0xCF,0xDB,0xF5); STEEL=RGBColor(0x5B,0x69,0x9A)
GREEN=RGBColor(0x1B,0x7A,0x55); LGREEN=RGBColor(0xE6,0xF3,0xEC)
RED=RGBColor(0xC0,0x39,0x2B); LRED=RGBColor(0xFB,0xEA,0xE8)
AMBER=RGBColor(0xB5,0x6A,0x09); LAMBER=RGBColor(0xFB,0xF0,0xDA)
TEAL=RGBColor(0x12,0x6E,0x82); LTEAL=RGBColor(0xE3,0xEF,0xF2)
INDIGO=RGBColor(0x3A,0x3F,0x9E); LIND=RGBColor(0xEC,0xEE,0xFA)
GREY=RGBColor(0x55,0x5B,0x6E); MUTE=RGBColor(0x9A,0xA3,0xBF)
WHITE=RGBColor(0xFF,0xFF,0xFF); PAPER=RGBColor(0xF6,0xF8,0xFC); CARD=RGBColor(0xFF,0xFF,0xFF)
LINEC=RGBColor(0xDD,0xE2,0xEE)
HEAD="IPAPGothic"; BODY="IPAPGothic"; JPF="IPAPGothic"
# ---- ビジカ3.0 モノクロ＋金 上書き ----
INKc=RGBColor(0x26,0x26,0x26); GOLD=RGBColor(0xF5,0xC8,0x42); CAP=RGBColor(0xF2,0xF2,0xF0); SUB=RGBColor(0x8A,0x8A,0x8A)
NAVY=INKc; NAVY2=INKc; DARK=INKc; TEAL=INKc; INDIGO=INKc; STEEL=INKc; AMBER=INKc
GREY=SUB; MUTE=SUB; ICE=SUB; LINEC=RGBColor(0xD9,0xD9,0xD9)
PAPER=WHITE; CARD=WHITE
LGREEN=CAP; LRED=CAP; LTEAL=CAP; LAMBER=CAP; LIND=CAP
GREEN=RGBColor(0x1B,0x6E,0x3A); RED=RGBColor(0xB2,0x2A,0x1F)

prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(10)
W=13.333; H=10
def slide(bg=WHITE):
    s=prs.slides.add_slide(prs.slide_layouts[6])
    if bg is not None: box(s,0,0,W,H,bg)
    return s

def _ea(run):
    rPr=run._r.get_or_add_rPr()
    for tag in ("a:ea","a:cs"):
        el=rPr.find(qn(tag))
        if el is None: el=rPr.makeelement(qn(tag),{}); rPr.append(el)
        el.set("typeface", JPF)

def box(s,x,y,w,h,fill=None,line=None,lw=1.0,round_=False,shadow=False):
    shp=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE,
                           Inches(x),Inches(y),Inches(w),Inches(h))
    if fill is None: shp.fill.background()
    else: shp.fill.solid(); shp.fill.fore_color.rgb=fill
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb=line; shp.line.width=Pt(lw)
    shp.shadow.inherit=False
    if round_:
        try: shp.adjustments[0]=0.08
        except Exception: pass
    return shp

def oval(s,x,y,w,h,fill,line=None,lw=1.0):
    shp=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(x),Inches(y),Inches(w),Inches(h))
    shp.fill.solid(); shp.fill.fore_color.rgb=fill
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb=line; shp.line.width=Pt(lw)
    shp.shadow.inherit=False
    return shp

def tb(s,x,y,w,h,anchor=MSO_ANCHOR.TOP):
    t=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); f=t.text_frame
    f.word_wrap=True; f.vertical_anchor=anchor
    for m in ("margin_left","margin_right","margin_top","margin_bottom"): setattr(f,m,Inches(0.04))
    return f

def para(f,text,size,color,bold=False,font=BODY,align=PP_ALIGN.LEFT,sa=4,sb=0,first=False,bullet=None):
    p=f.paragraphs[0] if first and not f.paragraphs[0].runs else f.add_paragraph()
    p.alignment=align; p.space_after=Pt(sa); p.space_before=Pt(sb)
    if bullet:
        r0=p.add_run(); r0.text=bullet+" "; r0.font.size=Pt(size); r0.font.bold=True
        r0.font.name=font; r0.font.color.rgb=color; _ea(r0)
    r=p.add_run(); r.text=text; r.font.size=Pt(size); r.font.bold=bold
    r.font.name=font; r.font.color.rgb=color; _ea(r)
    return p

def runp(f,parts,size,align=PP_ALIGN.LEFT,sa=4,sb=0,first=False):
    p=f.paragraphs[0] if first and not f.paragraphs[0].runs else f.add_paragraph()
    p.alignment=align; p.space_after=Pt(sa); p.space_before=Pt(sb)
    for text,color,bold in parts:
        r=p.add_run(); r.text=text; r.font.size=Pt(size); r.font.bold=bold
        r.font.name=BODY; r.font.color.rgb=color; _ea(r)
    return p

def icon_circle(s,x,y,dia,emoji,fill,tcol=WHITE,sz=15):
    oval(s,x,y,dia,dia,fill)
    f=tb(s,x,y,dia,dia,MSO_ANCHOR.MIDDLE); f.word_wrap=False
    for m in ("margin_left","margin_right","margin_top","margin_bottom"): setattr(f,m,Inches(0))
    para(f,emoji,sz,tcol,align=PP_ALIGN.CENTER,first=True)

def badge(s,x,y,text,fill,tcol=WHITE,sz=9.5,w=None):
    wd=w if w else min(0.115*len(text)+0.34,3.6)
    b=box(s,x,y,wd,0.32,fill,None,round_=True)
    f=b.text_frame; f.word_wrap=False; f.vertical_anchor=MSO_ANCHOR.MIDDLE
    for m in ("margin_left","margin_right","margin_top","margin_bottom"): setattr(f,m,Inches(0.03))
    para(f,text,sz,tcol,bold=True,align=PP_ALIGN.CENTER,first=True)
    return wd

# section accent colors
SECT={"問題":INDIGO,"解答":GREEN,"実務":AMBER,"概念":TEAL,"map":TEAL}
def header(s,emoji,label,sub,accent,tag=None):
    icon_circle(s,0.42,0.20,0.56,emoji,accent,WHITE,17)
    f=tb(s,1.15,0.08,9.0,0.60,MSO_ANCHOR.MIDDLE)
    para(f,label,22,DARK,bold=True,font=HEAD,first=True)
    if sub:
        f2=tb(s,1.17,0.60,9.4,0.30,MSO_ANCHOR.MIDDLE); para(f2,sub,10.5,GREY,first=True)
    if tag:
        b=box(s,11.35,0.26,1.55,0.42,accent,None,round_=True)
        bf=b.text_frame; bf.vertical_anchor=MSO_ANCHOR.MIDDLE
        para(bf,tag,11,WHITE,bold=True,align=PP_ALIGN.CENTER,first=True)
    box(s,0.42,0.985,12.5,0.018,LINEC)

def footer(s,n):
    box(s,0.42,9.62,12.5,0.015,LINEC)
    f=tb(s,0.45,9.66,11.4,0.32,MSO_ANCHOR.MIDDLE)
    para(f,"SC EXAM PREP  —  "+LABEL+"   |   情報処理安全確保支援士",8.5,GREY,first=True)
    f2=tb(s,12.1,9.66,1.0,0.32,MSO_ANCHOR.MIDDLE); para(f2,f"{n} / {TOTAL}",9.5,GREY,align=PP_ALIGN.RIGHT,first=True)

def stars(freq):
    return "★"*freq+"☆"*(3-freq)

def regtags(s,x,y,w,regs,color=TEAL):
    cx=x
    for rg in regs:
        wd=min(0.135*len(rg)+0.3,3.4)
        if cx+wd>x+w:
            y+=0.42; cx=x
        b=box(s,cx,y,wd,0.34,LTEAL,color,0.75,round_=True)
        f=b.text_frame; f.word_wrap=False; f.vertical_anchor=MSO_ANCHOR.MIDDLE
        for m in ("margin_left","margin_right","margin_top","margin_bottom"): setattr(f,m,Inches(0.02))
        para(f,rg,9,color,bold=True,align=PP_ALIGN.CENTER,first=True)
        cx+=wd+0.12

# ---- arrows & diagrams ----
def arrow(s,x1,y1,x2,y2,color,danger=False,w=2.2,head=True):
    cn=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(x1),Inches(y1),Inches(x2),Inches(y2))
    cn.line.color.rgb=color; cn.line.width=Pt(w if not danger else w+0.7)
    ln=cn.line._get_or_add_ln()
    if head:
        ln.append(ln.makeelement(qn('a:tailEnd'),{'type':'triangle','w':'lg','len':'lg'}))
    return cn

INK=RGBColor(0x26,0x26,0x26)        # ビジカ3.0 近黒
COIN=RGBColor(0xF5,0xC8,0x42)       # 金¥
COIND=RGBColor(0x26,0x26,0x26)
LANE=RGBColor(0xFF,0xFF,0xFF)       # レーン非表示
FILLB=RGBColor(0xF2,0xF2,0xF0)      # 容器の塗り(淡)
FILLY=RGBColor(0xF9,0xE8,0x8A)      # ファンド黄
import re as _re
MONEYRE=_re.compile(r'[¥円]|投資|リターン|送金|入出金|入金|出金|支払|分配|賃料|出資|資金|手数料|融資|決済|預金|購入|現金|宿泊費|費用')

def _lineart(shp,color=INK,w=1.6,fill=None):
    if fill is None: shp.fill.solid(); shp.fill.fore_color.rgb=WHITE
    else: shp.fill.solid(); shp.fill.fore_color.rgb=fill
    shp.line.color.rgb=color; shp.line.width=Pt(w); shp.shadow.inherit=False
    return shp

def node_kind(label):
    t=label
    for kws,kind in [
        (("顧客","個人","保有者","犯罪者","投資家","従業員","担当","職員","オーナー","ミュール","人"),"person"),
        (("AI","システム","データ","技術","情報","ブランド","モデル","プラットフォーム","アルゴリズム","スコア","エンジン","ツール"),"ellipse"),
        (("ファンド","口座","信託","リスト","ウォレット","投資信託","台帳","DB","レポジトリ"),"container"),
        (("評価","ゲート","審査","スクリーニング","検証","チェック","承認"),"gate"),
        (("アラート","異常","検知","疑わし","赤旗","レッド","リスク"),"alert"),
        (("銀行","会社","法人","機関","事業者","当局","取引所","カジノ","業者","FIU","FATF","支店","本部","部門","規制"),"building"),
    ]:
        for k in kws:
            if k in t: return kind
    return "concept"

def draw_icon(s,cx,top,kind,color=INK,k=1.0):
    def rc(sh,dx,dy,w,h,lw=1.5,fill=None):
        return _lineart(s.shapes.add_shape(sh,Inches(cx+dx*k),Inches(top+dy*k),Inches(w*k),Inches(h*k)),color,lw,fill)
    if kind=="person":
        rc(MSO_SHAPE.OVAL,-0.16,0,0.32,0.32)
        body=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(cx-0.26*k),Inches(top+0.36*k),Inches(0.52*k),Inches(0.34*k))
        try: body.adjustments[0]=0.85
        except Exception: pass
        _lineart(body,color,1.5)
    elif kind=="building":
        rc(MSO_SHAPE.RECTANGLE,-0.31,0,0.62,0.74)
        for r in range(3):
            for c in range(2):
                rc(MSO_SHAPE.RECTANGLE,-0.205+c*0.205,0.10+r*0.205,0.135,0.135,1.2)
    elif kind=="container":
        rc(MSO_SHAPE.RECTANGLE,-0.25,0,0.50,0.74)
        rc(MSO_SHAPE.RECTANGLE,-0.205,0.33,0.41,0.37,1.0,fill=FILLB)
    elif kind=="ellipse":
        rc(MSO_SHAPE.OVAL,-0.45,0.18,0.90,0.40)
    elif kind=="gate":
        rc(MSO_SHAPE.DIAMOND,-0.32,0.02,0.64,0.70)
    elif kind=="alert":
        rc(MSO_SHAPE.ISOSCELES_TRIANGLE,-0.34,0.03,0.68,0.68)
        tf2=tb(s,cx-0.12*k,top+0.30*k,0.24*k,0.34*k,MSO_ANCHOR.MIDDLE); tf2.word_wrap=False
        para(tf2,"!",18*k,color,bold=True,align=PP_ALIGN.CENTER,first=True)
    else:  # concept/document
        rc(MSO_SHAPE.FOLDED_CORNER,-0.27,0.02,0.54,0.70)

def _label(s,cx,cy,text,color,w=2.4,sz=9.5):
    money=bool(MONEYRE.search(text or ""))
    tcol=INK if color is STEEL else color
    if money:
        coin=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(cx-w/2),Inches(cy-0.115),Inches(0.23),Inches(0.23))
        coin.fill.solid(); coin.fill.fore_color.rgb=COIN; coin.line.color.rgb=COIND; coin.line.width=Pt(1.0); coin.shadow.inherit=False
        ctf=coin.text_frame; ctf.word_wrap=False
        for m in ("margin_left","margin_right","margin_top","margin_bottom"): setattr(ctf,m,Inches(0))
        para(ctf,"¥",11,COIND,bold=True,align=PP_ALIGN.CENTER,first=True)
        b=box(s,cx-w/2+0.26,cy-0.15,w-0.26,0.30,WHITE,None)
        f=b.text_frame; f.word_wrap=False; f.vertical_anchor=MSO_ANCHOR.MIDDLE
        for m in ("margin_left","margin_right","margin_top","margin_bottom"): setattr(f,m,Inches(0.02))
        para(f,text,sz,tcol,bold=True,align=PP_ALIGN.LEFT,first=True)
    else:
        b=box(s,cx-w/2,cy-0.15,w,0.30,WHITE,None)
        f=b.text_frame; f.word_wrap=False; f.vertical_anchor=MSO_ANCHOR.MIDDLE
        for m in ("margin_left","margin_right","margin_top","margin_bottom"): setattr(f,m,Inches(0.02))
        para(f,text,sz,tcol,bold=True,align=PP_ALIGN.CENTER,first=True)

def _col(layers,nid):
    for ci,layer in enumerate(layers):
        for nn in layer:
            if nn["id"]==nid: return ci
    return -1

def diagram(s,x,y,w,h,spec,title=True,panel=True,iconk=1.0):
    if panel:
        box(s,x,y,w,h,WHITE,LINEC,1.0,round_=True)
        x+=0.2; y+=0.16; w-=0.4; h-=0.32
    if title and spec.get("title"):
        ic=tb(s,x,y,w,0.34); para(ic,spec["title"],12 if iconk<=1 else 14,DARK,bold=True,first=True)
        y+=0.44; h-=0.44
    layers=spec["layers"]; nc=len(layers)
    has_skip=any(abs(_col(layers,e["from"])-_col(layers,e["to"]))>=2
                 for e in spec.get("edges",[]) if _col(layers,e["from"])>=0 and _col(layers,e["to"])>=0)
    band=(0.62 if iconk>1 else 0.55) if has_skip else 0.0
    ih=0.74*iconk; loff=ih+0.10; lblsz=10.5 if iconk<=1 else 12.5
    nodeh=loff+(0.62 if iconk>1 else 0.60)
    colw=w/nc; nodew=min(colw-0.40,2.35 if iconk<=1 else 3.1)
    toproom=0.62*iconk
    # レーンは描かない（ビジカ3.0）
    rects={}; colof={}
    for ci,layer in enumerate(layers):
        cx0=x+colw*ci+(colw-nodew)/2
        m=len(layer); gap=0.5*iconk
        total=m*nodeh+(m-1)*gap
        sy=y+toproom+((h-band-toproom)-total)/2
        for ni,node in enumerate(layer):
            ny=sy+ni*(nodeh+gap)
            dng=node.get("danger"); icol=RED if dng else INK
            kind=node_kind(node["label"])
            draw_icon(s,cx0+nodew/2,ny+0.02,kind,icol,k=iconk)
            ff=tb(s,cx0-0.06,ny+loff,nodew+0.12,nodeh-loff+0.2,MSO_ANCHOR.TOP)
            para(ff,node["label"],lblsz,(RED if dng else DARK),bold=True,align=PP_ALIGN.CENTER,first=True,sa=1)
            if node.get("role"): para(ff,node["role"],8.5 if iconk>1 else 7.5,GREY,align=PP_ALIGN.CENTER,sa=0)
            rects[node["id"]]=(cx0,ny,nodew,nodeh); colof[node["id"]]=ci
    maxbot=max((r[1]+r[3]) for r in rects.values()) if rects else (y+h-band)
    ybase=min(maxbot+(0.50 if iconk>1 else 0.34), y+h-band+0.20)  # ノード直下に浅く回す
    adj_i=0
    for e in spec.get("edges",[]):
        if e["from"] not in rects or e["to"] not in rects: continue
        fr=rects[e["from"]]; to=rects[e["to"]]; cf=colof[e["from"]]; ct=colof[e["to"]]
        col=RED if e.get("danger") else INK
        if abs(cf-ct)>=2:
            x1=fr[0]+fr[2]/2; x2=to[0]+to[2]/2
            arrow(s,x1,fr[1]+fr[3],x1,ybase,col,danger=e.get("danger"),head=False,w=2.2)
            arrow(s,x1,ybase,x2,ybase,col,danger=e.get("danger"),head=False,w=2.2)
            arrow(s,x2,ybase,x2,to[1]+to[3],col,danger=e.get("danger"),w=2.2)
            # ラベルは横断線の「下」に置き、線を分断しない
            if e.get("label"): _label(s,(x1+x2)/2,ybase+0.24,e["label"],col,w=2.9,sz=9)
        elif cf!=ct:
            if cf<ct: x1=fr[0]+fr[2]; x2=to[0]; yl=fr[1]+fr[3]/2; yr=to[1]+to[3]/2
            else: x1=fr[0]; x2=to[0]+to[2]; yl=fr[1]+fr[3]/2; yr=to[1]+to[3]/2
            arrow(s,x1,yl,x2,yr,col,danger=e.get("danger"),w=2.2)
            if e.get("label"):
                topn=min(fr[1],to[1]); tier=adj_i%2; adj_i+=1
                lw=min(abs(x2-x1)+0.7, (colw*0.92 if nc>=4 else 2.4))
                fsz=7.0 if nc>=4 else 8.5
                _label(s,(x1+x2)/2, topn-0.18-tier*0.30, e["label"], col, w=lw, sz=fsz)
        else:
            x1=fr[0]+fr[2]/2; arrow(s,x1,fr[1]+fr[3],x1,to[1],col,danger=e.get("danger"),w=2.2)
            if e.get("label"): _label(s,x1+1.0,(fr[1]+fr[3]+to[1])/2,e["label"],col)
    if spec.get("caption"):
        cf2=tb(s,x,y+h-0.30,w,0.46)
        lead="⚠ " if any(e.get("danger") for e in spec.get("edges",[])) else "› "
        para(cf2,lead+spec["caption"],10 if iconk<=1 else 11.5,DARK,bold=True,first=True)

def _clip(t,n):
    t=(t or "").strip()
    return t if len(t)<=n else t[:n-1]+"…"

def diagram_page(s,q,d,n):
    """フルページのハブ&スポーク図解スライド（ビジカ3.0調）"""
    no=q["no"]
    s2=slide()
    header(s2,"◆",f"図解 Q{no}",d["topic_en"]+" ・ "+q["tag"],INKc,f"Q{no}/5")
    # シナリオ着眼点（上部・余白の注釈ボックス）
    callout(s2,0.5,1.18,12.35,0.92,"📌","この図で押さえる構図",q.get("intro_jp",""),INKc,CAP)
    # フルページ図（大ピクトグラム・ハブ&スポーク）
    spec=q["diagram"]
    diagram(s2,0.5,2.22,12.35,5.55,spec,title=True,panel=False,iconk=1.45)
    # 最下部「論点」帯
    by=7.95; bh=0.95
    box(s2,0.5,by,12.35,bh,INKc,None,round_=True)
    box(s2,0.5,by,0.14,bh,GOLD)
    ans=("・".join(q.get("answer_letters",[]))+" "+_clip(q.get("answer_jp",""),46)).strip()
    trap=_clip(q.get("trap","") or q.get("hint_jp","") or "誤った経路・名義に注意",40)
    bf=tb(s2,0.78,by+0.06,11.9,bh-0.12,MSO_ANCHOR.MIDDLE)
    runp(bf,[("論点 ",GOLD,True),(q["tag"],WHITE,True)],12.5,first=True,sa=2)
    runp(bf,[("✗ 誤解「",GOLD,True),(trap,WHITE,False),("」 → ",GOLD,True),
             ("✓ 正解の核心「",GOLD,True),(ans,WHITE,True),("」",GOLD,True)],10.5,sa=0)
    footer(s2,n)

def table(s,x,y,w,h,data,colws,sizes=10.5,head_sizes=11.5,header_fill=NAVY):
    rows=len(data); cols=len(data[0])
    gt=s.shapes.add_table(rows,cols,Inches(x),Inches(y),Inches(w),Inches(h)).table
    gt.first_row=False; gt.horz_banding=False
    tot=sum(colws)
    for ci,cw in enumerate(colws): gt.columns[ci].width=Inches(w*cw/tot)
    for ri,row in enumerate(data):
        for ci,cell in enumerate(row):
            c=gt.cell(ri,ci)
            c.margin_left=Inches(0.08); c.margin_right=Inches(0.08); c.margin_top=Inches(0.04); c.margin_bottom=Inches(0.04)
            c.vertical_anchor=MSO_ANCHOR.MIDDLE
            if ri==0: c.fill.solid(); c.fill.fore_color.rgb=header_fill
            else: c.fill.solid(); c.fill.fore_color.rgb=WHITE
            txt=cell if isinstance(cell,str) else cell[0]
            color=WHITE if ri==0 else (cell[1] if not isinstance(cell,str) else DARK)
            bold=(ri==0) or (not isinstance(cell,str) and len(cell)>2 and cell[2])
            sz=head_sizes if ri==0 else sizes
            tf=c.text_frame; tf.word_wrap=True; p=tf.paragraphs[0]
            r=p.add_run(); r.text=txt; r.font.size=Pt(sz); r.font.bold=bold; r.font.name=BODY; r.font.color.rgb=color; _ea(r)
    return gt

def callout(s,x,y,w,h,emoji,title,body,color,lc):
    box(s,x,y,w,h,WHITE,color,1.1,round_=True); box(s,x,y,0.10,h,color)
    f=tb(s,x+0.26,y+0.10,w-0.40,h-0.18,MSO_ANCHOR.MIDDLE)
    runp(f,[(emoji+" ",color,True),(title,color,True)],11.5,first=True,sa=2)
    if body: para(f,body,10.5,DARK,sa=0)

# ===================== SLIDE 1: COVER =====================
s=slide(WHITE)
icon_circle(s,0.55,0.55,0.72,"🏛️",NAVY,WHITE,22)
f=tb(s,1.5,0.50,11.3,0.85,MSO_ANCHOR.MIDDLE)
para(f,"SC 予想演習"+(("  "+DLABEL) if DLABEL else ""),26,DARK,bold=True,font=HEAD,first=True)
f2=tb(s,0.6,1.55,12.2,0.55)
para(f2,d["topic_jp"]+"　/　"+d["topic_en"],14,GREY,first=True)
yy=2.45
for q in d["questions"]:
    b=box(s,0.75,yy,11.85,0.92,WHITE,LINEC,1.0,round_=True)
    icon_circle(s,0.95,yy+0.16,0.58,"Q"+str(q["no"]),NAVY,WHITE,14)
    ff=tb(s,1.75,yy+0.06,8.7,0.8,MSO_ANCHOR.MIDDLE)
    runp(ff,[(q["tag"],DARK,True),("　"+q["q_jp"][:30]+"…",GREY,False)],13,first=True)
    badge(s,10.7,yy+0.30,"頻出 "+stars(q.get("freq",2)),NAVY,WHITE,10)
    yy+=1.02
f3=tb(s,0.75,yy+0.2,12,0.6)
para(f3,"収録：概念6枚（学習マップ／中核構造図／比較表／用語集／規格マトリクス／試験のコツ）＋ 各問4枚",11,GREY,first=True)
para(f3,"※正解・解説・図解はAI生成。最終確認を推奨します。",10,MUTE,sa=0)
footer(s,1)

# ===================== SLIDE 2: LEARNING MAP =====================
s=slide(); header(s,"🗺️","学習マップ",d["topic_en"]+" — 全体像と学び方",TEAL,"MAP")
f=tb(s,0.5,1.15,12.3,0.55); para(f,d["shared"]["map_summary"],12.5,DARK,first=True)
_mn=[str(x) for x in (d["shared"].get("map_nodes") or []) if str(x).strip()][:5]
if len(_mn)<2: _mn=[d["topic_jp"][:10],"リスクの把握","統制・検知","当局報告"]
ov={"title":None,
 "layers":[[{"id":f"n{k}","label":lb}] for k,lb in enumerate(_mn)],
 "edges":[{"from":f"n{k}","to":f"n{k+1}"} for k in range(len(_mn)-1)],
 "caption":None}
diagram(s,0.5,1.85,12.3,5.0,ov,title=False)
_nq=len(d["questions"])
steps=[("STEP 1｜WHY","このサブカテゴリの構造とリスクの源を理解",INKc,"1"),
       ("STEP 2｜HOW",f"{_nq}問で頻出論点と検知の着眼点（レッドフラグ）",INKc,"2"),
       ("STEP 3｜WHAT","空-雨-傘で実務対応（EDD・照会・SAR起案）へ",INKc,"3")]
wx=4.02
for i,(t,desc,col,em) in enumerate(steps):
    x=0.5+i*(wx+0.2)
    box(s,x,7.15,wx,1.55,WHITE,col,1.1,round_=True); box(s,x,7.15,wx,0.1,col)
    icon_circle(s,x+0.18,7.35,0.5,em,col,WHITE,15)
    ff=tb(s,x+0.82,7.30,wx-0.95,1.3)
    para(ff,t,12.5,col,bold=True,first=True); para(ff,desc,10.5,DARK,sa=0)
footer(s,2)

# ===================== SLIDE 3: CONCEPT1 — 中核構造図 (JSON) =====================
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

# ===================== SLIDE 4: COMPARISON TABLE =====================
s=slide(); header(s,"②","基礎概念 — 混同しやすい概念 比較表","正しい・安全 と 誤り・危険 の対比",TEAL,"CONCEPT")
data=[["対象概念","🟢 正しい・安全",("🔴 誤り・危険（要注意）",WHITE,True)]]
for c in d["shared"]["comparison"]:
    data.append([(c["concept"],NAVY,True),(c["normal"],RGBColor(0x14,0x6B,0x4A),False),(c["suspicious"],RED,False)])
table(s,0.5,1.25,12.3,7.4,data,[2.1,4.0,4.7],sizes=11,head_sizes=11.5)
footer(s,4)

# ===================== SLIDE 5: GLOSSARY =====================
s=slide(); header(s,"③","基礎概念 — 必須用語集",d["topic_jp"]+" の頻出用語",TEAL,"CONCEPT")
gl=d["shared"]["glossary"]; colx=[0.5,6.92]; cw=5.9
for i,g in enumerate(gl):
    col=i//4; row=i%4; x=colx[col]; y=1.2+row*1.98
    box(s,x,y,cw+0.1,1.82,CARD,TEAL,0.9,round_=True); box(s,x,y,0.12,1.82,TEAL)
    icon_circle(s,x+0.2,y+0.18,0.46,str(i+1),TEAL,WHITE,13)
    ff=tb(s,x+0.78,y+0.12,cw-0.7,1.62)
    runp(ff,[(g["term"],NAVY,True),("  "+g["term_en"],GREY,False)],11.5,first=True,sa=2)
    para(ff,g["def"],10,DARK,sa=2)
    para(ff,"📚 "+g["regs"],9,TEAL,bold=True,sa=0)
footer(s,5)

# ===================== SLIDE 6: REG MATRIX =====================
s=slide(); header(s,"④","基礎概念 — 規格・法令マトリクス",d["topic_jp"]+" に関わる主要な規格・法令",TEAL,"CONCEPT")
data=[["規制 / Framework","適用範囲",("要点（コルレス／PTA論点）",WHITE,True)]]
for r in d["shared"]["reg_matrix"]:
    data.append([(r["reg"],NAVY,True),(r["scope"],DARK,False),(r["point"],DARK,False)])
table(s,0.5,1.2,12.3,5.7,data,[2.5,2.4,7.0],sizes=11,head_sizes=12)
callout(s,0.5,7.15,12.3,1.05,"💡","規格・法令は独立せず連動する。",d["shared"].get("map_summary",""),AMBER,LAMBER)
footer(s,6)

# ===================== SLIDE 7: EXAM TIPS / PITFALLS =====================
s=slide(); header(s,"🎯","試験のコツ & 頻出ひっかけ","Exam Strategy & Common Pitfalls",AMBER,"TIPS")
box(s,0.5,1.25,6.15,7.3,CARD,GREEN,1.1,round_=True); box(s,0.5,1.25,6.15,0.55,GREEN)
hf=tb(s,0.7,1.28,5.8,0.5,MSO_ANCHOR.MIDDLE); para(hf,"✅ 解くコツ（Exam Tips）",13,WHITE,bold=True,first=True)
ff=tb(s,0.78,2.0,5.6,6.4)
for i,t in enumerate(d["shared"].get("exam_tips",[])):
    icon_circle(s,0.7,2.05+i*1.5,0.4,str(i+1),GREEN,WHITE,12)
    pf=tb(s,1.22,2.0+i*1.5,5.2,1.45,MSO_ANCHOR.TOP); para(pf,t,11,DARK,first=True)
box(s,6.85,1.25,6.0,7.3,CARD,RED,1.1,round_=True); box(s,6.85,1.25,6.0,0.55,RED)
hf=tb(s,7.05,1.28,5.7,0.5,MSO_ANCHOR.MIDDLE); para(hf,"⚠️ よくあるひっかけ（Pitfalls）",13,WHITE,bold=True,first=True)
for i,t in enumerate(d["shared"].get("pitfalls",[])):
    icon_circle(s,7.05,2.1+i*2.0,0.42,"✗",RED,WHITE,13)
    pf=tb(s,7.6,2.05+i*2.0,5.1,1.9,MSO_ANCHOR.TOP); para(pf,t,11,DARK,first=True)
footer(s,7)

# ===================== PER-QUESTION (3 slides each) =====================
n=8
for q in d["questions"]:
    multi=len(q["answer_letters"])>1
    # ---------- A: 問題（全幅・テキスト中心） ----------
    s=slide(); header(s,"Q"+str(q["no"]),f"問題 Q{q['no']} ／ 5",d["topic_en"]+" ・ "+q["tag"],INDIGO,f"Q{q['no']}/5")
    # freq + multi badges
    badge(s,0.5,1.12,"頻出度 "+stars(q.get("freq",2)),INDIGO,WHITE,10)
    if multi: badge(s,2.3,1.12,"⚑ 解答を2つ選択",RED,WHITE,10)
    # 着眼点（全幅）
    callout(s,0.5,1.62,12.35,0.92,"📌","設問の着眼点",q["intro_jp"],AMBER,LAMBER)
    f2=tb(s,0.5,2.72,12.35,1.2)
    para(f2,q["q_jp"],15,DARK,bold=True,first=True)
    para(f2,q["q_en"],10.5,GREY,sa=0)
    # 選択肢（全幅・2列）
    chs=list(zip(q["choices_jp"],q["choices_en"]))
    half=(len(chs)+1)//2
    cols=[chs[:half],chs[half:]]
    for ci,grp in enumerate(cols):
        fx=0.5+ci*6.3
        fc=tb(s,fx,4.05,6.0,4.0); first=True
        for cj,ce in grp:
            para(fc,cj,12,NAVY,bold=True,first=first,sa=1); first=False
            para(fc,ce,9,MUTE,sa=8)
    # mnemonic strip（全幅）
    callout(s,0.5,8.55,12.35,0.78,"🧠","1行で覚える",q.get("mnemonic",""),TEAL,LTEAL)
    footer(s,n); n+=1
    # ---------- A2: 図解（フルページ・ハブ&スポーク） ----------
    diagram_page(s,q,d,n); n+=1
    # ---------- B: 解答・空雨傘・選択肢別 ----------
    s=slide(); header(s,"✓",f"解答・解説 Q{q['no']}","Answer & Explanation ・ Sky–Rain–Umbrella",GREEN,f"Q{q['no']}/5")
    ab=box(s,0.5,1.12,12.35,1.05,LGREEN,GREEN,1.3,round_=True); box(s,0.5,1.12,0.14,1.05,GREEN)
    icon_circle(s,0.75,1.32,0.62,"✓",GREEN,WHITE,20)
    af=tb(s,1.6,1.16,11.1,0.97,MSO_ANCHOR.MIDDLE)
    runp(af,[("正解 "+"・".join(q["answer_letters"])+"　",GREEN,True),(q["answer_jp"],DARK,True)],13,first=True)
    f=tb(s,0.5,2.32,12.35,1.15)
    para(f,q["explain_jp"],11,DARK,first=True,sa=2); para(f,q["explain_en"],9,GREY,sa=0)
    sru=[("☁ 空（事実 Facts）",q["sky"],TEAL,LTEAL),("☂ 雨（解釈 Interpretation）",q["rain"],AMBER,LAMBER),("⚑ 傘（行動 Action）",q["umbrella"],GREEN,LGREEN)]
    cw=4.05; yy=3.6
    for i,(t,items,col,lc) in enumerate(sru):
        x=0.5+i*(cw+0.13)
        box(s,x,yy,cw,2.55,lc,col,1.0,round_=True); box(s,x,yy,cw,0.42,col)
        hf=tb(s,x+0.12,yy+0.02,cw-0.24,0.4,MSO_ANCHOR.MIDDLE); para(hf,t,10.5,WHITE,bold=True,first=True)
        bf=tb(s,x+0.16,yy+0.5,cw-0.3,2.0); ff=True
        for it in items: para(bf,it,9.5,DARK,first=ff,bullet="・",sa=3); ff=False
    f=tb(s,0.5,6.32,12.35,0.32); para(f,"選択肢別の正誤と根拠",11.5,NAVY,bold=True,first=True)
    oy=6.72
    for o in q["options"]:
        good=o["correct"]
        box(s,0.5,oy,12.35,0.58,(LGREEN if good else LRED),(GREEN if good else RED),0.8,round_=True)
        icon_circle(s,0.62,oy+0.13,0.32,("✓" if good else "✗"),(GREEN if good else RED),WHITE,11)
        ff=tb(s,1.05,oy+0.02,11.7,0.54,MSO_ANCHOR.MIDDLE)
        runp(ff,[(o["letter"]+"： ",(GREEN if good else RED),True),(o["reason"],DARK,False)],10,first=True)
        oy+=0.605
    footer(s,n); n+=1
    # ---------- C: 実務・規制・実例 ----------
    s=slide(); header(s,"📋",f"実務・規格 Q{q['no']}","実務メモ・規格論点・実例・ひっかけ",AMBER,f"Q{q['no']}/5")
    # left col: bank notes
    box(s,0.5,1.15,6.35,7.35,WHITE,NAVY2,1.1,round_=True); box(s,0.5,1.15,0.10,7.35,NAVY2)
    hf=tb(s,0.72,1.22,6.0,0.44,MSO_ANCHOR.MIDDLE); para(hf,"📝 実務チェックポイント",12,NAVY2,bold=True,first=True)
    box(s,0.72,1.66,5.9,0.015,LINEC)
    bf=tb(s,0.72,1.78,6.0,6.6); ff=True
    for it in q["bank_notes"]: para(bf,it,10,DARK,first=ff,sa=7); ff=False
    # right col: trap / case / related / reg_detail
    callout(s,7.05,1.15,5.8,1.55,"⚠️","ひっかけ注意",q.get("trap",""),RED,LRED)
    callout(s,7.05,2.85,5.8,1.55,"📰","実例・教訓",q.get("case",""),AMBER,LAMBER)
    callout(s,7.05,4.55,5.8,1.05,"🔗","関連・つながり",q.get("related",""),TEAL,LTEAL)
    # reg_detail box
    box(s,7.05,5.75,5.8,2.73,WHITE,TEAL,1.1,round_=True); box(s,7.05,5.75,0.10,2.73,TEAL)
    hf=tb(s,7.25,5.80,5.5,0.4,MSO_ANCHOR.MIDDLE); para(hf,"📚 規制根拠の論点",11.5,TEAL,bold=True,first=True)
    box(s,7.25,6.20,5.45,0.015,LINEC)
    rf=tb(s,7.25,6.28,5.45,2.1); ff=True
    for rd in q.get("reg_detail",[]):
        runp_f=rf
        p=rf.paragraphs[0] if ff and not rf.paragraphs[0].runs else rf.add_paragraph()
        p.space_after=Pt(4)
        r1=p.add_run(); r1.text="▪ "+rd["reg"]+"： "; r1.font.size=Pt(9.5); r1.font.bold=True; r1.font.name=BODY; r1.font.color.rgb=TEAL; _ea(r1)
        r2=p.add_run(); r2.text=rd["point"]; r2.font.size=Pt(9.5); r2.font.name=BODY; r2.font.color.rgb=DARK; _ea(r2)
        ff=False
    footer(s,n); n+=1

# ===================== CLOSING =====================
s=slide(WHITE)
icon_circle(s,0.6,0.65,0.8,"🎓",TEAL,WHITE,24)
f=tb(s,1.65,0.62,11,0.9,MSO_ANCHOR.MIDDLE); para(f,"まとめ — "+d["topic_jp"],20,DARK,bold=True,font=HEAD,first=True)
rows=[]
for q in d["questions"]:
    mn=q.get("mnemonic","").strip()
    if mn: rows.append(f"{q.get('tag','')}：{mn}")
regs=[]
for q in d["questions"]:
    for r in q.get("related_regs",[]):
        if r not in regs: regs.append(r)
if regs: rows.append("規制連動＝"+"／".join(regs[:6]))
rows=rows[:8]
yy=2.0; rh=0.78; gap=0.14
for k2,txt in enumerate(rows,1):
    box(s,0.6,yy,12.1,rh,WHITE,LINEC,1.0,round_=True)
    nb=box(s,0.78,yy+0.17,0.44,0.44,NAVY,None,round_=True)
    ntf=nb.text_frame; ntf.vertical_anchor=MSO_ANCHOR.MIDDLE
    para(ntf,str(k2),12,WHITE,bold=True,align=PP_ALIGN.CENTER,first=True)
    tf2=tb(s,1.45,yy+0.06,11.1,rh-0.10,MSO_ANCHOR.MIDDLE)
    para(tf2,txt,12,DARK,bold=True,first=True)
    yy+=rh+gap
footer(s,TOTAL)

out=OUT
import os as _os
_os.makedirs(_os.path.dirname(out),exist_ok=True)
prs.save(out)
print("保存:",out,"／スライド:",len(prs.slides._sldIdLst))
