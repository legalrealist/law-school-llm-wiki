#!/usr/bin/env python3
"""Concept diagram for the law-school-llm-wiki pattern (illustrative)."""
from PIL import Image, ImageDraw, ImageFont
import os
W,H=1160,560
BG=(255,255,255); INK=(23,30,40); MUT=(110,120,132)
B1=(235,242,255); E1=(70,120,210)      # sources (blue)
B2=(236,247,239); E2=(40,160,90)        # claude (green)
B3=(245,239,252); E3=(150,90,200)       # wiki (purple)
LINE=(150,160,172)
ARIALB="/System/Library/Fonts/Supplemental/Arial Bold.ttf"; ARIAL="/System/Library/Fonts/Supplemental/Arial.ttf"
def f(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()
title=f(ARIALB,29); bt=f(ARIALB,21); body=f(ARIAL,16); small=f(ARIAL,16); lbl=f(ARIALB,15)
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
d.text((46,28),"Build the wiki first — knowledge compounds",font=title,fill=INK)
d.text((46,68),"Karpathy's LLM-wiki pattern, applied to law school: don't re-query raw documents — synthesize them into pages once.",font=small,fill=MUT)

def box(x,y,w,h,fill,edge,head,lines):
    d.rounded_rectangle([x,y,x+w,y+h],radius=14,fill=fill,outline=edge,width=2)
    d.text((x+18,y+16),head,font=bt,fill=edge)
    yy=y+50
    for ln in lines:
        d.text((x+18,yy),ln,font=body,fill=INK); yy+=24

bx=[46,440,834]; by=150; bw=280; bh=170
box(bx[0],by,bw,bh,B1,E1,"Sources  (raw/)",["• course outlines","• case briefs","• class notes  (.pdf/.docx)"])
box(bx[1],by,bw,bh,B2,E2,"Claude Code",["reads → extracts concepts","creates / updates pages","cross-links everything"])
box(bx[2],by,bw,bh,B3,E3,"Structured wiki",["one page per doctrine,","case, and course","Obsidian wikilinks throughout"])

def arrow(x0,y0,x1,y1):
    d.line([(x0,y0),(x1,y1)],fill=LINE,width=3)
    d.polygon([(x1,y1),(x1-12,y1-6),(x1-12,y1+6)],fill=LINE)
arrow(bx[0]+bw+6,by+bh/2,bx[1]-8,by+bh/2)
arrow(bx[1]+bw+6,by+bh/2,bx[2]-8,by+bh/2)

# feedback loop: wiki -> claude (over the top)
ytop=by-34
d.line([(bx[2]+bw/2,by),(bx[2]+bw/2,ytop)],fill=E3,width=3)
d.line([(bx[2]+bw/2,ytop),(bx[1]+bw/2,ytop)],fill=E3,width=3)
d.line([(bx[1]+bw/2,ytop),(bx[1]+bw/2,by-2)],fill=E3,width=3)
d.polygon([(bx[1]+bw/2,by-2),(bx[1]+bw/2-6,by-14),(bx[1]+bw/2+6,by-14)],fill=E3)
loop="each new source → re-extract & re-link → the wiki gets smarter"
lw=d.textlength(loop,font=lbl); d.text(((bx[1]+bw/2+bx[2]+bw/2)/2-lw/2, ytop-22),loop,font=lbl,fill=E3)

# footer contrast
fy=by+bh+58; d.line([(46,fy),(W-46,fy)],fill=(228,232,238),width=1)
d.text((46,fy+16),"RAG:",font=lbl,fill=(180,70,70)); d.text((110,fy+16),"retrieve chunks per question — nothing accumulates, every answer re-pieced from fragments.",font=small,fill=INK)
d.text((46,fy+44),"Wiki-first:",font=lbl,fill=E2); d.text((150,fy+44),"ingest once; every later question reads a synthesized, cross-referenced page.",font=small,fill=INK)

out=os.path.join(os.path.dirname(__file__),"how-it-works.png")
img.save(out); print("wrote",out,img.size)
