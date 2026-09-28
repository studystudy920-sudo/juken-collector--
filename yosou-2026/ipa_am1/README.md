# 午前I（科目A-1）公式過去問 パイプライン化メモ

情報処理技術者試験・高度共通「午前I」の公式過去問を学習パイプライン化するための調査結果（実DL・抽出検証済み）。個人学習用。

## 確定URL（IPA年度ページから辿って確認）

起点: R7=`https://www.ipa.go.jp/shiken/mondai-kaiotu/2025r07.html` / R6=`.../2024r06.html`
※att配下のハッシュ（`nl10bi...`/`m42obm...`）は年度ページごとに異なる。年度が変わったら必ず年度ページから辿る（推測不可）。

| 回 | qs(問題) | ans(解答) |
|---|---|---|
| R7秋 2025r07a | .../nl10bi0000009lh8-att/2025r07a_koudo_am1_qs.pdf | .../2025r07a_koudo_am1_ans.pdf |
| R7春 2025r07h | .../nl10bi0000009lh8-att/2025r07h_koudo_am1_qs.pdf | .../2025r07h_koudo_am1_ans.pdf |
| R6秋 2024r06a | .../m42obm000000afqx-att/2024r06a_koudo_am1_qs.pdf | .../2024r06a_koudo_am1_ans.pdf |
| R6春 2024r06h | .../m42obm000000afqx-att/2024r06h_koudo_am1_qs.pdf | .../2024r06h_koudo_am1_ans.pdf |

DL済み（`yosou-2026/ipa_am1/`）: 2025r07a(qs+ans), 2025r07h(ans), 2024r06a(qs+ans)。

## 抽出方法（検証済み）
- **解答ans**: 文字あり。pymupdf `page.get_text()` → 正規表現 `問(\d+)\s*([アイウエ])` で 問1〜30 の正解を確実に抽出（自動化可）。**正解の正はこのans**。
- **問題qs**: 画像のみ（本文0文字）。20ページ・各1画像。`page.get_pixmap(dpi=200〜300)` でPNG化（1434x2025, 約180KB/枚）。→ **問題文はOCRまたはClaudeのvisionで書き起こし**が必要。図表・選択肢図が多く、図問は画像添付前提が無難。
- 環境: `pdftotext`/`pdfimages`/tesseract は未導入。pymupdfは利用可。

## 制度変更（令和8年度〜 CBT／科目A・B）※IPA1次情報
- 1次情報: https://www.ipa.go.jp/shiken/2026/ap_koudo_sc-cbt.html ／ プレス https://www.ipa.go.jp/pressrelease/2025/press20250812.html ／ 要綱Ver5.5
- AP・高度8区分・SCがペーパー→**CBT**へ。名称: 午前Ⅰ→**科目A-1**／午前Ⅱ→科目A-2／午後Ⅰ→科目B-1／午後Ⅱ→科目B-2。午前Ⅰ免除→**科目A-1試験免除**として継続。
- 実施: 春期区分→前期（2026/11頃）、秋期区分→後期（2027/2頃）。
- **出題内容・形式・問題数・時間は変更なし**。→ 午前Ⅰ=科目A-1の30問・4択（ア〜エ）は継続想定、既存過去問素材はそのまま有効。

## 次段の設計方針
1. ans PDF から正解30問を自動抽出（pymupdf＋正規表現）。
2. qs PDF を各ページPNG化 → Claudeのvisionで問題文・選択肢を書き起こし（KNOWHOW §7の方式）→ ans と照合。
3. 図問はページ画像を添付する設計に。
4. 以降は SC予想と同じ問題データJSON（ア〜エ）→ デッキ/動画/ゼミページ/Obsidian/GoodNotes に流す。
