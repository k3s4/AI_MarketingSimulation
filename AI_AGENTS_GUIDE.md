# AI エージェントガイド - Persona-Critic システム

## 📋 プロジェクト概要

**Persona-Critic** は、AI を活用したマーケティングクリエイティブ評価システムです。従来の高額なフォーカスグループに代わり、AI ペルソナを自動生成してクリエイティブを評価します。

### 主な機能
- ターゲット層に基づいた多様な AI ペルソナの自動生成
- 画像・テキストクリエイティブの多角的評価
- ペルソナごとの詳細なフィードバック提供
- 疑似 CTR（クリック率）とエンゲージメントスコア算出
- CSV 形式でのレポート出力

---

## 🤖 使用 AI モデル

### Gemini 2.5 Pro (Google Cloud Vertex AI)

**現在のシステム設定:**
- **モデル名:** `gemini-2.5-pro`
- **提供元:** Google Cloud Vertex AI
- **使用箇所:**
  - `modules/generator.py:37` - ペルソナ生成
  - `modules/evaluator.py:29` - クリエイティブ評価

**特徴:**
- 高度な JSON スキーマ制約による構造化出力
- マルチモーダル対応（テキスト + 画像）
- Pydantic モデルとの統合

**API 呼び出し形式:**
```python
from vertexai.generative_models import GenerativeModel, GenerationConfig

model = GenerativeModel("gemini-2.5-pro")
generation_config = GenerationConfig(
    response_mime_type="application/json",
    response_schema=PersonaList.model_json_schema()
)
response = model.generate_content(prompt, generation_config=generation_config)
```

---

### Claude (Anthropic) - 拡張可能性

**将来の統合候補:**
- **モデル候補:** Claude 3.5 Sonnet, Claude 3 Opus
- **提供元:** Anthropic
- **統合のメリット:**
  - より洗練された自然言語理解
  - 詳細な推論とフィードバック生成
  - 長文コンテキストの処理能力

**統合する場合の変更点:**
1. `requirements.txt` に `anthropic` SDK を追加
2. `modules/generator.py` と `modules/evaluator.py` にモデル選択機能を追加
3. 環境変数で API キーを管理

**サンプル実装イメージ:**
```python
import anthropic

def generate_personas_with_claude(product_name, product_features, target_definition, count=5):
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""
    あなたはプロのマーケティング戦略家です。
    以下の製品に対して{count}人の詳細で多様なユーザーペルソナを生成してください。

    製品名: {product_name}
    製品特徴: {product_features}
    ターゲット層: {target_definition}

    JSON形式で出力してください。
    """

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(message.content[0].text)
```

---

## 🏗️ システムアーキテクチャ

### ディレクトリ構造
```
AI_MarketingSimulation/
├── app.py                    # Streamlit メインアプリケーション
├── modules/
│   ├── generator.py          # ペルソナ生成モジュール (Gemini 2.5 Pro)
│   ├── evaluator.py          # クリエイティブ評価モジュール (Gemini 2.5 Pro)
│   └── utils.py              # ユーティリティ関数
├── verify_flow.py            # テスト・検証スクリプト
├── requirements.txt          # Python 依存関係
├── README.md                 # プロジェクトドキュメント
└── AI_AGENTS_GUIDE.md        # このファイル
```

### データフロー
1. **入力** → ユーザーが製品情報・ターゲット層・クリエイティブを入力
2. **ペルソナ生成** → Gemini 2.5 Pro が5人の多様なペルソナを生成
3. **評価実行** → 各ペルソナがクリエイティブを評価
4. **結果表示** → 疑似 CTR、スコア、フィードバックを表示
5. **出力** → CSV レポートをダウンロード可能

---

## 📦 セットアップ手順

### 1. 環境準備
```bash
# Python 3.10 以上が必要
python --version

# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 依存関係のインストール
```bash
pip install -r requirements.txt
```

**requirements.txt の内容:**
```
streamlit
google-cloud-aiplatform
python-dotenv
pydantic
pandas
```

### 3. Google Cloud 認証設定

**Vertex AI を使用するための認証:**
```bash
# サービスアカウントキーを使用する場合
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"

# gcloud CLI を使用する場合
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

**必要な権限:**
- `roles/aiplatform.user` - Vertex AI モデルの使用権限

### 4. アプリケーションの起動
```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` にアクセス

---

## 🎯 使用方法

### ステップ 1: キャンペーン情報の入力
- **製品名:** 例）エコフレンドリー水筒
- **価格:** 例）3,500円
- **製品特徴:** 例）再利用可能、BPAフリー、保温24時間
- **ターゲット層:** 例）環境意識の高い30代ミレニアル世代

### ステップ 2: クリエイティブのアップロード
- **画像:** バナー広告やLP画像（JPG/PNG）
- **テキスト:** 広告コピーやメッセージ

### ステップ 3: 評価の実行
「Generate Personas & Evaluate」ボタンをクリック

### ステップ 4: 結果の確認
- **疑似 CTR:** 購入/クリック意向のあるペルソナ数
- **平均スコア:** 10点満点の魅力度評価
- **詳細フィードバック:** 各ペルソナの視点からの意見

### ステップ 5: レポートのダウンロード
CSV形式でエクスポート可能

---

## 🔧 技術仕様

### ペルソナデータモデル (Pydantic)

