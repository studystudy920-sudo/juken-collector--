# SC予想 学習パイプライン（CAMSノウハウ移植版）

CAMSで実証済みの「1問1動画・動画ゼミページ・Obsidian・GoodNotes」パイプラインを、情報処理安全確保支援士(SC)予想問題に移植したもの。個人学習用（生成物・素材は第三者共有禁止）。

## 成果物（SC予想 7分野・午前II 40問）

### ① 動画ゼミページ（Artifact／ブラウザ・スマホ）
問題→解説動画→その場でClaudeと理解度対話（sample/db 有効・得意/苦手を記録）。

| 分野 | リンク |
|---|---|
| 1 暗号・認証・PKI | https://claude.ai/artifact/9hq6QUrKqxJc5B3opZTX38 |
| 2 ネットワーク・ゼロトラスト | https://claude.ai/artifact/G3YeUYs3JWtaxP3VW7URXC |
| 3 Web/アプリ脆弱性 | https://claude.ai/artifact/5qScMxMT4vqTJsRDFm94mc |
| 4 AIセキュリティ・LLM | https://claude.ai/artifact/MHzCSrx9HRfqjvmWPfoyeE |
| 5 マルウェア・攻撃・IR | https://claude.ai/artifact/5zcLPR6SJDPCtf7cZZnwiQ |
| 6 マネジメント・法規 | https://claude.ai/artifact/4PGWvAJhM1p2DbHWNufNpX |
| 7 AI駆動型攻撃 | https://claude.ai/artifact/3xLYjCuVhmE96XDg2MjJLa |

※非公開Artifact（所有者のみ閲覧可）。

### ② 1問1動画（MP4）
各問4枚（問題→図解→解答→実務）＋女性音声(Nanami)。声は低速(-8%)・問題後の間6秒。全40本・計約83MB。`output/SC_1問1動画/<分野>/`。

### ③ Obsidian保管庫
1問1ノート（Spaced Repetitionカード＋図解40枚＋日英＋実務メモ＋選択肢別正誤）、分野別MOC(Dataview)、プラグイン同梱。`output/SC_Obsidian_Vault/`（zip配布）。

### ④ GoodNotes教材
分野別の要点シート（markdown）＋概念図(mermaid)。GoodNotesウィジェットとして生成（チャットから保存）。要点シート元データ: `output/goodnotes/sc_<n>.md`。

## 構成
- `data/decks_official/dt_<分野>_1.json` … 問題データ(全成果物の起点・40問)
- `data/manifest.json` … デッキ一覧
- `build/` … 生成スクリプト（CAMSからSC移植：記号ア〜エ、分野名、中核構造図のJSON駆動化、IPAフォント、ブランディング）
- `output/`, `.render/` … 生成物・中間（.gitignore）

## 再生成コマンド
```bash
cd yosou-2026/pipeline
python3 setup_data.py                                   # JSON配置+manifest
python3 build/render_all.py --kind diagram --out .render/attachments  # 全デッキPDF+図解PNG
python3 build/obsidian.py --images --en --img-src .render/attachments # Obsidian
python3 build/qvideo.py --all --jobs 6                  # 全動画(-8%/間6秒)
python3 build/qstudio.py <分野>                          # 動画ゼミページHTML
```
※コンテナ再作成でツールが消えるため、`pip install python-pptx pymupdf pillow edge-tts` と `apt-get install -y ffmpeg libreoffice-impress` を先に。SessionStartフック化推奨（KNOWHOW §7）。

## 次段：午前I（科目A-1）公式過去問
`../ipa_am1/README.md` 参照（URL・抽出方法・CBT制度変更）。解答PDFは自動抽出、問題PDFはvision書き起こしでJSON化 → 同じパイプラインに投入。
