# 環境構築ガイド

## 概要

このガイドは arXiv2Discord を使うための環境構築手順（必要なライブラリ・APIキー・設定方法など）を説明します.

## 前提条件

- Python 3.8 以上
- pip パッケージマネージャ
- Git（リポジトリのクローン用）

## インストール手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/shotafujie/arXiv2Discord.git
cd arXiv2Discord
```

### 2. 依存パッケージのインストール

Python用ライブラリをpipでインストールします:

```bash
pip install -r requirements.txt
```

主な依存ライブラリ:

- `requests` - arXiv/Perplexity/DiscordへのAPI接続
- `pyyaml` - YAML設定ファイルの読込
- `python-dotenv` - 環境変数管理 (任意)

### 3. 環境変数の設定

プロジェクトルートに`.env`ファイルを作成するか, OSの環境変数として設定.

#### 必須環境変数

| 変数                | 説明                 | 例                  |
|---------------------|----------------------|---------------------|
| `PERPLEXITY_API_KEY`   | Perplexity APIのキー | pplx-xxxxxxxxxxxxxxxx |
| `DISCORD_BOT_TOKEN`    | Discord BotのToken   | MTxxxxxxxxxxxx.yyyyyyyyyy.zzzzzzzzz |
| `DISCORD_CHANNEL_ID`   | 投稿先のチャンネルID | 123456789012345678 |

#### 任意環境変数

| 変数                | 説明                 | デフォルト値     |
|---------------------|----------------------|-----------------|
| `ARXIV_SETTINGS_PATH` | YAMLファイルのパス    | `./arxiv_settings.yaml` |
| `STATE_FILE`        | 投稿済みIDの保存ファイル | `./posted_arxiv_ids.json` |

**環境変数の設定例**

`.env`ファイルの例:

```env
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxx
DISCORD_BOT_TOKEN=MTxxxxxxxxxxxx.yyyyyyyyyy.zzzzzzzzz
DISCORD_CHANNEL_ID=123456789012345678
ARXIV_SETTINGS_PATH=./arxiv_settings.yaml
STATE_FILE=./posted_arxiv_ids.json
```

### 4. arxiv_settings.yaml の設定

arXiv検索条件を`arxiv_settings.yaml`に定義します.

**基本設定例**

```yaml
keywords:
  - "multimodal"
  - "text-to-image"

categories:
  - "cat:cs.AI"
  - "cat:cs.LG"

recent_hours: 24  # 過去24時間の論文のみ取得

max_results: 10
```

#### 主なarXivカテゴリ

- `cat:cs.AI` - 人工知能
- `cat:cs.LG` - 機械学習
- `cat:cs.CL` - 計算と言語 (NLP)
- `cat:cs.CV` - コンピュータビジョン
- `cat:stat.ML` - 機械学習（統計）

より詳細なカテゴリは[arXiv Category Taxonomy](https://arxiv.org/category_taxonomy)参照.

---

## APIキーの取得方法

### Perplexity API

1. [Perplexity公式サイト](https://www.perplexity.ai/)にアクセス
2. アカウント登録/ログイン
3. 設定画面からAPIキーを生成
4. 生成されたキーを`.env`の`PERPLEXITY_API_KEY`に設定

### Discord Bot Token

1. [Discord Developer Portal](https://discord.com/developers/applications)にアクセス
2. 「New Application」をクリックしアプリ作成
3. 左メニューの「Bot」タブを選択
4. 「Add Bot」でボット作成
5. 「TOKEN」セクションで「Copy」をクリック
6. コピーしたトークンを`.env`の`DISCORD_BOT_TOKEN`に設定
7. 「Privileged Gateway Intents」でMessage Content Intentを有効化
8. 「OAuth2」→「URL Generator」で `bot` + 必要な権限（Send Messages, Embed Links等）を選択
9. 生成されたURLでボットをサーバーに招待

### Discord Channel ID

1. Discordでデベロッパーモードを有効化（設定→詳細設定→デベロッパーモード）
2. 投稿したいチャンネルを右クリック
3. 「IDをコピー」を選択
4. `.env`の`DISCORD_CHANNEL_ID`に設定

---

## 動作確認

### テスト実行

```bash
python main.py
```

**正常動作時の出力例**:

```
[INFO] Loading settings from ./arxiv_settings.yaml
[INFO] Searching arXiv...
[INFO] Found 5 papers
[INFO] Generating summaries with Perplexity API...
[INFO] Posting to Discord...
[SUCCESS] Posted paper: Example Title (arXiv:2401.12345)
```

---

## トラブルシューティング

### よくあるエラー

#### 1. `ModuleNotFoundError: No module named 'xxx'`

**原因**: 依存パッケージが未インストール

**解決法**: `pip install -r requirements.txt`で依存インストール

#### 2. `KeyError: 'PERPLEXITY_API_KEY'`

**原因**: 環境変数が未設定

**解決法**: `.env`やシステム環境変数の値を確認

#### 3. Discord投稿エラー（403 Forbidden）

**原因**: ボット権限不足またはチャンネルID誤り

**解決法**: ボット権限＆チャンネルIDを確認

#### 4. Discord投稿エラー（404 Not Found）

**原因**: ボットがチャンネルにアクセスできない

**解決法**: Discordサーバ・チャンネル両方で権限確認

---

## 次のステップ

環境構築完了後は以下を参照:

- [ワークフロー解説](./workflow.md) - 処理フローの詳細
- [アーキテクチャ解説](./architecture.md) - コード構造とモジュール設計
