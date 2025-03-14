"""
트레이딩 시그널 시각화 모듈
"""

import logging
from pathlib import Path
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
from mplfinance.original_flavor import candlestick_ohlc

from config import HEATMAP_FILE, SIGNALS_FILE, SPY_DATA_FILE, TECHNICAL_INDICATORS

logger = logging.getLogger(__name__)


class TradingVisualizer:
    """트레이딩 시그널 시각화 클래스"""

    def __init__(
        self,
        signals_file: Path = SIGNALS_FILE,
        price_file: Path = SPY_DATA_FILE,
        output_file: Path = HEATMAP_FILE,
    ):
        """
        Args:
            signals_file (Path): 매매 시그널 파일 경로
            price_file (Path): 가격 데이터 파일 경로
            output_file (Path): 출력 파일 경로
        """
        self.signals_file = signals_file
        self.price_file = price_file
        self.output_file = output_file
        self.signals_df = None
        self.price_df = None
        self.merged_df = None
        self._load_data()

    def _load_data(self) -> None:
        """데이터를 로드합니다."""
        try:
            self.signals_df = pd.read_csv(self.signals_file)
            self.price_df = pd.read_csv(self.price_file)

            self.signals_df["Date"] = pd.to_datetime(self.signals_df.iloc[:, 0])
            self.price_df["Date"] = pd.to_datetime(self.price_df["Date"])

            logger.info("데이터 로드 완료")
        except Exception as e:
            logger.error(f"데이터 로드 실패: {str(e)}")
            raise

    def create_dashboard(self, last_n_trading_days: int = 30) -> None:
        """트레이딩 대시보드를 생성합니다.

        Args:
            last_n_trading_days (int): 표시할 거래일 수
        """
        try:
            # 시그널을 하루 뒤로 이동 (N+1일의 의사결정)
            self.signals_df.set_index("Date", inplace=True)
            # 마지막 날짜에 다음 거래일 추가하고 NaN으로 채우기
            next_business_day = self.signals_df.index[-1] + pd.offsets.BDay(1)
            self.signals_df.loc[next_business_day] = np.nan
            self.signals_df = self.signals_df.shift(1)  # 시그널을 하루 앞으로 이동

            # 데이터프레임 병합
            self.merged_df = pd.merge(
                self.price_df,
                self.signals_df,
                left_on="Date",
                right_index=True,
                how="outer",
            )
            self.merged_df.set_index("Date", inplace=True)
            self.merged_df.sort_index(inplace=True)

            if len(self.merged_df) >= last_n_trading_days:
                self.merged_df = self.merged_df.iloc[-last_n_trading_days:]

            self._create_visualization()
            logger.info("대시보드 생성 완료")

        except Exception as e:
            logger.error(f"대시보드 생성 실패: {str(e)}")
            raise

    def _create_visualization(self) -> None:
        """시각화를 생성합니다."""
        # 정수 인덱스로 변환
        dates = self.merged_df.index
        n_dates = len(dates)

        # OHLC 데이터 준비
        ohlc = []
        for i, (date, row) in enumerate(self.merged_df.iterrows()):
            ohlc.append((i, row["Open"], row["High"], row["Low"], row["Close"]))

        # 시그널 칼럼 정렬을 위한 기본 순서
        signal_order = [
            "SMA",
            "EMA",
            "TSI",
            "MACD",
            "PSAR",
            "ADX",
            "Aroon",
            "ADL",
            "ADR",
            "Ichimoku",
            "Keltner",
            "RSI",
            "BB",
            "CCI",
            "Stoch",
            "Williams",
            "CMO",
            "DeMarker",
            "Donchian",
            "Pivot",
            "PSY",
            "NPSY",
        ]
        signal_order = signal_order[::-1]  # 순서 반전

        # OHLCV 칼럼 제외
        signals = self.merged_df.drop(
            ["Open", "High", "Low", "Close", "Volume"], axis=1
        ).copy()

        # 시그널 칼럼 매칭 및 정렬
        signal_columns = []
        signal_display_names = []

        for base_name in signal_order:
            matching_columns = [col for col in signals.columns if base_name in col and "_Signal" in col]
            for col in matching_columns:
                signal_columns.append(col)
                params = re.search(r'\((.*?)\)', col)
                if params:
                    display_name = f"{base_name}({params.group(1)})"
                else:
                    display_name = base_name
                signal_display_names.append(display_name)

        # 시그널 데이터프레임 재정렬
        signals = signals[signal_columns]

        # 시그널 매핑 (-1 -> 0, 0 -> 1, 1 -> 2)
        heat_data = signals.replace({-1: 0, 0: 1, 1: 2}).to_numpy().T
        n_signals = heat_data.shape[0]

        # 그래프 생성
        fig = plt.figure(figsize=(15, 10))
        gs = plt.GridSpec(3, 1, height_ratios=[n_signals / 2, 6, 2], hspace=0.10)

        # 1. 히트맵
        ax_heat = fig.add_subplot(gs[0])

        # 히트맵 플롯 (빨간색: 매도, 회색: 중립, 초록색: 매수)
        cmap = ListedColormap(["#ff4d4d", "#e6e6e6", "#4dff4d"])
        im = ax_heat.imshow(
            heat_data,
            aspect="auto",  # 주가 차트와 맞추기 위해 auto로 설정
            extent=[-0.5, n_dates - 0.5, -0.5, n_signals - 0.5],
            cmap=cmap,
            origin="lower"  # 시그널 순서를 아래에서 위로 표시
        )

        # 히트맵 설정
        ax_heat.set_yticks(range(n_signals))
        ax_heat.set_yticklabels(signal_display_names, fontsize=8)
        ax_heat.set_xticks([])
        ax_heat.set_ylabel("Signals", fontsize=10)

        # 히트맵 그리드 (흰색 구분선)
        ax_heat.grid(False)  # 기본 그리드 제거
        ax_heat.set_xticks(np.arange(-0.5, n_dates, 1), minor=True)
        ax_heat.set_yticks(np.arange(-0.5, n_signals, 1), minor=True)
        ax_heat.grid(True, which="minor", color="white", linewidth=1)

        # 히트맵 셀 텍스트
        for i in range(n_signals):
            for j in range(n_dates):
                val = signals[signal_columns[i]].iloc[j]  # 올바른 순서로 접근
                if isinstance(val, (int, float)) and not np.isnan(val):
                    # 매핑된 값에 따라 텍스트 표시
                    if val == 1:
                        txt = "Buy"
                    elif val == -1:
                        txt = "Sell"
                    else:
                        txt = ""
                    ax_heat.text(j, i, txt, ha="center", va="center", fontsize=8)

        # 2. 캔들차트
        ax_candle = fig.add_subplot(gs[1])
        candlestick_ohlc(
            ax_candle,
            ohlc,
            width=0.6,
            colorup="#4dff4d",
            colordown="#ff4d4d",
            alpha=0.8,
        )

        # 캔들차트 설정
        ax_candle.set_xlim(-0.5, n_dates - 0.5)
        ax_candle.grid(True, alpha=0.3)
        ax_candle.set_ylabel("Price", fontsize=10)
        ax_candle.set_xticklabels([])

        # 캔들차트 마지막 날짜 음영 처리
        rect_candle = plt.Rectangle(
            (n_dates - 1.5, ax_candle.get_ylim()[0]),
            1,
            ax_candle.get_ylim()[1] - ax_candle.get_ylim()[0],
            facecolor="yellow",
            alpha=0.3,
        )
        ax_candle.add_patch(rect_candle)

        # 3. 볼륨차트
        ax_volume = fig.add_subplot(gs[2])
        volume_data = self.merged_df["Volume"]

        # 상승/하락 거래량 색상 구분
        colors = np.where(
            self.merged_df["Close"] >= self.merged_df["Open"], "#4dff4d", "#ff4d4d"
        )
        ax_volume.bar(
            range(len(volume_data)), volume_data, color=colors, alpha=0.7, width=0.8
        )

        # 볼륨차트 설정
        ax_volume.set_xlim(-0.5, n_dates - 0.5)
        ax_volume.grid(True, alpha=0.3)
        ax_volume.set_ylabel("Volume", fontsize=10)

        # 볼륨 차트의 y축 범위 설정
        min_volume = volume_data.min()
        max_volume = volume_data.max()
        volume_margin = (max_volume - min_volume) * 0.1
        ax_volume.set_ylim(min_volume - volume_margin, max_volume + volume_margin)

        # 볼륨차트 마지막 날짜 음영 처리
        rect_volume = plt.Rectangle(
            (n_dates - 1.5, ax_volume.get_ylim()[0]),
            1,
            ax_volume.get_ylim()[1] - ax_volume.get_ylim()[0],
            facecolor="yellow",
            alpha=0.3,
        )
        ax_volume.add_patch(rect_volume)

        # x축 레이블 설정
        ax_volume.set_xticks(range(n_dates))
        date_labels = [
            date.strftime("%Y-%m-%d") if i == 0 else date.strftime("%d")
            for i, date in enumerate(dates)
        ]
        ax_volume.set_xticklabels(date_labels, rotation=45, ha="right")

        # 타이틀 설정
        if len(dates) > 0:
            title = (
                f"Trading Signals Analysis Dashboard\n"
                f'{dates[0].strftime("%Y-%m-%d")} ~ {dates[-1].strftime("%Y-%m-%d")}'
            )
            fig.suptitle(title, fontsize=12, y=0.95)

        self.fig = fig

    def save_dashboard(self) -> None:
        """대시보드를 파일로 저장합니다."""
        try:
            # 디렉토리가 없으면 생성
            self.output_file.parent.mkdir(parents=True, exist_ok=True)

            # 저장
            self.fig.savefig(self.output_file, bbox_inches="tight", dpi=300)
            plt.close(self.fig)
            logger.info(f"대시보드 저장 완료: {self.output_file}")

        except Exception as e:
            logger.error(f"대시보드 저장 실패: {str(e)}")
            raise


if __name__ == "__main__":
    # 시각화 실행
    visualizer = TradingVisualizer()
    visualizer.create_dashboard(last_n_trading_days=20)
    visualizer.save_dashboard()
