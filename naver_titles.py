import requests
from bs4 import BeautifulSoup

URL = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%95%84%EC%9D%B4%ED%8F%B017&ackey=folw28gm"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def is_ad_element(tag):
    """광고 요소인지 판단"""
    href = (tag.get("href") or "").lower()
    if "ader.naver.com" in href or "/nad-" in href:
        return True
    for parent in tag.parents:
        if parent is None:
            continue
        classes = parent.get("class") or []
        if any("ad-badge" in c or "ugc-gray50-ad-badge" in c for c in classes):
            return True
        if parent.find(string=lambda s: isinstance(s, str) and "광고" in s):
            return True
    return False

def extract_text_from_tag(tag):
    """태그에서 텍스트 추출 및 정리"""
    text = tag.get_text(" ", strip=True)
    return " ".join(text.split())

def fetch_titles(url):
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    # 블로그, 카페, in.naver.com 등 다양한 UGC 콘텐츠 타이틀 선택자
    selectors = [
        # 기본 뉴스 선택자
        "a.news_tit",
        "a._sp_each_title",
        "a.api_txt_lines.total_tit",
        
        # UGC 콘텐츠 타이틀 (블로그, 카페 등)
        "a.fds-comps-right-image-text-title",
        "a[class*='fds-comps-right-image-text-title']",
        "a[data-heatmap-target='.link']",
        "a[data-heatmap-target='.imgtitlelink']",
        
        # 콘텐츠 내용
        "a.fds-comps-right-image-text-content",
        "a[class*='fds-comps-right-image-text-content']",
        "a[data-heatmap-target='.tit']",
        "a[data-heatmap-target='.des']",
        
        # 댓글/응답 텍스트
        "a.fds-ugc-sub-info-reply-layout-wrapper",
        "span.fds-ugc-sub-info-reply-text",
        
        # 기타 링크
        "a[data-cb-target]",
        "a[href*='blog.naver.com']",
        "a[href*='cafe.naver.com']",
        "a[href*='in.naver.com']",
    ]

    seen = set()
    titles = []

    for sel in selectors:
        for el in soup.select(sel):
            # span이나 다른 요소인 경우 부모 a 태그 찾기
            a_tag = el if el.name == "a" else el.find_parent("a")
            
            if a_tag is None:
                # span 등에서 직접 텍스트 추출
                candidate_text = extract_text_from_tag(el)
                if not candidate_text or len(candidate_text) < 5:
                    continue
                if is_ad_element(el):
                    continue
                if candidate_text not in seen:
                    seen.add(candidate_text)
                    titles.append(candidate_text)
                continue

            # 광고 요소 건너뛰기
            if is_ad_element(a_tag):
                continue

            candidate_text = extract_text_from_tag(a_tag)
            if not candidate_text or len(candidate_text) < 5:
                continue
            if candidate_text not in seen:
                seen.add(candidate_text)
                titles.append(candidate_text)

    return titles

if __name__ == "__main__":
    try:
        results = fetch_titles(URL)
        if not results:
            print("제목을 찾지 못했습니다. 페이지가 JS로 렌더링되는 경우 Selenium 사용을 고려하세요.")
        else:
            for i, title in enumerate(results, 1):
                print(f"{i}. {title}")
    except Exception as e:
        print("오류:", e)