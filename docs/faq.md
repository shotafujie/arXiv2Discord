# よくある質問 (FAQ)

## インストールとセットアップ

### Q: システム要件は何ですか?

**A:** Python 3.8以上, pipパッケージマネージャー, インターネット接続が必要です. 

### Q: 必要なAPIキーはどのように取得しますか?

**A:** 
- **Perplexity APIキー**: perplexity.aiでサインアップし, 設定でキーを生成します
- **Discord Botトークン**: Discord Developer Portalでボットを作成し, トークンをコピーします
- 詳細な手順は[環境設定ガイド](./env_setup.md)を参照してください

### Q: 環境変数はどのように管理すべきですか?

**A:** 環境変数はGitHub Actions Secretsで管理することを強く推奨します. これによりAPIキーやトークンなどの機密情報を安全に保管できます.
- 詳細: [GitHub Actions Secretsの使用方法](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
- リポジトリの Settings > Secrets and variables > Actions から設定できます

### Q: スクリプトを自動実行するようにスケジュールするにはどうすればよいですか?

**A:** このプロジェクトでは**GitHub Actionsワークフロー**を使用した自動化を推奨しています.

**重要な推奨事項:**
- CRON式の分には`0`ではなく，`10`など他のリポジトリと重複しない時間を指定してください
  - 例: `10 9 * * *` (毎日9:10に実行)
  - 理由: 多くのワークフローが毎時0分に起動するため，負荷が集中しスムーズに起動しない可能性があります
- 参考情報:
  - [GitHub公式: ワークフローをトリガーするイベント (schedule)](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
  - [Qiita: GitHub Actionsのscheduleトリガーの注意点](https://qiita.com/tommy_aka_jps/items/5f4fe384008ffc9fa794)

詳細な設定方法は[ワークフローガイド](./workflow.md)を参照してください.

**その他の自動化方法:**
- **Linux/macOS**: cronジョブを使用
- **Windows**: タスクスケジューラーを使用
- **クラウド**: AWS Lambda, Google Cloud Functionsなどにデプロイ

---

## 設定

### Q: `recent_hours`パラメータは何をしますか?

**A:** 指定された時間数以内に公開された論文のみを含めるようにフィルタリングします. 例えば, `recent_hours: 24`は過去24時間の論文のみを取得します. これにより古い論文の投稿を防ぎます.

### Q: 複数のキーワードを一度に検索できますか?

**A:** はい， `arxiv_settings.yaml`はキーワードのリストを受け入れます. ツールはすべてのキーワードを独立して検索します. 詳細は[設定ファイルの説明](../README.md#設定)を参照してください.

### Q: 利用可能なarXivカテゴリは何ですか?

**A:** 一般的なカテゴリには以下が含まれます:
- `cat:cs.AI` - 人工知能
- `cat:cs.LG` - 機械学習
- `cat:cs.CL` - 計算と言語
- `cat:cs.CV` - コンピュータビジョン
- `cat:stat.ML` - 機械学習(統計)

完全なリストは[arXiv Category Taxonomy](https://arxiv.org/category_taxonomy)を参照してください.

### Q: AI要約の形式を変更するにはどうすればよいですか?

**A:** `perplexity_client.py`の`build_perplexity_prompt()`関数内のプロンプトテンプレートを編集します. セクション, 言語, トーン, 出力形式をカスタマイズできます. 詳細なカスタマイズ方法は[アーキテクチャドキュメント](./architecture.md)を参照してください.

---

## Discord投稿

### Q: Discord投稿の制限はありますか?

**A:** はい，Discordアナウンスチャンネルには**1時間あたり10件**の投稿制限があります. この制限を超えないよう，`arxiv_settings.yaml`の`max_posts`パラメータを適切に設定してください.
- 参考: [Discord公式: Rate Limits](https://discord.com/developers/docs/topics/rate-limits)

### Q: 投稿が重複しないようにするにはどうすればよいですか?

**A:** システムは`posted_arxiv_ids.json`ファイルを使用して，既に投稿された論文のIDを追跡します. このファイルは自動的に更新されるため，手動で管理する必要はありません.

---

## トラブルシューティング

### Q: ワークフローが実行されない場合はどうすればよいですか?

**A:** 以下を確認してください:
1. GitHub Actions Secretsが正しく設定されているか
2. ワークフローファイルのCRON式が正しいか
3. リポジトリのActions設定が有効になっているか

詳細なトラブルシューティングは[ワークフローガイド](./workflow.md)を参照してください.

### Q: エラーが発生した場合はどこで確認できますか?

**A:** GitHub Actionsのワークフロー実行ログから詳細なエラー情報を確認できます. リポジトリの「Actions」タブから該当するワークフローの実行結果を確認してください.
