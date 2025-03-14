"""
S&P 500 데이터 수집 및 관리 모듈
"""
import logging
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

from .settings import SPY_DATA_FILE

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def update_spy_data(
    symbol: str = "^GSPC",
    days_back: int = 7,
    data_file: Path = SPY_DATA_FILE,
) -> None:
    """
    S&P 500 ETF 데이터를 업데이트합니다.
    최근 7일간의 데이터를 항상 다운로드하여 저장합니다.

    Args:
        symbol (str): 다운로드할 심볼
        days_back (int): 다운로드할 과거 데이터 기간 (일)
        data_file (Path): 저장할 파일 경로
    """
    try:
        # 디렉토리가 없으면 생성
        data_file.parent.mkdir(parents=True, exist_ok=True)

        # 기존 데이터 확인
        existing_data = None
        if data_file.exists():
            try:
                existing_data = pd.read_csv(data_file)
                existing_data["Date"] = pd.to_datetime(existing_data["Date"]).dt.date
                logger.info(f"기존 데이터 로드 완료: {len(existing_data)}개 데이터 포인트")
            except Exception as e:
                logger.warning(f"기존 데이터 로드 실패: {str(e)}")

        # 최근 7일 데이터 다운로드
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        start_date_str = start_date.strftime("%Y-%m-%d")
        
        logger.info(f"{symbol} 데이터 다운로드 시작: {start_date_str}부터")
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date_str)

        # 데이터 전처리
        df = df.reset_index()
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]

        # 기존 데이터와 병합
        if existing_data is not None and not existing_data.empty:
            # 중복 제거 및 정렬
            df = pd.concat([existing_data, df], ignore_index=True)
            df = df.drop_duplicates(subset=["Date"])
            df = df.sort_values("Date")
            logger.info(f"데이터 병합 완료: {len(df)}개 데이터 포인트")

        # 데이터 저장
        df.to_csv(data_file, index=False)
        logger.info(f"{symbol} 데이터 저장 완료: {len(df)}개 데이터 포인트")

    except Exception as e:
        logger.error(f"{symbol} 데이터 업데이트 실패: {str(e)}")
        raise


if __name__ == "__main__":
    # S&P 500 데이터 업데이트
    update_spy_data()
