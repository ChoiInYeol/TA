"""
S&P 500 데이터 수집 및 관리 모듈
"""
import logging
from pathlib import Path

import yfinance as yf
import pandas as pd

from config import SPY_DATA_FILE

logger = logging.getLogger(__name__)


def update_spy_data(
    symbol: str = "^GSPC",
    start_date: str = "2000-01-01",
    data_file: Path = SPY_DATA_FILE,
) -> None:
    """
    S&P 500 ETF 데이터를 업데이트합니다.

    Args:
        symbol (str): 다운로드할 심볼
        start_date (str): 데이터 시작일
        data_file (Path): 저장할 파일 경로
    """
    try:
        # 데이터 다운로드
        logger.info(f"{symbol} 데이터 다운로드 시작: {start_date}부터")
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date)

        # 데이터 전처리
        df = df.reset_index()
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]

        # 디렉토리가 없으면 생성
        data_file.parent.mkdir(parents=True, exist_ok=True)

        # 데이터 저장
        df.to_csv(data_file, index=False)
        logger.info(f"{symbol} 데이터 저장 완료: {len(df)}개 데이터 포인트")

    except Exception as e:
        logger.error(f"{symbol} 데이터 업데이트 실패: {str(e)}")
        raise


if __name__ == "__main__":
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # S&P 500 데이터 업데이트
    update_spy_data()
