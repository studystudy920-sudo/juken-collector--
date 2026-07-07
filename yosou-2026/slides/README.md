# SC予想問題 スライドデッキ（CAMS形式）

CAMS試験対策デッキと同じ形式（表紙→学習マップ→基礎概念①〜④→試験のコツ→各問Sky-Rain-Umbrella→統合サマリー）で、SC予想問題を7分野・各14スライドにまとめたものです。

## デッキ一覧

| No | 分野 | pptx | HTML(高精細) |
|----|------|------|------|
| 01 | 暗号・認証・PKI（PKCE/パスキー/OIDC/OCSP/mTLS/PQC） | `SC予想_01_暗号認証PKI.pptx` | `html/deck_01.html` |
| 02 | ネットワーク・クラウド・ゼロトラスト（SASE/SSE/ZTNA/DMARC/DNSSEC） | `SC予想_02_ネットワークゼロトラスト.pptx` | `html/deck_02.html` |
| 03 | Web/アプリケーション脆弱性（SQLi/XSS/CSRF/SSRF） | `SC予想_03_Webアプリ脆弱性.pptx` | `html/deck_03.html` |
| 04 | AIセキュリティ・LLM（OWASP LLM/PI/RAG/MITRE ATLAS） | `SC予想_04_AIセキュリティ.pptx` | `html/deck_04.html` |
| 05 | マルウェア・攻撃手法・IR（MITRE ATT&CK/ランサム/EDR-XDR） | `SC予想_05_攻撃手法IR.pptx` | `html/deck_05.html` |
| 06 | セキュリティマネジメント・法規（ISMS/個人情報/SBOM） | `SC予想_06_マネジメント法規.pptx` | `html/deck_06.html` |
| 07 | AI駆動型サイバー攻撃・フロンティアAI（自律型攻撃/防御・HITL） | `SC予想_07_AI駆動型攻撃.pptx` | `html/deck_07.html` |

## 形式について

- **pptx** は各スライドを画像として16:9に配置した「画像貼り付け型」（見た目の再現度を最優先。テキスト編集は不可）。
- **HTML** はブラウザで開くと最も高精細に表示されます（pptxの元データ）。
- 生成パイプライン: HTML → Chromium(headless)で各スライドを画像化 → python-pptx で16:9スライドに配置。

## 作成プロセス（マルチエージェント）

- 調査3 + 作問6 + 監修6 のワークフローで予想問題を作成（`../trend-analysis.md` 参照）。
- スライド化は、AIセキュリティ試作デッキをテンプレートに、6分野を並行エージェントでHTML生成。

> 本デッキはAIが過去問傾向・最新動向をもとに作成した**予想問題**です。実際の試験問題ではありません。正解・解説は最終確認を推奨します。