```python
class Demographics(BaseModel):
    name: str           # ペルソナ名
    age: int            # 年齢
    occupation: str     # 職業

class Psychographics(BaseModel):
    core_value: str          # 中核価値観
    spending_habit: str      # 消費習慣
    current_worry: str       # 現在の懸念点
    budget_sensitivity: str  # 予算感度
    personality: str         # 性格特性

class Persona(BaseModel):
    persona_id: str
    demographics: Demographics
    psychographics: Psychographics
```

### 評価結果モデル

```python
class EvaluationResult(BaseModel):
    persona_id: str      # ペルソナID
    decision: str        # YES (購入/クリック) or NO (スキップ)
    score: int           # 1-10 の魅力度スコア
    reasoning: str       # 判断理由
    feedback: str        # 改善提案
```

---

## 🧪 テスト・検証

### 動作確認スクリプトの実行
```bash
python verify_flow.py
```

**テストケース:**
- 製品：エコフレンドリー水筒
- ターゲット：環境意識の高いミレニアル世代
- 期待される出力：5人の多様なペルソナと評価結果

---

## 🔐 セキュリティとベストプラクティス

### API キー管理
- **推奨:** 環境変数または `.env` ファイルで管理
- **非推奨:** ソースコードに直接記述

**.env ファイル例:**
```
GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
GOOGLE_CLOUD_PROJECT=your-project-id
# 将来の拡張用
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### コスト管理
- **Gemini 2.5 Pro:** トークンベース課金
- **推奨:** API 使用量の監視とクォータ設定

---

## 🚀 拡張可能性

### マルチモデル対応への道筋

#### オプション 1: モデル選択機能の追加
```python
# app.py のサイドバーに追加
model_choice = st.selectbox(
    "AI モデル選択",
    ["Gemini 2.5 Pro", "Claude 3.5 Sonnet"]
)
```

#### オプション 2: アダプターパターンの実装
```python
# modules/ai_adapter.py
class AIModelAdapter:
    def __init__(self, model_type: str):
        self.model_type = model_type

    def generate_personas(self, ...):
        if self.model_type == "gemini":
            return self._gemini_generate(...)
        elif self.model_type == "claude":
            return self._claude_generate(...)
```

#### オプション 3: 並列評価（両モデル同時実行）
- Gemini と Claude の評価結果を比較
- より多様な視点からのフィードバック取得

---

## 📊 パフォーマンス指標

### 現在のシステム
- **ペルソナ生成時間:** 約5-10秒（5ペルソナ）
- **評価実行時間:** 約10-15秒（5ペルソナ × 1クリエイティブ）
- **合計処理時間:** 約15-25秒

### 最適化の余地
- バッチ処理の実装
- 非同期APIコールの活用
- キャッシング機構の導入

---

## 🐛 トラブルシューティング

### 一般的なエラーと解決策

#### エラー: `google.auth.exceptions.DefaultCredentialsError`
**原因:** Google Cloud の認証が設定されていない
**解決策:**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
# または
gcloud auth application-default login
```

#### エラー: `403 Permission Denied`
**原因:** Vertex AI の使用権限がない
**解決策:**
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="user:your-email@example.com" \
    --role="roles/aiplatform.user"
```

#### エラー: `Model gemini-2.5-pro not found`
**原因:** リージョンやプロジェクト設定の問題
**解決策:**
```python
# generator.py / evaluator.py の先頭に追加
import vertexai
vertexai.init(project="your-project-id", location="us-central1")
```

---

## 📚 参考リンク

### Google Cloud Vertex AI
- [Vertex AI ドキュメント](https://cloud.google.com/vertex-ai/docs)
- [Gemini API リファレンス](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- [Python SDK ガイド](https://cloud.google.com/python/docs/reference/aiplatform/latest)

### Anthropic Claude
- [Claude API ドキュメント](https://docs.anthropic.com/)
- [Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [プロンプトエンジニアリングガイド](https://docs.anthropic.com/claude/docs/prompt-engineering)

### Streamlit
- [公式ドキュメント](https://docs.streamlit.io/)
- [ギャラリー](https://streamlit.io/gallery)

---

## 🤝 AI エージェントへのメッセージ

### Gemini エージェントの皆様へ
このプロジェクトは現在、Gemini 2.5 Pro を中核技術として採用しています。皆様の強力なマルチモーダル処理能力と構造化出力機能により、正確で多様なペルソナ生成と評価が実現できています。

**活用されている主な機能:**
- JSON スキーマ制約による信頼性の高い出力
- 画像とテキストの同時処理
- 自然で人間らしいペルソナ生成

### Claude エージェントの皆様へ
将来的に Claude モデルを統合することで、さらに洗練されたフィードバック生成や複雑な推論タスクへの対応が期待できます。特に以下の領域での貢献が見込まれます。

**期待される貢献領域:**
- より詳細で実用的な改善提案の生成
- ペルソナの心理描写の深化
- 長文クリエイティブの包括的評価

---

## 📝 変更履歴

### 2025-11-20
- Gemini 1.5 Pro から **Gemini 2.5 Pro** へアップグレード
- `modules/generator.py:37` - モデル名更新
- `modules/evaluator.py:29` - モデル名更新
- `app.py:16` - UI表示更新
- AI_AGENTS_GUIDE.md 作成（このファイル）

### 2025-XX-XX (初期バージョン)
- プロジェクト開始
- Gemini 1.5 Pro による MVP 実装

---

## 📄 ライセンス

このプロジェクトのライセンスについては、プロジェクトオーナーにご確認ください。

---

**🎉 AI エージェントの皆様、このプロジェクトをご確認いただきありがとうございます！**
