#!/usr/bin/env python3
"""
juken-collector: 大学入試 過去問PDF ダウンローダ

sources.txt の各起点URLからページを取得し、リンクされている PDF を辿って
downloads/<ドメイン>/ 以下に保存する。年度別サブページも1階層だけ辿る。

- 取得したPDFは downloads/ に保存され .gitignore で除外される（＝手元での個人利用）。
  入試問題には第三者著作物が含まれるため、再配布・公開は各大学の許諾が必要。
- 登録/ログインが必要なサイトの中身は取得できない。

使い方:
    python3 download_pdfs.py                # sources.txt を使用
    python3 download_pdfs.py URL [URL ...]  # URLを直接指定
    python3 download_pdfs.py --list-only    # ダウンロードせずPDFリンク一覧のみ表示
"""
from __future__ import annotations
import os, re, sys, csv, time, html, urllib.parse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT, "downloads")
UA = "Mozilla/5.0 (juken-collector; personal study use)"
PAGE_TIMEOUT = 30
PDF_TIMEOUT = 90
MAX_SUBPAGES_PER_SOURCE = 40   # 起点ごとに辿るHTMLサブページ数の上限
MAX_PDFS_PER_SOURCE = 400      # 起点ごとのPDF取得数の上限
SLEEP = 0.5                    # サーバ負荷軽減のための待機（秒）

# 年度別ページらしいリンクだけ辿るためのヒント
SUBPAGE_HINTS = re.compile(
    r"(kakomon|past|exam|question|mondai|answer|kaito|nyushi|"
    r"r[0-9]{1,2}|h[23][0-9]|20[12][0-9]|令和|平成|年度)", re.I)


def fetch(url: str, timeout: int) -> tuple[bytes, str, str]:
    """URLを取得して (本文bytes, Content-Type, 最終URL) を返す。"""
    req = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urlopen(req, timeout=timeout) as r:
        return r.read(), (r.headers.get("Content-Type") or "").lower(), r.geturl()


def find_links(base_url: str, body: bytes) -> tuple[list[str], list[str]]:
    """HTMLから (PDFリンク, 同一ドメインのHTMLサブページ) を抽出して返す。"""
    text = body.decode("utf-8", "ignore")
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', text, re.I)
    pdfs, pages = [], []
    base_host = urllib.parse.urlparse(base_url).netloc
    for h in hrefs:
        h = html.unescape(h.strip())
        if h.startswith(("mailto:", "javascript:", "#")):
            continue
        absu = urllib.parse.urljoin(base_url, h)
        path = urllib.parse.urlparse(absu).path.lower()
        if path.endswith(".pdf"):
            pdfs.append(absu)
        elif (path.endswith((".html", ".htm", "/")) or "." not in path.split("/")[-1]):
            if urllib.parse.urlparse(absu).netloc == base_host and SUBPAGE_HINTS.search(absu):
                pages.append(absu)
    # 重複除去（順序維持）
    return list(dict.fromkeys(pdfs)), list(dict.fromkeys(pages))


def safe_name(url: str) -> str:
    name = urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(url).path))
    name = re.sub(r'[\\/:*?"<>|]+', "_", name) or "file.pdf"
    return name[:180]


def domain_dir(url: str) -> str:
    return urllib.parse.urlparse(url).netloc.replace(":", "_")


def download_pdf(url: str, manifest: list, list_only: bool) -> str:
    dest_dir = os.path.join(OUT_DIR, domain_dir(url))
    dest = os.path.join(dest_dir, safe_name(url))
    if list_only:
        print(f"  PDF  {url}")
        return "listed"
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        print(f"  skip (exists) {os.path.relpath(dest, ROOT)}")
        manifest.append((url, os.path.relpath(dest, ROOT), "exists"))
        return "exists"
    try:
        data, ctype, _ = fetch(url, PDF_TIMEOUT)
    except (HTTPError, URLError, TimeoutError, Exception) as e:  # noqa
        print(f"  FAIL {url}  ({e})")
        manifest.append((url, "", f"error:{e}"))
        return "error"
    if not (data[:5] == b"%PDF-" or "pdf" in ctype):
        print(f"  skip (not pdf) {url}")
        manifest.append((url, "", "not-pdf"))
        return "not-pdf"
    os.makedirs(dest_dir, exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)
    kb = len(data) // 1024
    print(f"  OK   {os.path.relpath(dest, ROOT)} ({kb} KB)")
    manifest.append((url, os.path.relpath(dest, ROOT), f"ok:{kb}KB"))
    return "ok"


def process_source(src: str, manifest: list, list_only: bool) -> None:
    print(f"\n=== {src} ===")
    try:
        body, ctype, final = fetch(src, PAGE_TIMEOUT)
    except Exception as e:  # noqa
        print(f"  ページ取得失敗: {e}")
        manifest.append((src, "", f"page-error:{e}"))
        return
    if final.lower().endswith(".pdf") or body[:5] == b"%PDF-":
        download_pdf(final, manifest, list_only)
        return
    pdfs, pages = find_links(final, body)
    print(f"  直リンPDF: {len(pdfs)} 件 / サブページ候補: {len(pages)} 件")
    seen_pdf = set()
    got = 0
    for p in pdfs:
        if got >= MAX_PDFS_PER_SOURCE:
            break
        if p in seen_pdf:
            continue
        seen_pdf.add(p)
        download_pdf(p, manifest, list_only)
        got += 1
        time.sleep(SLEEP)
    # 1階層だけサブページを辿る
    for i, page in enumerate(pages[:MAX_SUBPAGES_PER_SOURCE]):
        try:
            sub_body, _, sub_final = fetch(page, PAGE_TIMEOUT)
        except Exception:  # noqa
            continue
        sub_pdfs, _ = find_links(sub_final, sub_body)
        new = [x for x in sub_pdfs if x not in seen_pdf]
        if new:
            print(f"  [sub] {page}  -> PDF {len(new)} 件")
        for p in new:
            if got >= MAX_PDFS_PER_SOURCE:
                break
            seen_pdf.add(p)
            download_pdf(p, manifest, list_only)
            got += 1
            time.sleep(SLEEP)
        time.sleep(SLEEP)


def main() -> None:
    args = [a for a in sys.argv[1:]]
    list_only = "--list-only" in args
    args = [a for a in args if a != "--list-only"]
    if args:
        sources = args
    else:
        sp = os.path.join(ROOT, "sources.txt")
        with open(sp, encoding="utf-8") as f:
            sources = [ln.strip() for ln in f
                       if ln.strip() and not ln.lstrip().startswith("#")]
    print(f"起点URL: {len(sources)} 件 / 保存先: {OUT_DIR}"
          + ("  （--list-only: 取得なし）" if list_only else ""))
    manifest: list = []
    for src in sources:
        process_source(src, manifest, list_only)

    if not list_only:
        os.makedirs(OUT_DIR, exist_ok=True)
        mpath = os.path.join(OUT_DIR, "manifest.csv")
        with open(mpath, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["source_pdf_url", "saved_path", "status"])
            w.writerows(manifest)
        ok = sum(1 for _, _, s in manifest if s.startswith("ok"))
        print(f"\n完了: 取得成功 {ok} 件 / 記録 {len(manifest)} 件 -> {os.path.relpath(mpath, ROOT)}")


if __name__ == "__main__":
    main()
