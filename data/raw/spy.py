"""
S&P 500 지수의 일별 데이터를 로드하여 저장하는 모듈
"""
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Union

import pandas as pd
import yfinance as yf

from config import DATA_START_DATE, LOG_FORMAT, LOG_LEVEL, SPY_DATA_FILE, TRADING_START_TIME

# 로깅 설정
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(__file__).parent / 'spy_data.log')
    ]
)
logger = logging.getLogger(__name__)

class SPYDataLoader:
    """S&P 500 데이터 로더 클래스"""
    
    def __init__(self, start_date: str = DATA_START_DATE):
        """
        Args:
            start_date (str): 데이터 수집 시작일 (YYYY-MM-DD)
        """
        self.start_date = start_date
        self.spy_data = None
        self._ensure_data_dir()
        
    @staticmethod
    def _ensure_data_dir():
        """데이터 디렉토리 존재 확인 및 생성"""
        SPY_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        
    def _load_existing_data(self) -> Optional[pd.DataFrame]:
        """기존 데이터 로드
        
        Returns:
            Optional[pd.DataFrame]: 기존 데이터 또는 None
        """
        try:
            if SPY_DATA_FILE.exists():
                data = pd.read_csv(SPY_DATA_FILE, index_col='Date', parse_dates=True)
                logger.info(f"기존 데이터 로드 완료: {len(data)} 개의 데이터 포인트")
                return data
        except Exception as e:
            logger.error(f"기존 데이터 로드 실패: {e}")
        return None

    def load_data(self, force_update: bool = False) -> pd.DataFrame:
        """데이터 로드 및 업데이트
        
        Args:
            force_update (bool): 강제 업데이트 여부
            
        Returns:
            pd.DataFrame: 업데이트된 데이터
        """
        try:
            existing_data = None if force_update else self._load_existing_data()
            
            if existing_data is not None:
                start_date = (existing_data.index[-1] + timedelta(days=1)).strftime('%Y-%m-%d')
            else:
                start_date = self.start_date
                
            # 현재 시간이 미국 장 마감 시간 이후인지 확인
            now = datetime.now()
            if now.strftime('%H:%M:%S') < TRADING_START_TIME:
                logger.info("미국 장 마감 전입니다. 전일 데이터까지만 업데이트합니다.")
                end_date = (now - timedelta(days=1)).strftime('%Y-%m-%d')
            else:
                end_date = now.strftime('%Y-%m-%d')
            
            # 새로운 데이터 다운로드
            ticker = yf.Ticker("^GSPC")
            new_data = ticker.history(start=start_date, end=end_date, interval="1d")
            
            if new_data.empty:
                if existing_data is not None:
                    logger.info("새로운 데이터가 없습니다. 기존 데이터를 반환합니다.")
                    return existing_data
                raise ValueError("S&P 500 데이터를 불러올 수 없습니다.")
            
            # 필요한 컬럼만 선택하고 소수점 2자리로 반올림
            new_data = new_data[['Open', 'High', 'Low', 'Close', 'Volume']].round(2)
            
            # 날짜 형식 통일
            new_data.index = new_data.index.normalize().tz_localize(None)
            
            # 기존 데이터와 병합
            if existing_data is not None:
                self.spy_data = pd.concat([existing_data, new_data])
                self.spy_data = self.spy_data[~self.spy_data.index.duplicated(keep='last')]
            else:
                self.spy_data = new_data
            
            logger.info(f"데이터 업데이트 완료: {len(self.spy_data)} 개의 데이터 포인트")
            return self.spy_data
        
        except Exception as e:
            logger.error(f"데이터 로드 실패: {e}")
            raise
        
    def save_to_csv(self, filename: Union[str, Path] = None):
        """데이터를 CSV 파일로 저장
        
        Args:
            filename (Union[str, Path], optional): 저장할 파일 경로
        """
        if self.spy_data is None:
            raise ValueError("데이터가 로드되지 않았습니다.")
        
        filename = SPY_DATA_FILE if filename is None else Path(filename)
        
        try:
            self.spy_data.to_csv(filename)
            logger.info(f"데이터를 {filename}에 저장했습니다.")
        except Exception as e:
            logger.error(f"데이터 저장 실패: {e}")
            raise
        
    def get_data(self) -> pd.DataFrame:
        """현재 로드된 데이터 반환
        
        Returns:
            pd.DataFrame: 로드된 데이터
        """
        if self.spy_data is None:
            raise ValueError("데이터가 로드되지 않았습니다.")
        return self.spy_data.copy()

def update_spy_data():
    """SPY 데이터 업데이트 실행 함수"""
    try:
        loader = SPYDataLoader()
        loader.load_data()
        loader.save_to_csv()
        logger.info("SPY 데이터 업데이트가 완료되었습니다.")
    except Exception as e:
        logger.error(f"SPY 데이터 업데이트 실패: {e}")
        raise

if __name__ == "__main__":
    update_spy_data()
