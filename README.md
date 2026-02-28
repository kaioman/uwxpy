# uwxpy

Uwgen API、Gemini Vision、Tweepyを使用して、AI生成画像をX（旧Twitter）に投稿・編集するPythonツールキット。

**日本語 | [English](README.en.md)**

## 概要

uwxpyは、AI画像生成、プロンプト最適化、X（旧Twitter）への自動投稿ワークフローを効率化するために設計されたPythonライブラリです。Uwgen APIで画像生成、Gemini Visionでプロンプト分析・生成、Tweepyで投稿管理を統合します。

## 主な機能

- **AI画像生成**: Uwgen APIを使用した高品質なAIアート作成
- **プロンプト最適化**: Geminiモデルを活用した動的プロンプト生成・編集
- **X（Twitter）統合**: Tweepyを使用した簡単投稿機能
- **構造化設定**: JSONファイルによる柔軟な設定管理

## 必要環境

- Python 3.8以上
- libcore-hng
- pycorex
- tweepy

## インストール

PyPIで利用可能な場合はpipで、またはソースから直接インストールできます：

```bash
git clone https://github.com/kaioman/uwxpy.git
cd uwxpy
pip install .
```

## セットアップ

ツールキットを実行する前に、設定ファイルを準備してください。サンプル設定はconfigs/uwxpy.sample.jsonにあります。

1. configs/uwxpy.sample.jsonをconfigs/uwxpy.jsonにコピーします
2. APIキーとアプリケーション設定を入力します

## クイックスタート

アプリケーション初期化と基本的な使用方法：

```python
import uwxpy.configs.app_init as app
import libcore_hng.utils.app_logger as app_logger

# 設定ファイルで初期化

app.init_app(__file__, "logger.json", "uwxpy.json")

app_logger.info("uwxpy アプリケーションの初期化が完了しました！")
```

## プロンプト生成の例

```python
from uwxpy.service.generate_prompt_service import GeneratePrompt

# データファイルからプロンプトジェネレータを初期化
prompt_gen = GeneratePrompt(
    modes_path="tests/prompt/modes.json",
    word_path="tests/prompt/words_data.json",
    style_anchor_path="tests/prompt/style_anchor.json"
)

# 新しい画像生成用プロンプトを作成
prompt_request, elements = prompt_gen.create_rewrite_request(mode_key='chill', is_edit=False)
print(prompt_request)
```

## ライセンス

このプロジェクトはBSD-3-Clauseライセンスの下で公開されています。詳細はLICENSEファイルをご覧ください。

## 作成者

- **unchainworks** ([kajin0318@gmail.com](mailto:kajin0318@gmail.com))
- [GitHubリポジトリ](https://github.com/kaioman/uwxpy)
