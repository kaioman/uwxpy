# Gemini CLI - Project Guidelines (uwxpy)

このプロジェクト(`uwxpy`)における開発ガイドライン、命名規則、および「このプロジェクトらしい」実装方法をまとめます。
AIアシスタントは本プロジェクト内のコードを編集・生成する際、このガイドラインに厳密に従ってください。

## 1. 技術スタック

* **言語**: Python 3.8以上
* **主要パッケージ**:
  * `tweepy`: X (旧Twitter) API v2 および API v1.1 連携用
  * `libcore-hng`: 共通ユーティリティ (ロギングなど)
  * `pycorex`: 共通コアモジュール・ユーティリティ
* **外部API / AIモデル**:
  * **Uwgen API**: AI画像生成
  * **Gemini API / Vertex AI**: プロンプト解析・動的生成・最適化
  * **X (Twitter)**: 生成したAI画像の投稿

## 2. 命名規則

Pythonの標準的なPEP 8に準拠しつつ、以下の規則を徹底してください。

* **クラス名**: PascalCase (`XClient`, `BasePromptService`, `GeneratePrompt` など)
* **関数名・メソッド名**: snake_case (`tweet_with_media`, `upload_media`, `init_app` など)
* **変数名・属性名・引数名**: snake_case (`media_bytes`, `tweet_id`, `prompt_request` など)
* **ファイル名・ディレクトリ名**: snake_case (`x_client.py`, `base_prompt_service.py` など)
* **非公開（プライベート）メソッド**: プレフィックスに単一のアンダースコア `_` を付与 (`_load_json` など)

## 3. 「このプロジェクトらしい」実装方法（Idiomatic Guidelines）

### 3.1. 設定（Configuration）と機密情報の管理

**【重要】 `.env` ファイルは使用・読み込みしないでください。**

* 設定値やシークレット（APIキーなど）は、JSON形式の設定ファイル (`configs/uwxpy.json` 等) で管理されています。（※構造の参考が必要な場合は `configs/uwxpy.sample.json` を確認してください）
* コード内から設定値へアクセスする場合は、`uwxpy.configs.app_init`（または `pycorex.configs.app_init`）を使用して初期化された `app` オブジェクトの階層構造経由で行います。
  * 例: `app.core.config.x_api.consumer_key`

### 3.2. ロギング (Logging)

* 標準の `print()` や標準 `logging` モジュールの直接呼び出しは避け、必ず `libcore_hng.utils.app_logger` を使用してログを出力してください。
  * 実装例:

    ```python
    import libcore_hng.utils.app_logger as app_logger
    app_logger.info(f"Tweet successfully posted. tweet_id={tweet_id}")
    ```

### 3.3. 型アノテーション (Type Hints)

* すべての関数・メソッドの引数と戻り値には、必ず型アノテーションを記述してください。
  * 例: `def tweet(self, text: str, media_ids: list[str] | None = None) -> TweetResult:`
* 戻り値の型には、独自のデータクラスやモデル (`TweetResult` など) を積極的に利用し、インターフェースを明確にしてください。

### 3.4. 例外処理 (Error Handling)

* サードパーティライブラリ（`tweepy`など）から送出される例外は直接上位に伝搬させず、モジュールごとの独自例外クラス（例: `XApiError`）でラップしてから送出（`raise`）するようにしてください。

### 3.5. ドキュメンテーション (Docstrings)

* クラス、メソッド、関数には必ずトリプルクォート `"""` を用いた docstring（日本語）を記述してください。
* パラメータの記述が必要な場合は、既存の実装に合わせて分かりやすく記述してください。

#### Python DocString Standard

PythonのDocStringを生成・修正する場合は、必ず以下の **NumPyスタイル** を遵守してください。Googleスタイル（Args: / Returns:）は使用禁止です。

#### 構成ルール

1. 概要（Summary）を1行目に記述。
1. `Parameters` セクション：

* ヘッダーの下に `----------`（ハイフン10個）を引く。
* `引数名 : 型` の形式で記述。
* 次の行にインデントして説明を記述。

1. `Returns` セクション：

* ヘッダーの下に `--------`（ハイフン8個）を引く。
* `型` を記述し、次の行に説明を記述。

#### 正解例（Example）

```Markdown
設定をJSONから読み込む

Parameters
----------
abs_path : str
    JSONファイル相対パス

Returns
--------
str
    JSON文字列
```
