"""
기술적 지표 계산 모듈
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from config import INDICATORS_FILE, SPY_DATA_FILE, TECHNICAL_INDICATORS

logger = logging.getLogger(__name__)


class TechnicalIndicator:
    """기술적 지표 계산 클래스"""

    def __init__(
        self,
        data_file: Path = SPY_DATA_FILE,
        output_file: Path = INDICATORS_FILE,
    ):
        """
        Args:
            data_file (Path): OHLCV 데이터 파일 경로
            output_file (Path): 출력 파일 경로
        """
        self.data_file = data_file
        self.output_file = output_file
        self.df = None
        self.indicators_df = None
        self._load_data()

    def _load_data(self) -> None:
        """데이터를 로드합니다."""
        try:
            self.df = pd.read_csv(self.data_file)
            self.df["Date"] = pd.to_datetime(self.df["Date"])
            logger.info("OHLCV 데이터 로드 완료")
        except Exception as e:
            logger.error(f"OHLCV 데이터 로드 실패: {str(e)}")
            raise

    def calculate_all(self) -> None:
        """모든 기술적 지표를 계산합니다."""
        try:
            # 지표 데이터프레임 초기화
            self.indicators_df = pd.DataFrame({"Date": self.df["Date"]})

            # OHLCV 데이터 추가
            self.indicators_df["Open"] = self.df["Open"]
            self.indicators_df["High"] = self.df["High"]
            self.indicators_df["Low"] = self.df["Low"]
            self.indicators_df["Close"] = self.df["Close"]
            self.indicators_df["Volume"] = self.df["Volume"]

            # 모멘텀 지표 계산
            self._calculate_momentum_indicators()

            # 반대매매 지표 계산
            self._calculate_contrarian_indicators()

            # 지표 정렬
            self.indicators_df = self.indicators_df.sort_values("Date")
            logger.info("기술적 지표 계산 완료")

        except Exception as e:
            logger.error(f"기술적 지표 계산 실패: {str(e)}")
            raise

    def _calculate_momentum_indicators(self) -> None:
        """모멘텀 지표를 계산합니다."""
        # SMA
        for period in TECHNICAL_INDICATORS["모멘텀 지표"]["SMA"]["periods"]:
            self.indicators_df[f"SMA_{period}"] = self._calculate_sma(period)

        # EMA
        for period in TECHNICAL_INDICATORS["모멘텀 지표"]["EMA"]["periods"]:
            self.indicators_df[f"EMA_{period}"] = self._calculate_ema(period)

        # TSI
        short_period = TECHNICAL_INDICATORS["모멘텀 지표"]["TSI"]["short_period"]
        long_period = TECHNICAL_INDICATORS["모멘텀 지표"]["TSI"]["long_period"]
        self._calculate_tsi(short_period, long_period)

        # MACD
        short_period = TECHNICAL_INDICATORS["모멘텀 지표"]["MACD"]["short_period"]
        long_period = TECHNICAL_INDICATORS["모멘텀 지표"]["MACD"]["long_period"]
        signal_period = TECHNICAL_INDICATORS["모멘텀 지표"]["MACD"]["signal_period"]
        self._calculate_macd(short_period, long_period, signal_period)

        # PSAR
        af_start = TECHNICAL_INDICATORS["모멘텀 지표"]["PSAR"]["af_start"]
        af_increment = TECHNICAL_INDICATORS["모멘텀 지표"]["PSAR"]["af_increment"]
        af_max = TECHNICAL_INDICATORS["모멘텀 지표"]["PSAR"]["af_max"]
        self.indicators_df[f"PSAR({af_start},{af_increment},{af_max})"] = (
            self._calculate_psar(af_start, af_increment, af_max)
        )

        # ADX
        period = TECHNICAL_INDICATORS["모멘텀 지표"]["ADX"]["period"]
        self._calculate_adx(period)

        # Aroon
        period = TECHNICAL_INDICATORS["모멘텀 지표"]["Aroon"]["period"]
        self._calculate_aroon(period)

        # ADL
        period = TECHNICAL_INDICATORS["모멘텀 지표"]["ADL"]["period"]
        self._calculate_adl(period)

        # ADR
        period = TECHNICAL_INDICATORS["모멘텀 지표"]["ADR"]["period"]
        self._calculate_adr(period)

        # Ichimoku
        tenkan_period = TECHNICAL_INDICATORS["모멘텀 지표"]["Ichimoku"]["tenkan_period"]
        kijun_period = TECHNICAL_INDICATORS["모멘텀 지표"]["Ichimoku"]["kijun_period"]
        self._calculate_ichimoku(tenkan_period, kijun_period)

        # Keltner
        period = TECHNICAL_INDICATORS["모멘텀 지표"]["Keltner"]["period"]
        multiplier = TECHNICAL_INDICATORS["모멘텀 지표"]["Keltner"]["multiplier"]
        self._calculate_keltner(period, multiplier)

    def _calculate_contrarian_indicators(self) -> None:
        """반대매매 지표를 계산합니다."""
        # RSI
        period = TECHNICAL_INDICATORS["반대매매 지표"]["RSI"]["period"]
        self.indicators_df[f"RSI({period})"] = self._calculate_rsi(period)

        # BB
        period = TECHNICAL_INDICATORS["반대매매 지표"]["BB"]["period"]
        std_dev = TECHNICAL_INDICATORS["반대매매 지표"]["BB"]["std_dev"]
        self._calculate_bb(period, std_dev)

        # CCI
        period = TECHNICAL_INDICATORS["반대매매 지표"]["CCI"]["period"]
        self.indicators_df[f"CCI({period})"] = self._calculate_cci(period)

        # Stoch
        k_period = TECHNICAL_INDICATORS["반대매매 지표"]["Stoch"]["k_period"]
        d_period = TECHNICAL_INDICATORS["반대매매 지표"]["Stoch"]["d_period"]
        self._calculate_stoch(k_period, d_period)

        # Williams
        period = TECHNICAL_INDICATORS["반대매매 지표"]["Williams"]["period"]
        self.indicators_df[f"Williams({period})"] = self._calculate_williams(period)

        # CMO
        period = TECHNICAL_INDICATORS["반대매매 지표"]["CMO"]["period"]
        self.indicators_df[f"CMO({period})"] = self._calculate_cmo(period)

        # DeMarker
        period = TECHNICAL_INDICATORS["반대매매 지표"]["DeMarker"]["period"]
        self.indicators_df[f"DeMarker({period})"] = self._calculate_demarker(period)

        # Donchian
        period = TECHNICAL_INDICATORS["반대매매 지표"]["Donchian"]["period"]
        self._calculate_donchian(period)

        # Pivot
        method = TECHNICAL_INDICATORS["반대매매 지표"]["Pivot"]["method"]
        self._calculate_pivot(method)

        # PSY
        period = TECHNICAL_INDICATORS["반대매매 지표"]["PSY"]["period"]
        self.indicators_df[f"PSY({period})"] = self._calculate_psy(period)

        # NPSY
        period = TECHNICAL_INDICATORS["반대매매 지표"]["NPSY"]["period"]
        self.indicators_df[f"NPSY({period})"] = self._calculate_npsy(period)

    def _calculate_sma(self, period: int) -> pd.Series:
        """단순 이동평균을 계산합니다."""
        return self.df["Close"].rolling(window=period).mean()

    def _calculate_ema(self, period: int) -> pd.Series:
        """지수 이동평균을 계산합니다."""
        return self.df["Close"].ewm(span=period, adjust=False).mean()

    def _calculate_tsi(self, short_period: int, long_period: int) -> None:
        """True Strength Index를 계산합니다.

        수식:
        - 가격 변화 = 현재 종가 - 이전 종가
        - 이중 지수 이동평균 = EMA(EMA(가격 변화, 25), 13)
        - 이중 지수 이동평균 절대값 = EMA(EMA(|가격 변화|, 25), 13)
        - TSI = 100 * (이중 지수 이동평균 / 이중 지수 이동평균 절대값)
        """
        # 가격 변화
        price_change = self.df["Close"].diff()
        abs_price_change = abs(price_change)

        # 이중 지수 이동평균
        tsi = 100 * (
            price_change.ewm(span=long_period, adjust=False)
            .mean()
            .ewm(span=short_period, adjust=False)
            .mean()
            / abs_price_change.ewm(span=long_period, adjust=False)
            .mean()
            .ewm(span=short_period, adjust=False)
            .mean()
        )
        signal = tsi.ewm(span=short_period, adjust=False).mean()

        self.indicators_df[f"TSI({short_period},{long_period})"] = tsi
        self.indicators_df[f"TSI_Signal({short_period},{long_period})"] = signal

    def _calculate_macd(
        self, short_period: int, long_period: int, signal_period: int
    ) -> None:
        """MACD를 계산합니다.

        수식:
        - MACD 라인 = EMA(12) - EMA(26)
        - 시그널 라인 = EMA(MACD 라인, 9)
        - 히스토그램 = MACD 라인 - 시그널 라인
        """
        # MACD 라인
        macd = (
            self.df["Close"].ewm(span=short_period, adjust=False).mean()
            - self.df["Close"].ewm(span=long_period, adjust=False).mean()
        )
        # 시그널 라인
        signal = macd.ewm(span=signal_period, adjust=False).mean()
        # 히스토그램
        hist = macd - signal

        self.indicators_df[f"MACD({short_period},{long_period})"] = macd
        self.indicators_df[
            f"MACD_Signal({short_period},{long_period},{signal_period})"
        ] = signal
        self.indicators_df[
            f"MACD_Hist({short_period},{long_period},{signal_period})"
        ] = hist

    def _calculate_psar(
        self, af_start: float, af_increment: float, af_max: float
    ) -> pd.Series:
        """Parabolic SAR을 계산합니다."""
        high = self.df["High"]
        low = self.df["Low"]
        close = self.df["Close"]

        psar = close.copy()
        trend = pd.Series(1, index=close.index)
        af = af_start
        ep = high[0]
        psar[0] = low[0]

        for i in range(1, len(close)):
            if trend[i - 1] == 1:
                psar[i] = psar[i - 1] + af * (ep - psar[i - 1])
                psar[i] = min(psar[i], low[i - 1], low[i - 2] if i > 1 else low[i - 1])
                if close[i] > ep:
                    ep = close[i]
                    af = min(af + af_increment, af_max)
                if close[i] < psar[i]:
                    trend[i] = -1
                    psar[i] = ep
                    ep = low[i]
                    af = af_start
                else:
                    trend[i] = 1
            else:
                psar[i] = psar[i - 1] - af * (psar[i - 1] - ep)
                psar[i] = max(
                    psar[i], high[i - 1], high[i - 2] if i > 1 else high[i - 1]
                )
                if close[i] < ep:
                    ep = close[i]
                    af = min(af + af_increment, af_max)
                if close[i] > psar[i]:
                    trend[i] = 1
                    psar[i] = ep
                    ep = high[i]
                    af = af_start
                else:
                    trend[i] = -1

        return psar

    def _calculate_adx(self, period: int) -> None:
        """Average Directional Index를 계산합니다.

        수식:
        - True Range = max(고가-저가, |고가-이전종가|, |저가-이전종가|)
        - +DM = max(고가-이전고가, 0)
        - -DM = max(이전저가-저가, 0)
        - +DI = 100 * EMA(+DM, 14) / EMA(TR, 14)
        - -DI = 100 * EMA(-DM, 14) / EMA(TR, 14)
        - DX = 100 * |+DI - -DI| / (+DI + -DI)
        - ADX = EMA(DX, 14)
        """
        high = self.df["High"]
        low = self.df["Low"]
        close = self.df["Close"]

        # True Range
        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()

        # Plus/Minus Directional Movement
        up_move = high - high.shift(1)
        down_move = low.shift(1) - low

        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)

        plus_di = (
            100
            * pd.Series(plus_dm, index=close.index).rolling(window=period).mean()
            / atr
        )
        minus_di = (
            100
            * pd.Series(minus_dm, index=close.index).rolling(window=period).mean()
            / atr
        )

        # ADX
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(window=period).mean()

        self.indicators_df[f"ADX({period})"] = adx
        self.indicators_df[f"ADX_Plus_DI({period})"] = plus_di
        self.indicators_df[f"ADX_Minus_DI({period})"] = minus_di

    def _calculate_aroon(self, period: int) -> None:
        """Aroon 지표를 계산합니다.

        수식:
        - Aroon Up = 100 * (기간 - 최근 고가까지의 기간) / 기간
        - Aroon Down = 100 * (기간 - 최근 저가까지의 기간) / 기간
        """
        high = self.df["High"]
        low = self.df["Low"]

        # Aroon Up
        rolling_max = high.rolling(window=period).max()
        aroon_up = 100 * (period - (high == rolling_max).cumsum()) / period

        # Aroon Down
        rolling_min = low.rolling(window=period).min()
        aroon_down = 100 * (period - (low == rolling_min).cumsum()) / period

        self.indicators_df[f"Aroon_Up({period})"] = aroon_up
        self.indicators_df[f"Aroon_Down({period})"] = aroon_down

    def _calculate_adl(self, period: int) -> None:
        """Accumulation/Distribution Line을 계산합니다.

        수식:
        - Money Flow Multiplier = ((종가-저가)-(고가-종가)) / (고가-저가)
        - Money Flow Volume = Money Flow Multiplier * 거래량
        - ADL = Money Flow Volume의 누적합
        """
        high = self.df["High"]
        low = self.df["Low"]
        close = self.df["Close"]
        volume = self.df["Volume"]

        # Money Flow Multiplier
        mfm = ((close - low) - (high - close)) / (high - low)
        mfm = mfm.replace([np.inf, -np.inf], 0)

        # Money Flow Volume
        mfv = mfm * volume

        # ADL
        adl = mfv.cumsum()
        adl_sma = adl.rolling(window=period).mean()

        self.indicators_df[f"ADL({period})"] = adl
        self.indicators_df[f"ADL_SMA({period})"] = adl_sma

    def _calculate_adr(self, period: int) -> None:
        """Advance/Decline Ratio를 계산합니다."""
        close = self.df["Close"]
        volume = self.df["Volume"]

        # 가격 변화
        price_change = close.diff()

        # 상승/하락 거래량
        up_volume = volume.where(price_change > 0, 0)
        down_volume = volume.where(price_change < 0, 0)

        # ADR
        adr = (
            up_volume.rolling(window=period).sum()
            / down_volume.rolling(window=period).sum()
        )
        adr_sma = adr.rolling(window=period).mean()

        self.indicators_df[f"ADR({period})"] = adr
        self.indicators_df[f"ADR_SMA({period})"] = adr_sma

    def _calculate_ichimoku(self, tenkan_period: int, kijun_period: int) -> None:
        """일목균형표를 계산합니다."""
        high = self.df["High"]
        low = self.df["Low"]

        # Tenkan-sen (Conversion Line)
        period_high = high.rolling(window=tenkan_period).max()
        period_low = low.rolling(window=tenkan_period).min()
        tenkan = (period_high + period_low) / 2

        # Kijun-sen (Base Line)
        period_high = high.rolling(window=kijun_period).max()
        period_low = low.rolling(window=kijun_period).min()
        kijun = (period_high + period_low) / 2

        self.indicators_df[f"Ichimoku_Tenkan({tenkan_period})"] = tenkan
        self.indicators_df[f"Ichimoku_Kijun({kijun_period})"] = kijun

    def _calculate_keltner(self, period: int, multiplier: float) -> None:
        """Keltner Channel을 계산합니다."""
        close = self.df["Close"]
        high = self.df["High"]
        low = self.df["Low"]

        # EMA
        ema = close.ewm(span=period, adjust=False).mean()

        # ATR
        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()

        # Keltner Channel
        upper = ema + multiplier * atr
        lower = ema - multiplier * atr

        self.indicators_df[f"Keltner_Upper({period},{multiplier})"] = upper
        self.indicators_df[f"Keltner_Lower({period},{multiplier})"] = lower

    def _calculate_rsi(self, period: int) -> pd.Series:
        """Relative Strength Index를 계산합니다.

        수식:
        - 가격 변화 = 현재 종가 - 이전 종가
        - 상승 평균 = EMA(상승 변화, 14)
        - 하락 평균 = EMA(하락 변화, 14)
        - RS = 상승 평균 / 하락 평균
        - RSI = 100 - (100 / (1 + RS))
        """
        close = self.df["Close"]

        # 가격 변화
        delta = close.diff()

        # 상승/하락 평균
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        # RSI
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def _calculate_bb(self, period: int, std_dev: float) -> None:
        """Bollinger Bands를 계산합니다.

        수식:
        - 중간 밴드 = SMA(종가, 20)
        - 표준편차 = 종가의 20일 표준편차
        - 상단 밴드 = 중간 밴드 + (2 * 표준편차)
        - 하단 밴드 = 중간 밴드 - (2 * 표준편차)
        """
        close = self.df["Close"]

        # 중간 밴드 (SMA)
        middle = close.rolling(window=period).mean()

        # 표준편차
        std = close.rolling(window=period).std()

        # 상단/하단 밴드
        upper = middle + (std_dev * std)
        lower = middle - (std_dev * std)

        self.indicators_df[f"BB_Upper({period},{std_dev})"] = upper
        self.indicators_df[f"BB_Lower({period},{std_dev})"] = lower

    def _calculate_cci(self, period: int) -> pd.Series:
        """Commodity Channel Index를 계산합니다.

        수식:
        - Typical Price = (고가 + 저가 + 종가) / 3
        - TP의 이동평균 = SMA(Typical Price, 20)
        - Mean Absolute Deviation = |TP - TP의 이동평균|의 20일 평균
        - CCI = (TP - TP의 이동평균) / (0.015 * Mean Absolute Deviation)
        """
        high = self.df["High"]
        low = self.df["Low"]
        close = self.df["Close"]

        # Typical Price
        tp = (high + low + close) / 3

        # SMA of TP
        tp_sma = tp.rolling(window=period).mean()

        # Mean Absolute Deviation
        mad = tp.rolling(window=period).apply(lambda x: abs(x - x.mean()).mean())

        # CCI
        cci = (tp - tp_sma) / (0.015 * mad)

        return cci

    def _calculate_stoch(self, k_period: int, d_period: int) -> None:
        """Stochastic Oscillator를 계산합니다.

        수식:
        - %K = 100 * (현재 종가 - 최저가) / (최고가 - 최저가)
        - %D = SMA(%K, 3)
        """
        high = self.df["High"]
        low = self.df["Low"]
        close = self.df["Close"]

        # %K
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()
        k = 100 * (close - lowest_low) / (highest_high - lowest_low)

        # %D
        d = k.rolling(window=d_period).mean()

        self.indicators_df[f"Stoch_K({k_period})"] = k
        self.indicators_df[f"Stoch_D({k_period},{d_period})"] = d

    def _calculate_williams(self, period: int) -> pd.Series:
        """Williams %R을 계산합니다.

        수식:
        - Williams %R = -100 * (최고가 - 현재 종가) / (최고가 - 최저가)
        """
        high = self.df["High"]
        low = self.df["Low"]
        close = self.df["Close"]

        # Highest High
        highest_high = high.rolling(window=period).max()

        # Lowest Low
        lowest_low = low.rolling(window=period).min()

        # Williams %R
        williams = -100 * (highest_high - close) / (highest_high - lowest_low)

        return williams

    def _calculate_cmo(self, period: int) -> pd.Series:
        """Chande Momentum Oscillator를 계산합니다.

        수식:
        - 상승 합계 = 상승 변화의 14일 합계
        - 하락 합계 = 하락 변화의 14일 합계
        - CMO = 100 * (상승 합계 - 하락 합계) / (상승 합계 + 하락 합계)
        """
        close = self.df["Close"]

        # 가격 변화
        delta = close.diff()

        # 상승/하락 합계
        up_sum = delta.where(delta > 0, 0).rolling(window=period).sum()
        down_sum = -delta.where(delta < 0, 0).rolling(window=period).sum()

        # CMO
        cmo = 100 * (up_sum - down_sum) / (up_sum + down_sum)

        return cmo

    def _calculate_demarker(self, period: int) -> pd.Series:
        """DeMarker를 계산합니다.

        수식:
        - DeMax = max(고가 - 이전고가, 0)
        - DeMin = max(이전저가 - 저가, 0)
        - DeMarker = DeMax의 14일 합계 / (DeMax의 14일 합계 + DeMin의 14일 합계)
        """
        high = self.df["High"]
        low = self.df["Low"]

        # DeMax
        demax = high - high.shift(1)
        demax = demax.where(demax > 0, 0)

        # DeMin
        demin = low.shift(1) - low
        demin = demin.where(demin > 0, 0)

        # DeMarker
        demarker = demax.rolling(window=period).sum() / (
            demax.rolling(window=period).sum() + demin.rolling(window=period).sum()
        )

        return demarker

    def _calculate_donchian(self, period: int) -> None:
        """Donchian Channel을 계산합니다."""
        high = self.df["High"]
        low = self.df["Low"]

        # Upper/Lower Bands
        upper = high.rolling(window=period).max()
        lower = low.rolling(window=period).min()

        self.indicators_df[f"Donchian_Upper({period})"] = upper
        self.indicators_df[f"Donchian_Lower({period})"] = lower

    def _calculate_pivot(self, method: str) -> None:
        """Pivot Points를 계산합니다."""
        high = self.df["High"]
        low = self.df["Low"]
        close = self.df["Close"]

        # Pivot Point
        pivot = (high + low + close) / 3

        # Support/Resistance Levels
        r1 = 2 * pivot - low
        s1 = 2 * pivot - high

        self.indicators_df[f"Pivot_R1({method})"] = r1
        self.indicators_df[f"Pivot_S1({method})"] = s1

    def _calculate_psy(self, period: int) -> pd.Series:
        """Psychological Line을 계산합니다.

        수식:
        - 상승일 비율 = (상승일 수 / 기간) * 100
        """
        close = self.df["Close"]

        # 가격 변화
        price_change = close.diff()

        # 상승일 비율
        psy = 100 * (price_change > 0).rolling(window=period).mean()

        return psy

    def _calculate_npsy(self, period: int) -> pd.Series:
        """Negative Psychological Line을 계산합니다.

        수식:
        - 하락일 비율 = (하락일 수 / 기간) * 100
        """
        close = self.df["Close"]

        # 가격 변화
        price_change = close.diff()

        # 하락일 비율
        npsy = 100 * (price_change < 0).rolling(window=period).mean()

        return npsy

    def save_indicators(self) -> None:
        """지표를 파일로 저장합니다."""
        try:
            # 디렉토리가 없으면 생성
            self.output_file.parent.mkdir(parents=True, exist_ok=True)

            # 저장
            self.indicators_df.to_csv(self.output_file, index=False)
            logger.info(f"지표 저장 완료: {self.output_file}")

        except Exception as e:
            logger.error(f"지표 저장 실패: {str(e)}")
            raise


if __name__ == "__main__":
    # 지표 계산 실행
    indicator = TechnicalIndicator()
    indicator.calculate_all()
    indicator.save_indicators()
