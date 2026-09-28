#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CAMS 750問 学習・進捗管理ツール.

進捗は data/study_progress.json に保存（id => 状態）。
状態判定:
  - unseen : 未学習
  - weak   : 苦手（直近で誤答 / streak<0 寄り）
  - learning: 学習中（1回は正解したが定着不十分）
  - strong : 得意（連続正解2回以上）
"""
import json, glob, re, sys, os, datetime, argparse, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK_DIR = os.path.join(ROOT, "data", "decks_official")
PROG = os.path.join(ROOT, "data", "study_progress.json")

def load_questions():
    qs = {}
    for f in sorted(glob.glob(os.path.join(DECK_DIR, "dt_*.json"))):
        sc = re.search(r"dt_(\d+-\d+)_", f).group(1)
        d = json.load(open(f, encoding="utf-8"))
        for q in d.get("questions", []):
            qid = str(q.get("id"))
            qs[qid] = {
                "id": qid, "sc": sc,
                "tag": q.get("tag", ""),
                "q": q.get("q_jp", ""),
                "choices": q.get("choices_jp", []),
                "answer": q.get("answer_letters", []),
                "answer_jp": q.get("answer_jp", ""),
                "explain": q.get("explain_jp", ""),
                "topic": d.get("topic_jp", ""),
            }
    return qs

def load_prog():
    if os.path.exists(PROG):
        return json.load(open(PROG, encoding="utf-8"))
    return {}

def save_prog(p):
    json.dump(p, open(PROG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def status_of(rec):
    if rec is None or rec.get("correct",0)+rec.get("wrong",0)==0:
        return "unseen"
    streak = rec.get("streak",0)
    if streak <= -1: return "weak"
    if streak >= 2:  return "strong"
    return "learning"

def ensure(p, qid):
    if qid not in p:
        p[qid] = {"correct":0,"wrong":0,"streak":0,"last":None}
    return p[qid]

def cmd_pick(args):
    qs = load_questions(); p = load_prog()
    items = list(qs.values())
    if args.sc:
        items = [q for q in items if q["sc"] in args.sc]
    # priority: weak > unseen > learning > strong; tie-break by sc/id order
    prio = {"weak":0,"unseen":1,"learning":2,"strong":3}
    def key(q):
        st = status_of(p.get(q["id"]))
        return (prio[st], tuple(int(x) for x in q["sc"].split("-")), int(q["id"]))
    if args.mode:
        items = [q for q in items if status_of(p.get(q["id"]))==args.mode]
    items.sort(key=key)
    out = items[:args.n]
    # don't leak answers unless --withanswer
    res = []
    for q in out:
        r = {"id":q["id"],"sc":q["sc"],"tag":q["tag"],"q":q["q"],
             "choices":q["choices"],"status":status_of(p.get(q["id"]))}
        if args.withanswer:
            r["answer"]=q["answer"]; r["answer_jp"]=q["answer_jp"]; r["explain"]=q["explain"]
        res.append(r)
    print(json.dumps(res, ensure_ascii=False, indent=1))

def cmd_grade(args):
    qs = load_questions(); p = load_prog()
    today = datetime.date.today().isoformat()
    toks = args.pairs
    i=0
    changed=[]
    while i < len(toks)-1:
        qid = toks[i]; res = toks[i+1].lower(); i+=2
        if qid not in qs:
            print(f"!! unknown id {qid}", file=sys.stderr); continue
        rec = ensure(p, qid)
        if res in ("ok","o","1","correct","c"):
            rec["correct"]+=1; rec["streak"]=max(1, rec["streak"]+1)
            mark="○"
        else:
            rec["wrong"]+=1; rec["streak"]=min(-1, rec["streak"]-1) if rec["streak"]<=0 else -1
            mark="×"
        rec["last"]=today
        changed.append((qid, mark, status_of(rec)))
    save_prog(p)
    for qid,mark,st in changed:
        print(f"{qid} {mark} -> {st}")

def cmd_stats(args):
    qs = load_questions(); p = load_prog()
    by = collections.Counter(); bysc=collections.defaultdict(collections.Counter)
    for qid,q in qs.items():
        st = status_of(p.get(qid)); by[st]+=1; bysc[q["sc"]][st]+=1
    total=len(qs)
    print(f"=== 全体 {total}問 ===")
    for st in ["strong","learning","weak","unseen"]:
        print(f"  {st:9s}: {by[st]}")
    seen = total - by["unseen"]
    print(f"  学習済み: {seen}/{total}")
    if args.verbose:
        print("=== サブカテゴリ別 (strong/learning/weak/unseen) ===")
        for sc in sorted(bysc, key=lambda x:tuple(int(i) for i in x.split('-'))):
            c=bysc[sc]
            print(f"  {sc}: {c['strong']}/{c['learning']}/{c['weak']}/{c['unseen']}")

def cmd_show(args):
    qs = load_questions()
    for qid in args.ids:
        q=qs.get(qid)
        if not q: print(f"!! unknown {qid}"); continue
        print(json.dumps(q, ensure_ascii=False, indent=1))

ap = argparse.ArgumentParser()
sub = ap.add_subparsers()
a=sub.add_parser("pick"); a.add_argument("n",type=int,nargs="?",default=5)
a.add_argument("--sc",nargs="*"); a.add_argument("--mode",choices=["weak","unseen","learning","strong"])
a.add_argument("--withanswer",action="store_true"); a.set_defaults(func=cmd_pick)
a=sub.add_parser("grade"); a.add_argument("pairs",nargs="+"); a.set_defaults(func=cmd_grade)
a=sub.add_parser("stats"); a.add_argument("-v","--verbose",action="store_true"); a.set_defaults(func=cmd_stats)
a=sub.add_parser("show"); a.add_argument("ids",nargs="+"); a.set_defaults(func=cmd_show)
args=ap.parse_args()
if hasattr(args,"func"): args.func(args)
else: ap.print_help()
