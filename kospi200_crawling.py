import requests
from bs4 import BeautifulSoup
import pandas as pd

def crawl_kospi200():
    url = "https://finance.naver.com/sise/sise_index.naver?code=KPI200"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 편입종목 테이블 찾기 (class='type_1')
        table = soup.find('table', {'class': 'type_1'})
        
        if not table:
            print("테이블을 찾을 수 없습니다.")
            return None
        
        # 테이블 헤더
        headers_list = []
        thead = table.find('tr')
        for th in thead.find_all('th'):
            headers_list.append(th.get_text(strip=True))
        
        # 테이블 데이터
        rows = []
        tbody_trs = table.find_all('tr')[1:]  # 헤더 제외
        
        for tr in tbody_trs:
            # 빈 행이나 구분선 무시
            if tr.find('td', {'colspan': '7'}):
                continue
            
            cols = tr.find_all('td')
            if not cols:
                continue
            
            # 종목명
            name = cols[0].get_text(strip=True)
            # 현재가
            price = cols[1].get_text(strip=True)
            # 전일비
            change_val = cols[2].get_text(strip=True)
            # 등락률
            change_rate = cols[3].get_text(strip=True)
            # 거래량
            volume = cols[4].get_text(strip=True)
            # 거래대금
            amount = cols[5].get_text(strip=True)
            # 시가총액
            market_cap = cols[6].get_text(strip=True)
            
            row = [name, price, change_val, change_rate, volume, amount, market_cap]
            rows.append(row)
        
        # DataFrame으로 변환
        df = pd.DataFrame(rows, columns=headers_list)
        
        print("=== 코스피200 편입종목 상위 데이터 ===")
        print(df)
        print(f"\n총 {len(df)}개의 종목")
        
        return df
        
    except Exception as e:
        print(f"에러 발생: {e}")
        return None

if __name__ == "__main__":
    crawl_kospi200()