# アセットマネジメント システム構成図

> 面接対策用のサンプル構成図。内部（フロント→ミドル→バック）と外部金融インフラ接続、横断セキュリティ基盤を1枚に。
> 画像版: `asset_mgmt_system_diagram.png` / 編集用ソース: `asset_mgmt_system_diagram.mmd`

```mermaid
flowchart TB
  classDef front fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
  classDef midback fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
  classDef ext fill:#fff3e0,stroke:#ef6c00,color:#e65100
  classDef sec fill:#fce4ec,stroke:#ad1457,color:#880e4f
  classDef crit fill:#ffcdd2,stroke:#c62828,color:#b71c1c

  subgraph INTERNAL["社内システム（運用・会計系）"]
    direction TB
    subgraph FRONT["フロントオフィス"]
      direction TB
      RES["リサーチ/市場データ・分析<br/>Bloomberg/Refinitiv/FactSet/MSCI"]
      PMS["PMS ポートフォリオ管理<br/>保有/リバランス/What-if"]
      RISK["事前リスク管理<br/>VaR・エクスポージャー<br/>Aladdin Risk/Barra"]
      COMP["事前コンプラチェック<br/>ガイドライン/禁止銘柄<br/>Charles River/Aladdin"]
      OMS["OMS 発注管理<br/>Aladdin/CRD/NRI T-STAR"]
      EMS["EMS 執行<br/>アルゴ/SOR/TCA<br/>EMSX/Triton"]
      RES --> PMS --> RISK --> COMP --> OMS --> EMS
    end
    subgraph MIDBACK["ミドル/バックオフィス"]
      direction TB
      MATCH["約定照合<br/>DTCC/Omgeo CTM・ALERT"]
      NAV["★NAV 基準価額計算★<br/>NRI T-STAR/SimCorp"]
      PERF["パフォーマンス測定<br/>アトリビューション"]
      ACCT["ファンド経理/GL<br/>SS&amp;C/SimCorp"]
      REP["規制・社内報告<br/>EDINET/運用報告書"]
      MATCH --> NAV --> PERF --> ACCT --> REP
    end
  end

  subgraph PLATFORM["全社横断 セキュリティ/IT基盤"]
    SEC["IAM・PAM / ゼロトラスト / EDR / SIEM・SOC / DLP / メール(BEC)対策 / BCP・DR"]
  end

  subgraph EXTERNAL["社外接続（外部金融インフラ）"]
    direction TB
    BROKER["ブローカー/取引所<br/>東証 arrowhead"]
    CUST["信託銀行/カストディ<br/>三菱UFJ信託/State Street/BNY"]
    SETTLE["国内決済<br/>JASDEC・ほふり/JSCC/日銀ネット"]
    DATA["市場データベンダー<br/>Bloomberg/LSEG/QUICK"]
    INDEX["指数提供<br/>MSCI/FTSE/TOPIX"]
    DIST["販売会社<br/>銀行/証券/ネット証券"]
    REG["規制当局<br/>金融庁/投信協会"]
    PROXY["議決権行使<br/>ISS/Glass Lewis"]
  end

  OMS --> MATCH
  EMS -- "FIX" --> BROKER
  MATCH -- "CTM/ALERT(SSI)" --> CUST
  CUST -- "SWIFT" --> SETTLE
  BROKER --> SETTLE
  DATA --> RES
  DATA --> NAV
  INDEX --> PMS
  NAV -- "基準価額配信" --> DIST
  REP --> REG
  PMS --> PROXY

  SEC -. "横断ガバナンス" .-> INTERNAL
  SEC -. "外部接続の監視/統制" .-> EXTERNAL

  class RES,PMS,RISK,COMP,OMS,EMS front
  class MATCH,PERF,ACCT,REP midback
  class NAV crit
  class BROKER,CUST,SETTLE,DATA,INDEX,DIST,REG,PROXY ext
  class SEC sec
```

## 凡例
- 🔵 **フロントオフィス**：投資判断〜発注〜執行（リサーチ→PMS→リスク→コンプラ→OMS→EMS）
- 🟢 **ミドル/バックオフィス**：約定照合→**NAV計算**→パフォーマンス→経理→報告
- 🔴 **NAV（基準価額計算）**＝生命線。停止＝取引停止、改ざん＝全投資家に不当価格
- 🟠 **社外接続**：FIX（発注）/ SWIFT（決済）/ CTM・ALERT（照合）/ データ・指数 / 販売会社 / 規制 / 議決権
- 🩷 **横断セキュリティ基盤**：IAM・PAM / ゼロトラスト / EDR / SIEM・SOC / DLP / BCP

## 主要な接続プロトコル
- **FIX** … EMS/OMS → ブローカー/取引所（発注・約定）
- **SWIFT** … カストディ/信託銀行 → 国内外決済（資金・証券決済指図）
- **CTM/ALERT(SSI)** … 約定照合・決済先口座情報
- **基準価額配信** … NAV → 販売会社 → 個人/法人顧客
