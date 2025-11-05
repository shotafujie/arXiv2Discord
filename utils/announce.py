# =========================
# announce.py
# Discord投稿・公開・投稿ID管理処理
# =========================
import requests
import json
import os
import logging

# --------------------------------------------------
# 投稿済みIDの管理（arXiv IDのみ保存）
# --------------------------------------------------

def load_posted_ids(posted_ids_file):
    """
    投稿済みarXiv ID群をJSONから取得
    - JSONにはarXiv IDのみを記録（URLは保存しない）
    - ファイルがなければ空集合を返す
    """
    logging.info("load_posted_ids")
    if not os.path.exists(posted_ids_file):
        return set()
    with open(posted_ids_file, "r", encoding="utf-8") as f:
        try:
            return set(json.load(f))
        except Exception as ex:
            logging.warning(f"投稿済みIDファイル読込失敗: {ex}")
            return set()

def save_posted_ids(posted_ids, posted_ids_file):
    """
    投稿済みarXiv ID集合をJSONに保存
    - arXiv IDのみを保存（URLは保存しない）
    - URLが必要な際は都度 IDから生成: f"https://arxiv.org/abs/{arxiv_id}"
    """
    logging.info("save_posted_ids")
    with open(posted_ids_file, "w", encoding="utf-8") as f:
        json.dump(list(posted_ids), f, ensure_ascii=False, indent=2)

# --------------------------------------------------
# Discordへの投稿と公開フロー
# --------------------------------------------------

def post_and_publish_to_discord(channel_id, content, bot_token):
    """
    Discordにメッセージ投稿し，クロスポスト（公開）まで実行
    - content: Discordに投稿するメッセージ内容（URLを含む）
    - URLはIDから生成されたものを使用
    """
    logging.info("投稿→公開開始")
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }
    data = {"content": content}
    
    # Discord投稿
    resp = requests.post(url, headers=headers, json=data)
    logging.info(f"status: {resp.status_code}")
    logging.info(f"body: {resp.text}")
    
    if resp.status_code != 200:
        logging.info(f"Discord投稿失敗: {resp.status_code} {resp.text}")
        return
    
    logging.info(f"Discord投稿成功！")
    
    # メッセージIDを取得し，公開(クロスポスト)
    try:
        message_id = resp.json()["id"]
        publish_url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}/crosspost"
        publish_resp = requests.post(publish_url, headers=headers)
        
        logging.info(f"publish_status: {publish_resp.status_code}")
        logging.info(f"publish_body: {publish_resp.text}")
        
        if publish_resp.status_code == 200:
            logging.info(f"Discord公開（クロスポスト）成功！")
        else:
            logging.error(f"公開失敗: {publish_resp.status_code}, {publish_resp.text}")
    except Exception as e:
        logging.exception(f"クロスポスト（公開）API例外！", e)
