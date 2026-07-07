【過去問傾向】
# 情報処理安全確保支援士(SC)試験 分析レポート(2026年時点)

## (1) 最新の試験形式の要点
- 従来「午前I/午前II/午後」の3区分。2026年度(令和8年度)からCBT方式へ移行するが、出題形式・出題数・配点・合格基準は変更なし。
- **午前I**(科目A-1相当):四肢択一30問/90分。応用情報レベルの共通問題。高度試験・支援士の合格や午前I通過で最大2年間免除可。
- **午前II**(科目A-2相当):四肢択一25問/40分。セキュリティ専門(20問以上がセキュリティ、残りがネットワーク・DB・マネジメント等)。
- **午後**(科目B相当):記述式。4問中2問選択/150分。事例ベースの長文シナリオ。
- **合格基準**:各区分とも100点満点で60点以上(全区分クリアが条件)。
- **実施回数**:年2回。従来は春期(4月)・秋期(10月)。2026年度は移行に伴い「前期(2026年11月頃)」「後期(2027年2月頃)」の予定。

## (2) 午前II 定番論点リスト(20項目以上)
繰り返し問われる論点(令和3〜7年で頻出):
1. TLS(TLS1.3、DTLS、ハンドシェイク、IPsec/L2TPとの位置関係)
2. 公開鍵基盤PKI・電子証明書・CRL/OCSP運用
3. デジタル署名(XML署名、トランザクション署名、MAC/メッセージ認証符号)
4. ハッシュ関数(SHA-512/256、性質)
5. CRYPTREC暗号リスト・FIPS PUB 140-3
6. 耐量子計算機暗号PQC・情報理論的安全性(近年増加)
7. OAuth2.0・OpenID Connect・SAML(シングルサインオン)
8. 認証・認可・アカウンティングAAA(RADIUS/Diameter)、IEEE802.1X
9. メール認証(SPF/DKIM/DMARC)
10. DNSSEC・カミンスキー攻撃・ドメインフロンティング
11. DDoS/DRDoS(リフレクション・アンプ攻撃)、Mirai/ボットネット
12. Webアプリ攻撃(XSS、CSRF対策、OSコマンド/SQLインジェクション、クリックジャッキング、HSTS)
13. Pass the Hash、タイミング攻撃、クリプトジャッキング
14. AI関連攻撃(モデルインバージョン、敵対的サンプル)※新傾向
15. マルウェア動作・コネクトバック(接続外向き)通信
16. IPS/IDS・ステートフルパケットインスペクション・WAF
17. SOAR・UEBA・CSPM等の新しい防御技術
18. 脆弱性管理(CVSS、CVE、CWE、IoC/侵害指標、SBOM)
19. ISMS・JIS Q 27000用語定義・内部統制・システム監査
20. ISMAP(政府クラウド登録)・NISTサイバーセキュリティフレームワーク(CSF)
21. 証拠保全・フォレンジック(保全順序)
22. ネットワーク基礎(TCP/HTTPヘッダー、ICMP、サブネット、OSPF、HTTPステータスコード)
23. 非セキュリティ枠:DB設計・デザインパターン・TDD・サービスマネジメント

## (3) 午後(記述式)題材シナリオの傾向(令和5〜7年)
- **R5秋**:Webアプリ開発/セキュリティ対策見直し/CI(継続的インテグレーション)サービス/リスクアセスメント
- **R6春**:APIセキュリティ/サイバー攻撃対策/Webセキュリティ/Webアプリプログラム
- **R6秋**:インシデントレスポンス/ドメイン名変更・管理/クレジットカード情報漏えい対応/セキュリティ診断
- **R7春**:サプライチェーンのリスク対策/脆弱性管理/モバイルアプリ開発/IT資産管理
- **R7秋**:SaaS利用(コンサル業務)/暗号資産交換業のセキュリティ/情報システムのセキュリティ強化/製造業のセキュリティ管理

**傾向の要約**:
- 「Webアプリ/APIのセキュア開発」と「インシデント対応・脆弱性管理」が二大定番。
- クラウド/SaaS利用、サプライチェーン、IT資産管理など**運用・組織管理系**が増加。
- 業界特化シナリオ(クレジットカード=PCI DSS、暗号資産、製造業OT)が登場。
- 実務プロセス(証拠保全、脆弱性診断、リスクアセスメント)を問う設問が定着。

