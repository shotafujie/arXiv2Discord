# =========================
# searchpaper.py
# arXiv論文検索・取得・フィルタリング処理
# =========================
import requests
import xml.etree.ElementTree as ET
import logging
from datetime import datetime, timedelta
# ------------------------------------------
# arXiv検索クエリ生成
# ------------------------------------------
def build_arxiv_query(keywords, category, max_results):
    """キーワードとカテゴリに基づきarXivのAPIクエリ文字列を生成"""
    logging.info("Building ARXiv query")
    # 半角スペース含む場合は""で括る
    qs = " OR ".join([f'"{k}"' if " " in k else k for k in keywords])
    return f"http://export.arxiv.org/api/query?search_query=({category})+AND+all:({qs})&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
# ------------------------------------------
# arXivフィード(xml)解析
# ------------------------------------------
def parse_arxiv_feed(feed_xml):
    """arXivから受け取ったATOM形式のXMLをパースし論文情報リスト化"""
    logging.info("parse_arxiv_feed")
    entries = []
    root = ET.fromstring(feed_xml)
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
        abstract = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
        link = entry.find('{http://www.w3.org/2005/Atom}id').text.strip()
        author_elems = entry.findall('{http://www.w3.org/2005/Atom}author')
        authors = ", ".join([a.find('{http://www.w3.org/2005/Atom}name').text.strip() for a in author_elems]) if author_elems else "N/A"
        published = entry.find('{http://www.w3.org/2005/Atom}published').text.strip()
        arxiv_id = link.split('/')[-1]
        entries.append({
            "title": title,
            "abstract": abstract,
            "link": link,
            "authors": authors,
            "published": published,
            "arxiv_id": arxiv_id,
        })
    return entries
# --------------------------------------------------
# 新着(指定時間以内)だけフィルタ
# --------------------------------------------------
def filter_recent_entries(entries, hours):
    """新着◯時間以内だけ抽出，日付失敗はスキップ"""
    logging.info("filter_recent_entries")
    threshold = datetime.utcnow() - timedelta(hours=hours)
    results = []
    for e in entries:
        published_str = e.get("published", "")
        try:
            published = datetime.strptime(published_str, "%Y-%m-%dT%H:%M:%SZ")
        except Exception as ex:
            logging.warning(f"日付パース失敗: {published_str} ({ex})")
            continue
        if published >= threshold:
            results.append(e)
    return results
# --------------------------------------------------
# arXiv論文検索のメイン関数
# --------------------------------------------------
def search_arxiv_papers(keywords, category, max_results, recent_hours):
    """arXiv APIで論文を検索し，新着のものだけ返す"""
    logging.info("search_arxiv_papers")
    qurl = build_arxiv_query(keywords, category, max_results)
    r = requests.get(qurl, timeout=20)
    papers = parse_arxiv_feed(r.content)
    logging.info(f"papers取得件数: {len(papers)}")
    recent_papers = filter_recent_entries(papers, hours=recent_hours)
    return recent_papers
