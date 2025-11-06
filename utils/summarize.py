# =========================
# summarize.py
# Perplexity APIを使った論文要約生成処理
# =========================
import requests
import logging

# --------------------------------------------------
# Perplexity用プロンプト生成
# --------------------------------------------------
def build_perplexity_prompt(title, abstract, keywords, authors, link):
    """論文情報を元にPerplexity用プロンプト形成"""
    logging.info("build_perplexity_prompt")
    tags = " ".join([f"#{k.replace(' ', '')}" for k in keywords.split(",") if k])
    return (
        f"【論文タイトル】\n{title}\n\n"
        f"【著者】\n{authors}\n\n"
        f"【arXivリンク】\n{link}\n\n"
        f"【アブストラクト】\n{abstract}\n\n"
        f"指定されたarXiv論文について、下記の見出し構成で日本語要約＋考察コメントを書いてください。要約には小見出し名は不要です。"
        f"自己肯定感高め＆親しみある言葉づかい、絵文字を交えてまとめてください。\n\n"
        f"- どんなもの？:\n"
        f"- 先行研究と比べてどこがすごい？:\n"
        f"- 技術や手法のキモはどこ？:\n"
        f"- どうやって有効だと検証した？:\n"
        f"- 議論はある？:\n"
        f"\n#タグ: {tags}\n"
        f"## AIコメント\n"
        f"（200～300字程度で、自己肯定感高め＆親しみある語り＋絵文字を盛り込んでください！）\n\n"
    )

# --------------------------------------------------
# Perplexity APIでAIコメント生成
# --------------------------------------------------
def generate_perplexity_comment(title, abstract, keywords, authors, link, api_key, model):
    """PerplexityにAPIリクエストしAI生成コメント取得"""
    logging.info("generate_perplexity_comment")
    prompt = build_perplexity_prompt(title, abstract, keywords, authors, link)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "日本語の学術解説者として出力してください"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1024,
        "temperature": 0.6,
    }
    resp = requests.post("https://api.perplexity.ai/chat/completions", headers=headers, json=data, timeout=45)
    try:
        res = resp.json()
    except Exception as e:
        logging.info(f"APIレスポンスをJSONにパースできません: {e}, {resp.text}")
        return "APIレスポンスエラー"
    if "choices" not in res:
        logging.info(f"APIエラー or レート制限: {res}")
        return "APIエラー or 認証・キー・モデル名等に問題"
    comment = res["choices"][0]["message"]["content"].strip()
    return comment
