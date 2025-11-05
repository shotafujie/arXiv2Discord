# =========================
# arXiv2Discord メインモジュール（リファクタリング版）
# utils配下の各モジュールを利用
# =========================
import os
import yaml
import logging

# utils配下の各モジュールをインポート
from utils.searchpaper import search_arxiv_papers
from utils.summarize import generate_perplexity_comment
from utils.announce import load_posted_ids, save_posted_ids, post_and_publish_to_discord

# -- ログフォーマット設定 --
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -- 環境変数の取得 (APIキー等) --
PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY")
PERPLEXITY_MODEL = os.environ.get("PERPLEXITY_MODEL")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = os.environ.get("DISCORD_CHANNEL_ID")
POSTED_IDS_FILE = os.environ.get("POSTED_IDS_FILE", "posted_arxiv_ids.json")

# 設定ファイル読込用関数
def load_settings():
    """arxiv_settings.yamlから設定（キーワード等）を読込む"""
    with open("arxiv_settings.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# 設定値の取得
settings = load_settings()
ARXIV_KEYWORDS = settings["keywords"]
CATEGORY = settings["category"]
MAX_RESULTS = settings["max_results"]
RECENT_HOURS = settings["recent_hours"]

# --------------------------------------------------
# メイン処理
# --------------------------------------------------
def main():
    """arXiv API検索→AI要約→Discord投稿，投稿済ID更新まで一連実施"""
    logging.info("main")
    
    # 投稿済みID読込（arXiv IDのみ記録）
    posted_ids = load_posted_ids(POSTED_IDS_FILE)
    
    # arXiv論文検索（utils.searchpaper使用）
    recent_papers = search_arxiv_papers(ARXIV_KEYWORDS, CATEGORY, MAX_RESULTS, RECENT_HOURS)
    
    # 投稿対象の絞り込み（arXiv IDで判定）
    to_post = []
    for p in recent_papers:
        if p["arxiv_id"] in posted_ids:
            continue
        to_post.append(p)
        if len(to_post) == MAX_RESULTS:
            break
    
    # 各論文について要約→Discord投稿
    post_count = 0
    for p in to_post:
        try:
            # arXiv IDからURL生成
            arxiv_id = p["arxiv_id"]
            link = f"https://arxiv.org/abs/{arxiv_id}"
            
            # キーワードマッチング
            kw = ", ".join([k for k in ARXIV_KEYWORDS if k.lower() in (p["title"] + p["abstract"]).lower()])
            authors = p.get("authors", "N/A")
            
            # AI要約生成（utils.summarize使用）
            comment = generate_perplexity_comment(
                p["title"], 
                p["abstract"], 
                kw, 
                authors, 
                link,
                PERPLEXITY_API_KEY,
                PERPLEXITY_MODEL
            )
            
            # Discordメッセージ組立（ID→URL変換したlinkを使用）
            discord_message = (
                f"# {p['title']}\n"
                f" {authors}\n"
                f" {link}\n"
                f"{comment}"
            )
            
            # Discord投稿・公開（utils.announce使用）
            post_and_publish_to_discord(DISCORD_CHANNEL_ID, discord_message, DISCORD_BOT_TOKEN)
            
            # 投稿済みIDとして記録（arXiv IDのみ保存）
            posted_ids.add(arxiv_id)
            post_count += 1
        except Exception as e:
            logging.exception(f"投稿ループ例外！", e)
    
    # 投稿済みID保存（arXiv IDのみ記録，utils.announce使用）
    try:
        save_posted_ids(posted_ids, POSTED_IDS_FILE)
        logging.info(f"save_posted_ids後")
    except Exception as e:
        logging.exception(f"save_posted_ids例外！", e)
    
    logging.info(f"今回投稿件数: {post_count}")

if __name__ == "__main__":
    main()
