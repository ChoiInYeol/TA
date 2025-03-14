"""
메인 실행 모듈

이 모듈은 기술적 지표와 매매 시그널을 생성하는 메인 실행 파일입니다.
"""

import logging
from pathlib import Path

from src.signal_generator import SignalGenerator
from src.technical_indicator import TechnicalIndicator
from src.update_spy import update_spy_data
from src.visualizer import TradingVisualizer

# 로그 디렉토리 생성
log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


def main() -> None:
    """메인 실행 함수"""
    try:
        # 데이터 디렉토리 생성
        data_dir = Path("data")
        data_dir.mkdir(parents=True, exist_ok=True)

        # spy 데이터 업데이트
        logger.info("spy 데이터 업데이트 시작")
        try:
            update_spy_data()
            logger.info("spy 데이터 업데이트 완료")
        except Exception as e:
            logger.error(f"spy 데이터 업데이트 실패: {str(e)}")
            raise

        # 기술적 지표 생성
        logger.info("기술적 지표 생성 시작")
        indicator = TechnicalIndicator()
        indicator.calculate_all()
        indicator.save_indicators()
        logger.info("기술적 지표 생성 완료")

        # 매매 시그널 생성
        logger.info("매매 시그널 생성 시작")
        generator = SignalGenerator()
        generator.generate_all()
        generator.save_signals()
        logger.info("매매 시그널 생성 완료")

        # 시각화 생성
        logger.info("시각화 생성 시작")
        visualizer = TradingVisualizer()
        visualizer.create_dashboard()
        visualizer.save_dashboard()
        logger.info("시각화 생성 완료")

    except Exception as e:
        logger.error(f"실행 중 오류 발생: {str(e)}")
        raise


if __name__ == "__main__":
    main()