## (4) 今後出そうな空白テーマ(狙われうる領域)
- **生成AI/LLMのセキュリティ**:プロンプトインジェクション、RAGの情報漏えい、AI利用ガバナンス。
- **耐量子暗号(PQC)への移行**:CRYPTREC推奨更新、ハイブリッド鍵交換。午前IIで既出→午後展開の可能性。
- **クラウドネイティブ**:コンテナ/Kubernetes、IaC、CSPM/CWPP、ゼロトラスト(SASE・SSE)。
- **サプライチェーン深掘り**:SBOM運用、OSS依存の脆弱性(Log4j型)、ソフトウェア署名。
- **アイデンティティ**:パスキー/FIDO2・パスワードレス、Identity Proofing、条件付きアクセス。
- **OT/IoT・制御システム**:製造業シナリオの延長、産業プロトコル。
- **法規・制度**:改正個人情報保護法、経済安全保障、SBOM義務化、EDR/MDR運用委託。
- **ランサムウェア対応**:二重脅迫、バックアップ戦略、事業継続(BCP)との連携。

出典:
- [IPA 情報処理安全確保支援士試験](https://www.ipa.go.jp/shiken/kubun/sc.html)
- [IPA 令和8年度実施予定](https://www.ipa.go.jp/shiken/2026/ap_koudo_sc_yotei.html)
- [試験形式と合格基準｜sc-siken.com](https://www.sc-siken.com/sckeisiki.html)
- [sc-siken 令和7年秋](https://www.sc-siken.com/kakomon/07_aki/) / [令和7年春](https://www.sc-siken.com/kakomon/07_haru/) / [令和6年秋](https://www.sc-siken.com/kakomon/06_aki/) / [令和6年春](https://www.sc-siken.com/kakomon/06_haru/) / [令和5年秋](https://www.sc-siken.com/kakomon/05_aki/)

【AIセキュリティ】
SC試験「AIセキュリティ」出題予測のための論点整理(15項目以上)を以下にまとめます。調査材料はOWASP Top 10 for LLM Applications 2025、AI特有攻撃、国内外ガイドラインです。

---

## A. OWASP Top 10 for LLM Applications 2025 系(用語×対策)

1. **プロンプトインジェクション(LLM01)**
   午前II: 「指示とデータを同一チャネルで処理する性質を突く攻撃」の定義選択。午後: ユーザ入力を検証せずシステムプロンプトへ連結する構成の脆弱性指摘と、入力/出力の分離・権限最小化の対策記述。

2. **直接 vs 間接プロンプトインジェクション**
   午前II: 「外部Webページやメール本文に埋め込んだ指示をLLMが実行」=間接、という区別の4択。午後: RAGで取り込んだ外部文書に不可視の指示が仕込まれた事例のリスク分析。

3. **機密情報漏えい(LLM02)/システムプロンプトリーク(LLM07)**
   午前II: 「プロンプトリーク」「システムプロンプト漏えい」の用語定義。午後: 学習データや会話履歴に含まれるPIIが応答に出力される経路と、マスキング・データ最小化の記述。

4. **サプライチェーン(LLM03)**
   午前II: 「サードパーティ製モデル/LoRA/データセットの汚染」を選ぶ問題。午後: 外部公開モデルやライブラリの出所検証(SBOM、署名、来歴確認)の必要性を記述。

5. **データ汚染/モデル汚染(データポイズニング)(LLM04)**
   午前II: 「学習データに悪意あるサンプルを混入しモデル挙動を操作」=ポイズニングの定義選択。午後: 学習パイプラインの完全性確保、データ検証、バックドア検知の対策。

6. **不適切な出力処理(Improper Output Handling)(LLM05)**
   午前II: 「LLM出力を無検証で下流に渡す」=XSS/SSRF/コード実行への連鎖、という4択。午後: LLM出力を信頼境界の外側として扱い、エスケープ・サニタイズする設計を記述(既存Webセキュリティ知識との接続点で狙われやすい)。

7. **過剰な代理権限(Excessive Agency)(LLM06)/AIエージェント**
   午前II: 「AIエージェントに過大な権限・ツール・自律性を与えた結果の被害」を選ぶ。午後: 最小権限、ツール実行前の人間承認(human-in-the-loop)、操作範囲の制限を記述。エージェント時代の目玉になりやすい論点。

8. **ベクトル/埋め込みの脆弱性(LLM08)/RAG情報漏えい**
   午前II: 「ベクトルDBのアクセス制御不備で他テナントの文書が検索される」等の選択。午後: RAGにおけるテナント分離、埋め込みからの元データ復元リスク、検索結果の権限フィルタリング。

9. **誤情報/ハルシネーション(Misinformation)(LLM09)**
   午前II: 「ハルシネーション」「ファクトチェック」「過度の依存(overreliance)」の用語定義。午後: 出力の根拠提示・検証プロセス・利用者への注意喚起という統制記述。

10. **リソース枯渇(Unbounded Consumption)(LLM10)**
    午前II: 「大量・長大な推論要求によるDoS/コスト増/モデル窃取」の選択。午後: レート制限、トークン上限、コスト監視の対策記述(従来のDoS対策の応用として問いやすい)。

---

## B. AIシステム特有の攻撃(単独用語として午前IIで頻出化しやすい)

11. **ジェイルブレイク(脱獄, Jail Break)**
    午前II: 「ガードレール/安全機構を回避させ禁止された出力を引き出す」の定義選択。ガードレールとセットで問われる。

12. **敵対的サンプル(Adversarial Example)/回避攻撃(Evasion Attack)**
    午前II: 「人間には気づかない微小な摂動で分類器を誤認識させる」=敵対的サンプル、の定義。画像認識/マルウェア検知の文脈で4択化しやすい。

13. **モデル反転(Model Inversion)/メンバーシップ推論**
    午前II: 「出力から学習データや個人情報を復元する攻撃」=モデルインバージョン、の選択。プライバシー漏えいの一種として問われる。

14. **モデル抽出/モデル窃取(Model Extraction/Stealing)**
    午前II: 「APIへの大量クエリで内部モデルを複製する攻撃」の定義選択。LLM10やAPI認証・レート制限と絡めやすい。

15. **ディープフェイク**
    午前II: 生成AIによる偽コンテンツの用語・悪用(なりすまし、BEC、フェイクニュース)の選択。午後: 本人確認・多要素認証・検知の文脈で登場。

16. **ガードレール/システムプロンプト/マルチモーダル(基礎用語群)**
    午前II: これら生成AI基礎用語の定義を素直に問う4択(SC過去問系サイトが既に収録)。

---

## C. ガイドライン・規制・フレームワーク(制度知識として午前II、午後の助言記述で活用)

17. **NIST AI RMF**
    午前II: 「GOVERN/MAP/MEASURE/MANAGE の4機能でAIリスクを管理」=AI RMF、の選択。従来のNIST CSF(Identify等)との対比で狙われやすい。

18. **MITRE ATLAS**
    午前II: 「ATT&CKのAI版で、AIシステムへの攻撃戦術・技法を体系化」=ATLAS、の定義選択。Reconnaissance/Initial Access/Exfiltration等の戦術名で。

19. **AI事業者ガイドライン(総務省・経済産業省)**
    午前II: 「AI開発者/AI提供者/AI利用者の3主体区分」と10原則の知識選択。午後: 組織のAI利用ポリシー策定・体制整備の助言記述の根拠として。

20. **ISO/IEC 42001(AIマネジメントシステム)/EU AI Act**
    午前II: 「AIMSの認証規格」=ISO/IEC 42001、EUのリスクベース規制=AI Act、の選択。ISMS(27001)との対比で問いやすい。

21. **IPA/国内動向(補足)**
    午前II: IPA公表の生成AI利用時のセキュリティ注意点(社内データ入力による漏えい、シャドーAI)を組織統制の文脈で。午後: 従業員の生成AI利用ガバナンス(利用範囲・入力禁止情報の規程化)。

---

## 出題形式の傾向予測(まとめ)

- **午前II(4択)**: 上記の「用語の定義当て」が最有力(プロンプトインジェクション、ジェイルブレイク、データポイズニング、敵対的サンプル、モデルインバージョン、回避攻撃、ハルシネーション、ATLAS、AI RMF、ISO/IEC 42001)。SC過去問系サイトが既にこれら用語群を収録済みで、単問化されやすい。
- **午後(記述)**: 既存Webセキュリティ知識と接続する **LLM05(出力処理→XSS/SSRF連鎖)**、**LLM06(エージェント過剰権限→最小権限・人間承認)**、**LLM08/RAG(テナント分離・アクセス制御)**、**LLM02(機密漏えい→データ最小化)** が、シナリオ問題(社内チャットボット/RAG導入)に組み込みやすく最有力。対策記述では「入力検証」「出力を信頼境界外扱い」「最小権限」「human-in-the-loop」「レート制限」「データ最小化・マスキング」が定番解答語彙になる見込み。

主要ソース: [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) / [OWASP LLM10 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) / [SC過去問 生成AI関連用語](https://sc-kakomon.com/?p=291) / [IPA SC試験](https://www.ipa.go.jp/shiken/kubun/sc.html) / [AI事業者ガイドライン(経産省)](https://www.meti.go.jp/shingikai/mono_info_service/ai_shakai_jisso/pdf/20250328_2.pdf) / [NIST AI RMF(デロイト解説)](https://www.deloitte.com/jp/ja/services/consulting/perspectives/nist-ai-rmf.html) / [MITRE ATLAS(Vectra)](https://www.vectra.ai/topics/mitre-atlas)

【ホットトピック】
# SC試験2026 頻出テーマ整理(核心ポイント)

## 1. MITRE ATT&CK フレームワーク(最重要・厚めに)

利用者の言う「ミュトス」はほぼ確実に **MITRE ATT&CK(マイター・アタック)** のこと。「MITRE(マイター)」の空耳と思われます。

### 基本概念
- **実在の攻撃を観測して体系化したナレッジベース**。攻撃者の「振る舞い(behavior/TTP)」を軸にする点が核心。IPやハッシュなど個別IOCではなく、抽象度の高い「やり口」を分類する。
- **TTP** = Tactics(戦術=攻撃者の目的・What)、Techniques(技術=目的達成の手段・How)、Procedures(手順=具体的な実装)。マトリクスは**列=戦術、セル=技術、その下=サブ技術**という2次元構造。
- **T番号**で識別。技術は「T1566」、サブ技術は「T1566.001(スピアフィッシング添付ファイル)」のようにドット付き。戦術はTA番号(例: Initial Access=TA0001)。
- Enterprise マトリクス(2025年時点)は**15戦術・222技術・475サブ技術**規模。対象はWindows/macOS/Linuxに加え**クラウド(AWS/Azure/GCP/M365/Entra ID)・SaaS・ネットワーク機器・コンテナ**まで拡張。他にMobile、ICS(制御システム)マトリクスがある。

### 主要な戦術(順序を問われやすい・言える様に)
初期アクセス(Initial Access) → 実行(Execution) → 永続化(Persistence) → 権限昇格(Privilege Escalation) → 防御回避(Defense Evasion) → 認証情報アクセス(Credential Access) → 探索(Discovery) → 水平展開/横展開(Lateral Movement) → 収集(Collection) → C2(Command and Control) → 持ち出し(Exfiltration) → 影響(Impact)。※先頭に偵察(Reconnaissance)・リソース開発(Resource Development)が加わり全体で14〜15戦術。

### 構成要素(用語として問われる)
- **Groups**: 攻撃者グループ(APTなど、G番号)。**Software**: マルウェア/正規ツール(S番号)。**Mitigations**: 緩和策(M番号)。**Data Sources / Data Components**: 検知に必要なログ源。
- ナレッジベースの改訂で従来の「Detections」欄が **Detection Strategies / Analytics / Data Components** に再構造化され、検知の精緻化が進んでいる。

### サイバーキルチェーンとの違い(頻出の対比)
- **サイバーキルチェーン(Lockheed Martin)** = 偵察→武器化→デリバリ→エクスプロイト→インストール→C2→目的実行の**直線的7段階モデル**。経営層説明・全体像整理向き。
- **ATT&CK** = 順序モデルではなく**攻撃手法の網羅的な辞書/マトリクス**。脅威ハンティング、検知ルール(SIEM/EDR)設計、製品評価に使う実務向き。「線」がキルチェーン、「面(網羅)」がATT&CK、と整理すると良い。

### 関連フレームワーク(用語区別)
- **D3FEND**: ATT&CKの各技術に対応する**防御側**の対策をマッピングしたナレッジベース(攻撃=ATT&CK、防御=D3FEND)。
- **CAR(Cyber Analytics Repository)**: 技術検知のための分析(アナリティクス)集。
- **ATT&CK Navigator**: マトリクス上でカバレッジや検知の空白(ギャップ)を色分け可視化するツール。

### 試験での問われ方(答案の書き方)
- 記述で**「攻撃段階 → 検知 → 封じ込め」をATT&CKで筋道立てる**問題が想定される。「どの技術(T番号/技術名)に該当し、どのログ(Data Source)で検知し、どのMitigationで防ぐか」を書けるように。
- 例: フィッシング(Initial Access/T1566)→ 不正ログイン(Valid Accounts)→ 認証情報ダンプ(Credential Access, LSASS)→ 横展開(RDP/PsExec)→ ランサム暗号化(Impact/Data Encrypted for Impact)、という物語をT番号で再構成する練習。
- **カバレッジ評価・検知ギャップの特定・SOC成熟度評価・レッドチーム/パープルチームの共通言語**という活用目的を答えられること。

## 2. 認証・アクセス制御(ゼロトラスト系)

### ゼロトラスト / SASE / SSE
- **ゼロトラスト**: 「決して信頼せず常に検証(Never Trust, Always Verify)」。境界防御(ペリメタ)から脱却し、**すべてのアクセスを都度認証・認可、最小権限、継続的監視**。NIST SP 800-207が基盤(PDP/PEP=ポリシー決定点/実施点)。
- **SASE**: ネットワーク(SD-WAN)+セキュリティをクラウドで統合。構成要素の**SWG / CASB / ZTNA / FWaaS**を言えること。
- **SSE**: SASEからネットワーク(SD-WAN)を除いた**セキュリティ部分(SWG/CASB/ZTNA)**の総称。SASE=SD-WAN+SSE という関係。
- **ZTNA**: VPNの代替。アプリ単位でアクセス許可し、社内ネット全体を晒さない(VPNの過剰な信頼範囲問題を解決)。

### パスキー / FIDO2 / WebAuthn(頻出・仕組みを正確に)
- **公開鍵暗号ベースのパスワードレス認証**。秘密鍵は認証器(デバイス)内に保持し外に出ない → **サーバ側漏洩・フィッシング・リプレイに耐性**。
- **FIDO2 = WebAuthn + CTAP2**。WebAuthnは「ブラウザ↔RP(サーバ)」のW3C API仕様、CTAP2は「PC/ブラウザ↔認証器」の通信仕様。
- **フィッシング耐性の原理**: 署名時にオリジン(ドメイン)を検証するため、偽サイトでは認証が成立しない。チャレンジ・レスポンスで署名を検証。
- **パスキー**は秘密鍵をクラウド経由でデバイス間**同期(synced passkey)**できるようにしたもの(vs. デバイス固定のdevice-bound)。UX向上と可用性が利点。

### OAuth 2.0 / OIDC / mTLS(認証と認可の区別が核心)
- **OAuth 2.0 = 認可(アクセス権の委譲)**、**OIDC = OAuth2.0上に構築した認証**(IDトークン=JWTで「誰か」を伝える)。この違いは頻出。
- **認可コードフロー + PKCE** が現在の推奨。**PKCE**は認可コード横取り攻撃対策で、`code_verifier`(43〜128文字の高エントロピー乱数)と、そのハッシュである`code_challenge`を使い、正規クライアントのみがトークン交換できることを証明する。
- JWTの検証(署名・iss/aud/exp)、JWKSによる公開鍵配布、リフレッシュトークン、スコープ、暗黙(Implicit)フローが非推奨になった理由も押さえる。
- **mTLS(相互TLS)**: クライアント・サーバ双方が証明書を提示して相互認証。ゼロトラストのサービス間通信やAPI保護、証明書バインドトークンに利用。

## 3. サプライチェーン攻撃 / SBOM / ソフトウェア署名

- **サプライチェーン攻撃**: 取引先・OSS依存・ソフト更新経路など「弱い環」を経由した侵害(例: SolarWinds、OSSのtyposquatting、ビルド環境汚染)。
- **SBOM(Software Bill of Materials)**: ソフト構成部品の一覧。**脆弱性(例: Log4j)発覚時に影響範囲を即座に特定**でき、依存関係を可視化。主要フォーマットは**SPDX(ライセンス管理向き)**と**CycloneDX(セキュリティ向き)**。生成ツールにSyft/Trivy、管理にOWASP Dependency-Track。
- 動向: 米大統領令でSBOM連邦義務化、日本は経産省「SBOM導入手引」、2025年に日米CISA主導で**15か国が国際共同ガイダンスに署名**。義務化の潮流。
- **ソフトウェア署名 / 完全性**: **Sigstore/cosign** でSBOMや成果物に署名し改ざん検知。ビルド由来の保証枠組み **SLSA(サプライチェーンの整合性レベル)** も押さえる。

## 4. ランサムウェア / EDR・XDR / SOC

- **多重脅迫**: ①暗号化 ②暗号化+**データ窃取・暴露(二重脅迫)** ③さらに**DDoSや関係者への連絡(三重・四重)**。バックアップ破壊も定石で、**イミュータブル(改変不可)バックアップ・3-2-1・オフライン保管**が対策。
- **RaaS(Ransomware as a Service)**、初期侵入ブローカー(IAB)の分業化。
- **EDR**: エンドポイントの挙動を監視し初期段階で検知・対応。**XDR**: EDRをエンドポイント外(ネットワーク/クラウド/メール/ID)へ拡張し横断的に相関分析。**MDR**: それを運用代行するサービス。
- **SOC**: 監視・検知・対応の中枢。**SIEM**(ログ相関)、**SOAR**(対応自動化)との関係、EDR/XDRとの連携を整理。

## 5. クラウドセキュリティ(IAM / 設定ミス / コンテナ・K8s)

- **設定ミス(Misconfiguration)がクラウド最大のリスク**。S3公開設定、過剰権限。**責任共有モデル**の理解が前提。
- **IAM**: **最小権限の原則、MFA強制、長期アクセスキーの棚卸し・無効化、一時的認証情報(STS等)の利用**。放置された特権IDの乗っ取りが被害を拡大。
- **コンテナ/Kubernetes**: イメージ脆弱性スキャン、シークレット管理、ネットワークポリシー、ランタイムでの不審プロセス/通信のリアルタイム監視。
- **CSPM**(設定ミス検出)/**CWPP**(ワークロード保護)/**CNAPP**(両者統合)の役割区別。

## 6. メールセキュリティ(送信ドメイン認証)

- **SPF**: 送信元IPをDNSに登録して正当性を確認(「このIPから送ってよい」の許可証)。**エンベロープFrom**を検証。
- **DKIM**: 送信側が**秘密鍵で電子署名**、受信側がDNS公開鍵で検証 → **改ざん検知と送信ドメインの正当性**。
- **DMARC**: SPF/DKIMの結果と**ヘッダFromの一致(アライメント)**を検証。ポリシーは **none(監視)→ quarantine(隔離)→ reject(拒否)** の3段階。**集計(rua)/失敗(ruf)レポート**で運用改善。
- **BIMI**: DMARCを quarantine以上で運用しているドメインに、メールクライアント上で**ブランドロゴ**を表示(VMC証明書が必要)。なりすまし抑止+ブランド訴求。Gmail/Yahoo/Apple対応。
- 動向: **Google/Yahooの送信者要件**で、大量送信(5,000通/日超)はSPF+DKIM+DMARC必須化。ワンクリック購読解除も要件。

---

## 主な参照元
- MITRE ATT&CK: [NTTデータ先端技術](https://www.intellilink.co.jp/article/column/attack-mitre-sec01.html) / [Splunk](https://www.splunk.com/ja_jp/data-insider/what-is-the-mitre-att-and-ck-framework.html) / [MITRE公式マトリクス](https://attack.mitre.org/matrices/enterprise/) / [Palo Alto](https://www.paloaltonetworks.com/cyberpedia/what-is-mitre-attack) / [キルチェーン比較(東京都)](https://cybersecurity-taisaku.metro.tokyo.lg.jp/know_more/cyberkillchain-mitreattck/)
- ゼロトラスト/SASE/SSE: [LAC WATCH](https://www.lac.co.jp/lacwatch/service/20230605_003401.html) / [Zscaler](https://www.zscaler.com/products-and-solutions/secure-access-service-edge-sase)
- パスキー/FIDO2/WebAuthn: [IP3導入ガイド](https://ip3.co.jp/guide/8294/) / [CAPY解説](https://corp.capy.me/blog/passkey/)
- OAuth/OIDC/PKCE: [zenn シーケンス図](https://zenn.dev/zaki_yama/articles/oauth2-authorization-code-grant-and-pkce) / [ONE CAREER Tech](https://note.com/dev_onecareer/n/nc60183573565)
- SBOM/署名: [経産省 国際ガイダンス署名](https://www.meti.go.jp/press/2025/09/20250904001/20250904001.html) / [Guardian SBOM解説](https://guardian.jpn.com/security/cloud-supply/supply-chain/column/technical/sbom/)
- ランサム/EDR/XDR/クラウド: [iret 2026提言](https://iret.media/184166) / [Cybereason CNAPP](https://www.cybereason.co.jp/blog/cnapp/13678/)
- メール認証: [IIJ 送信ドメイン認証](https://ent.iij.ad.jp/articles/172/) / [PwC DMARC/BIMI](https://www.pwc.com/jp/ja/knowledge/column/awareness-cyber-security/dmarc-bimi.html)