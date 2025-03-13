'''
S&P 500 지수의 일별 데이터를 로드하여 저장하는 모듈
'''

import yfinance as yf
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SPYDataLoader:
    def __init__(self, start_date: str = "2000-01-01"):
        self.start_date = start_date
        self.spy_data = None

    def load_data(self):
        try:
            ticker = yf.Ticker("^GSPC")
            spy_data = ticker.history(start=self.start_date, interval="1d")
            
            if spy_data.empty:
                raise ValueError("S&P 500 데이터를 불러올 수 없습니다.")
                
            # Open, High, Low, Close, Volume만 다운로드
            spy_data = spy_data[['Open', 'High', 'Low', 'Close', 'Volume']]
            
            # 소수점 2자리로 반올림
            spy_data = spy_data.round(2)
            
            # 날짜 형식을 YYYY-MM-DD로 변경
            spy_data.index = spy_data.index.normalize().tz_localize(None)
            
            self.spy_data = spy_data
            
            logger.info(f"일별 S&P 500 데이터 로드 완료: {len(spy_data)} 개의 데이터 포인트")
            return spy_data
        
        except Exception as e:
            logger.error(f"S&P 500 데이터 로드 오류: {e}")
            raise e
        
    def save_to_csv(self, filename: str = None):
        if self.spy_data is None:
            raise ValueError("데이터가 로드되지 않았습니다.")
        
        if filename is None:
            # 기본 저장 경로 설정
            filename = str(Path(__file__).parent / 'spy_data.csv')
            
        self.spy_data.to_csv(filename, index=True)
        logger.info(f"S&P 500 데이터를 {filename}에 저장했습니다.")
        
    def get_data(self):
        return self.spy_data
    
if __name__ == "__main__":
    loader = SPYDataLoader()
    spy_data = loader.load_data()
    loader.save_to_csv()
