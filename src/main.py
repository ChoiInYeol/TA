"""
기술적 지표 기반 트레이딩 시그널 분석 시스템
"""
import logging
from pathlib import Path

import pandas as pd

from config import (
    HEATMAP_FILE, INDICATORS_FILE, LOG_FORMAT, LOG_LEVEL,
    SIGNALS_FILE, SPY_DATA_FILE
)
from data.raw.spy import update_spy_data
from technical_indicator import CORE16MomentumIndicator, CORE16ContrarianIndicator
from signal_generator import SignalGenerator
from visualizer import aligned_signal_candlestick

# 로깅 설정
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(__file__).parent / 'main.log')
    ]
)
logger = logging.getLogger(__name__)

def process_technical_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """기술적 지표 계산
    
    Args:
        data (pd.DataFrame): OHLCV 데이터
        
    Returns:
        pd.DataFrame: 계산된 지표가 포함된 데이터프레임
    """
    try:
        logger.info("기술적 지표 계산 시작")
        
        # 모멘텀 지표 계산
        momentum_indicator = CORE16MomentumIndicator(data, resample='1d')
        momentum_df = momentum_indicator.calculate_all_indicators()
        
        # 반추세 지표 계산
        contrarian_indicator = CORE16ContrarianIndicator(data, resample='1d')
        contrarian_df = contrarian_indicator.calculate_all_indicators()
        
        # 모든 지표를 하나의 데이터프레임으로 통합
        combined_df = pd.concat([data, momentum_df, contrarian_df], axis=1).round(4)
        
        logger.info(f"기술적 지표 계산 완료: {len(combined_df.columns)} 개의 지표")
        return combined_df
    
    except Exception as e:
        logger.error(f"기술적 지표 계산 실패: {e}")
        raise

def generate_trading_signals(data: pd.DataFrame) -> pd.DataFrame:
    """트레이딩 시그널 생성
    
    Args:
        data (pd.DataFrame): 기술적 지표가 포함된 데이터프레임
        
    Returns:
        pd.DataFrame: 생성된 시그널 데이터프레임
    """
    try:
        logger.info("트레이딩 시그널 생성 시작")
        
        signal_generator = SignalGenerator(data)
        momentum_signals = signal_generator.generate_momentum_signals()
        contrarian_signals = signal_generator.generate_contrarian_signals()
        
        # 모든 시그널을 하나의 데이터프레임으로 통합
        all_signals = pd.concat([momentum_signals, contrarian_signals], axis=1).round(4)
        
        logger.info(f"트레이딩 시그널 생성 완료: {len(all_signals.columns)} 개의 시그널")
        return all_signals
    
    except Exception as e:
        logger.error(f"트레이딩 시그널 생성 실패: {e}")
        raise

def create_visualization(signals_file: Path = SIGNALS_FILE,
                       price_file: Path = SPY_DATA_FILE,
                       output_file: Path = HEATMAP_FILE,
                       last_n_trading_days: int = 30) -> None:
    """시각화 생성
    
    Args:
        signals_file (Path): 시그널 파일 경로
        price_file (Path): 가격 데이터 파일 경로
        output_file (Path): 출력 파일 경로
        last_n_trading_days (int): 표시할 거래일 수
    """
    try:
        logger.info("시각화 생성 시작")
        
        aligned_signal_candlestick(
            signal_file=str(signals_file),
            price_file=str(price_file),
            last_n_trading_days=last_n_trading_days,
            savefig=str(output_file)
        )
        
        logger.info(f"시각화 생성 완료: {output_file}")
    
    except Exception as e:
        logger.error(f"시각화 생성 실패: {e}")
        raise

def main():
    """메인 실행 함수"""
    try:
        logger.info("분석 프로세스 시작")
        
        # 1. SPY 데이터 업데이트
        update_spy_data()
        
        # 2. 데이터 로드
        data = pd.read_csv(SPY_DATA_FILE, index_col='Date', parse_dates=True)
        
        # 3. 기술적 지표 계산
        indicators_df = process_technical_indicators(data)
        indicators_df.to_csv(INDICATORS_FILE)
        
        # 4. 트레이딩 시그널 생성
        signals_df = generate_trading_signals(indicators_df)
        signals_df.to_csv(SIGNALS_FILE)
        
        # 5. 시각화 생성
        create_visualization()
        
        logger.info("분석 프로세스 완료")
        
    except Exception as e:
        logger.error(f"분석 프로세스 실패: {e}")
        raise

if __name__ == "__main__":
    main() 