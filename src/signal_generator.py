"""
매매 시그널 생성 모듈

이 모듈은 기술적 지표 데이터를 기반으로 매매 시그널을 생성합니다.
생성되는 시그널은 다음과 같은 의미를 가집니다:
- 1: 매수 시그널
- -1: 매도 시그널
- 0: 중립 시그널
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from config import INDICATORS_FILE, SIGNALS_FILE, TECHNICAL_INDICATORS, SIGNAL_THRESHOLDS

logger = logging.getLogger(__name__)


class SignalGenerator:
    """매매 시그널 생성 클래스"""

    def __init__(
        self,
        indicators_file: Path = INDICATORS_FILE,
        output_file: Path = SIGNALS_FILE,
    ):
        """
        Args:
            indicators_file (Path): 기술적 지표 데이터 파일 경로
            output_file (Path): 출력 파일 경로
        """
        self.indicators_file = indicators_file
        self.output_file = output_file
        self.indicators_df = None
        self.signals_df = None
        self._load_data()

    def _load_data(self) -> None:
        """데이터를 로드합니다."""
        try:
            self.indicators_df = pd.read_csv(self.indicators_file)
            self.indicators_df["Date"] = pd.to_datetime(self.indicators_df["Date"])
            logger.info("기술적 지표 데이터 로드 완료")
        except Exception as e:
            logger.error(f"기술적 지표 데이터 로드 실패: {str(e)}")
            raise

    def generate_all(self) -> None:
        """모든 매매 시그널을 생성합니다."""
        try:
            # 시그널 데이터프레임 초기화
            self.signals_df = pd.DataFrame({"Date": self.indicators_df["Date"]})

            # 모멘텀 지표 시그널
            self._generate_momentum_signals()

            # 반대매매 지표 시그널
            self._generate_contrarian_signals()

            # 시그널 정렬
            self.signals_df = self.signals_df.sort_values("Date")
            logger.info("매매 시그널 생성 완료")

        except Exception as e:
            logger.error(f"매매 시그널 생성 실패: {str(e)}")
            raise

    def _generate_momentum_signals(self) -> None:
        """모멘텀 지표 기반 시그널을 생성합니다."""
        # SMA
        for period in TECHNICAL_INDICATORS["모멘텀 지표"]["SMA"]["periods"]:
            self.signals_df[f"SMA_{period}_Signal"] = self._generate_sma_signal(period)

        # EMA
        for period in TECHNICAL_INDICATORS["모멘텀 지표"]["EMA"]["periods"]:
            self.signals_df[f"EMA_{period}_Signal"] = self._generate_ema_signal(period)

        # TSI
        short_period = TECHNICAL_INDICATORS["모멘텀 지표"]["TSI"]["short_period"]
        long_period = TECHNICAL_INDICATORS["모멘텀 지표"]["TSI"]["long_period"]
        self.signals_df[f"TSI({short_period},{long_period})_Signal"] = self._generate_tsi_signal(short_period, long_period)

        # MACD
        short_period = TECHNICAL_INDICATORS["모멘텀 지표"]["MACD"]["short_period"]
        long_period = TECHNICAL_INDICATORS["모멘텀 지표"]["MACD"]["long_period"]
        signal_period = TECHNICAL_INDICATORS["모멘텀 지표"]["MACD"]["signal_period"]
        self.signals_df[f"MACD({short_period},{long_period},{signal_period})_Signal"] = self._generate_macd_signal(
            short_period, long_period, signal_period
        )

        # PSAR
        af_start = TECHNICAL_INDICATORS["모멘텀 지표"]["PSAR"]["af_start"]
        af_increment = TECHNICAL_INDICATORS["모멘텀 지표"]["PSAR"]["af_increment"]
        af_max = TECHNICAL_INDICATORS["모멘텀 지표"]["PSAR"]["af_max"]
        self.signals_df[f"PSAR({af_start},{af_increment},{af_max})_Signal"] = self._generate_psar_signal(
            af_start, af_increment, af_max
        )

        # ADX
        period = TECHNICAL_INDICATORS["모멘텀 지표"]["ADX"]["period"]
        self.signals_df[f"ADX({period})_Signal"] = self._generate_adx_signal(period)

        # Aroon
        period = TECHNICAL_INDICATORS["모멘텀 지표"]["Aroon"]["period"]
        self.signals_df[f"Aroon({period})_Signal"] = self._generate_aroon_signal(period)

        # ADL
        period = TECHNICAL_INDICATORS["모멘텀 지표"]["ADL"]["period"]
        self.signals_df[f"ADL({period})_Signal"] = self._generate_adl_signal(period)

        # ADR
        period = TECHNICAL_INDICATORS["모멘텀 지표"]["ADR"]["period"]
        self.signals_df[f"ADR({period})_Signal"] = self._generate_adr_signal(period)

        # Ichimoku
        tenkan_period = TECHNICAL_INDICATORS["모멘텀 지표"]["Ichimoku"]["tenkan_period"]
        kijun_period = TECHNICAL_INDICATORS["모멘텀 지표"]["Ichimoku"]["kijun_period"]
        self.signals_df[f"Ichimoku({tenkan_period},{kijun_period})_Signal"] = self._generate_ichimoku_signal(
            tenkan_period, kijun_period
        )

        # Keltner
        period = TECHNICAL_INDICATORS["모멘텀 지표"]["Keltner"]["period"]
        multiplier = TECHNICAL_INDICATORS["모멘텀 지표"]["Keltner"]["multiplier"]
        self.signals_df[f"Keltner({period},{multiplier})_Signal"] = self._generate_keltner_signal(period, multiplier)

    def _generate_contrarian_signals(self) -> None:
        """반대매매 지표 기반 시그널을 생성합니다."""
        # RSI
        period = TECHNICAL_INDICATORS["반대매매 지표"]["RSI"]["period"]
        self.signals_df[f"RSI({period})_Signal"] = self._generate_rsi_signal(period)

        # BB
        period = TECHNICAL_INDICATORS["반대매매 지표"]["BB"]["period"]
        std_dev = TECHNICAL_INDICATORS["반대매매 지표"]["BB"]["std_dev"]
        self.signals_df[f"BB({period},{std_dev})_Signal"] = self._generate_bb_signal(period, std_dev)

        # CCI
        period = TECHNICAL_INDICATORS["반대매매 지표"]["CCI"]["period"]
        self.signals_df[f"CCI({period})_Signal"] = self._generate_cci_signal(period)

        # Stoch
        k_period = TECHNICAL_INDICATORS["반대매매 지표"]["Stoch"]["k_period"]
        d_period = TECHNICAL_INDICATORS["반대매매 지표"]["Stoch"]["d_period"]
        self.signals_df[f"Stoch({k_period},{d_period})_Signal"] = self._generate_stoch_signal(k_period, d_period)

        # Williams
        period = TECHNICAL_INDICATORS["반대매매 지표"]["Williams"]["period"]
        self.signals_df[f"Williams({period})_Signal"] = self._generate_williams_signal(period)

        # CMO
        period = TECHNICAL_INDICATORS["반대매매 지표"]["CMO"]["period"]
        self.signals_df[f"CMO({period})_Signal"] = self._generate_cmo_signal(period)

        # DeMarker
        period = TECHNICAL_INDICATORS["반대매매 지표"]["DeMarker"]["period"]
        self.signals_df[f"DeMarker({period})_Signal"] = self._generate_demarker_signal(period)

        # Donchian
        period = TECHNICAL_INDICATORS["반대매매 지표"]["Donchian"]["period"]
        self.signals_df[f"Donchian({period})_Signal"] = self._generate_donchian_signal(period)

        # Pivot
        method = TECHNICAL_INDICATORS["반대매매 지표"]["Pivot"]["method"]
        self.signals_df[f"Pivot({method})_Signal"] = self._generate_pivot_signal(method)

        # PSY
        period = TECHNICAL_INDICATORS["반대매매 지표"]["PSY"]["period"]
        self.signals_df[f"PSY({period})_Signal"] = self._generate_psy_signal(period)

        # NPSY
        period = TECHNICAL_INDICATORS["반대매매 지표"]["NPSY"]["period"]
        self.signals_df[f"NPSY({period})_Signal"] = self._generate_npsy_signal(period)

    def _generate_sma_signal(self, period: int) -> pd.Series:
        """SMA 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: 현재 종가 > SMA
        - 매도: 현재 종가 < SMA
        - 중립: 그 외
        """
        close = self.indicators_df["Close"]
        sma = self.indicators_df[f"SMA_{period}"]

        signal = pd.Series(0, index=close.index)
        signal[close > sma] = 1
        signal[close < sma] = -1

        return signal

    def _generate_ema_signal(self, period: int) -> pd.Series:
        """EMA 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: 현재 종가 > EMA
        - 매도: 현재 종가 < EMA
        - 중립: 그 외
        """
        close = self.indicators_df["Close"]
        ema = self.indicators_df[f"EMA_{period}"]

        signal = pd.Series(0, index=close.index)
        signal[close > ema] = 1
        signal[close < ema] = -1

        return signal

    def _generate_tsi_signal(self, short_period: int, long_period: int) -> pd.Series:
        """TSI 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: TSI > TSI Signal
        - 매도: TSI < TSI Signal
        - 중립: 그 외
        """
        tsi = self.indicators_df[f"TSI({short_period},{long_period})"]
        tsi_signal = self.indicators_df[f"TSI_Signal({short_period},{long_period})"]

        signal = pd.Series(0, index=tsi.index)
        signal[tsi > tsi_signal] = 1
        signal[tsi < tsi_signal] = -1

        return signal

    def _generate_macd_signal(self, short_period: int, long_period: int, signal_period: int) -> pd.Series:
        """MACD 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: MACD > MACD Signal
        - 매도: MACD < MACD Signal
        - 중립: 그 외
        """
        macd = self.indicators_df[f"MACD({short_period},{long_period})"]
        macd_signal = self.indicators_df[f"MACD_Signal({short_period},{long_period},{signal_period})"]

        signal = pd.Series(0, index=macd.index)
        signal[macd > macd_signal] = 1
        signal[macd < macd_signal] = -1

        return signal

    def _generate_psar_signal(self, af_start: float, af_increment: float, af_max: float) -> pd.Series:
        """PSAR 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: 현재 종가 > PSAR
        - 매도: 현재 종가 < PSAR
        - 중립: 그 외
        """
        close = self.indicators_df["Close"]
        psar = self.indicators_df[f"PSAR({af_start},{af_increment},{af_max})"]

        signal = pd.Series(0, index=close.index)
        signal[close > psar] = 1
        signal[close < psar] = -1

        return signal

    def _generate_adx_signal(self, period: int) -> pd.Series:
        """ADX 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: ADX > 25 and +DI > -DI
        - 매도: ADX > 25 and +DI < -DI
        - 중립: 그 외
        """
        adx = self.indicators_df[f"ADX({period})"]
        plus_di = self.indicators_df[f"ADX_Plus_DI({period})"]
        minus_di = self.indicators_df[f"ADX_Minus_DI({period})"]

        signal = pd.Series(0, index=adx.index)
        signal[(adx > 25) & (plus_di > minus_di)] = 1
        signal[(adx > 25) & (plus_di < minus_di)] = -1

        return signal

    def _generate_aroon_signal(self, period: int) -> pd.Series:
        """Aroon 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: Aroon Up > Aroon Down
        - 매도: Aroon Up < Aroon Down
        - 중립: 그 외
        """
        aroon_up = self.indicators_df[f"Aroon_Up({period})"]
        aroon_down = self.indicators_df[f"Aroon_Down({period})"]

        signal = pd.Series(0, index=aroon_up.index)
        signal[aroon_up > aroon_down] = 1
        signal[aroon_up < aroon_down] = -1

        return signal

    def _generate_adl_signal(self, period: int) -> pd.Series:
        """ADL 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: ADL > ADL SMA
        - 매도: ADL < ADL SMA
        - 중립: 그 외
        """
        adl = self.indicators_df[f"ADL({period})"]
        adl_sma = self.indicators_df[f"ADL_SMA({period})"]

        signal = pd.Series(0, index=adl.index)
        signal[adl > adl_sma] = 1
        signal[adl < adl_sma] = -1

        return signal

    def _generate_adr_signal(self, period: int) -> pd.Series:
        """ADR 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: ADR > ADR SMA
        - 매도: ADR < ADR SMA
        - 중립: 그 외
        """
        adr = self.indicators_df[f"ADR({period})"]
        adr_sma = self.indicators_df[f"ADR_SMA({period})"]

        signal = pd.Series(0, index=adr.index)
        signal[adr > adr_sma] = 1
        signal[adr < adr_sma] = -1

        return signal

    def _generate_ichimoku_signal(self, tenkan_period: int, kijun_period: int) -> pd.Series:
        """Ichimoku 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: Tenkan-sen > Kijun-sen
        - 매도: Tenkan-sen < Kijun-sen
        - 중립: 그 외
        """
        tenkan = self.indicators_df[f"Ichimoku_Tenkan({tenkan_period})"]
        kijun = self.indicators_df[f"Ichimoku_Kijun({kijun_period})"]

        signal = pd.Series(0, index=tenkan.index)
        signal[tenkan > kijun] = 1
        signal[tenkan < kijun] = -1

        return signal

    def _generate_keltner_signal(self, period: int, multiplier: float) -> pd.Series:
        """Keltner Channel 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: 현재 종가 > 상단 밴드
        - 매도: 현재 종가 < 하단 밴드
        - 중립: 그 외
        """
        close = self.indicators_df["Close"]
        upper = self.indicators_df[f"Keltner_Upper({period},{multiplier})"]
        lower = self.indicators_df[f"Keltner_Lower({period},{multiplier})"]

        signal = pd.Series(0, index=close.index)
        signal[close > upper] = 1
        signal[close < lower] = -1

        return signal

    def _generate_rsi_signal(self, period: int) -> pd.Series:
        """RSI 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: RSI < 30
        - 매도: RSI > 70
        - 중립: 그 외
        """
        rsi = self.indicators_df[f"RSI({period})"]

        signal = pd.Series(0, index=rsi.index)
        signal[rsi < 30] = 1
        signal[rsi > 70] = -1

        return signal

    def _generate_bb_signal(self, period: int, std_dev: float) -> pd.Series:
        """Bollinger Bands 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: 현재 종가 < 하단 밴드
        - 매도: 현재 종가 > 상단 밴드
        - 중립: 그 외
        """
        close = self.indicators_df["Close"]
        upper = self.indicators_df[f"BB_Upper({period},{std_dev})"]
        lower = self.indicators_df[f"BB_Lower({period},{std_dev})"]

        signal = pd.Series(0, index=close.index)
        signal[close < lower] = 1
        signal[close > upper] = -1

        return signal

    def _generate_cci_signal(self, period: int) -> pd.Series:
        """CCI 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: CCI < -100
        - 매도: CCI > 100
        - 중립: 그 외
        """
        cci = self.indicators_df[f"CCI({period})"]

        signal = pd.Series(0, index=cci.index)
        signal[cci < -100] = 1
        signal[cci > 100] = -1

        return signal

    def _generate_stoch_signal(self, k_period: int, d_period: int) -> pd.Series:
        """Stochastic Oscillator 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: %K < 20 and %D < 20
        - 매도: %K > 80 and %D > 80
        - 중립: 그 외
        """
        k = self.indicators_df[f"Stoch_K({k_period})"]
        d = self.indicators_df[f"Stoch_D({k_period},{d_period})"]

        signal = pd.Series(0, index=k.index)
        signal[(k < 20) & (d < 20)] = 1
        signal[(k > 80) & (d > 80)] = -1

        return signal

    def _generate_williams_signal(self, period: int) -> pd.Series:
        """Williams %R 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: Williams %R < -80
        - 매도: Williams %R > -20
        - 중립: 그 외
        """
        williams = self.indicators_df[f"Williams({period})"]

        signal = pd.Series(0, index=williams.index)
        signal[williams < -80] = 1
        signal[williams > -20] = -1

        return signal

    def _generate_cmo_signal(self, period: int) -> pd.Series:
        """CMO 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: CMO < -50
        - 매도: CMO > 50
        - 중립: 그 외
        """
        cmo = self.indicators_df[f"CMO({period})"]

        signal = pd.Series(0, index=cmo.index)
        signal[cmo < -50] = 1
        signal[cmo > 50] = -1

        return signal

    def _generate_demarker_signal(self, period: int) -> pd.Series:
        """DeMarker 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: DeMarker < 0.2
        - 매도: DeMarker > 0.8
        - 중립: 그 외
        """
        demarker = self.indicators_df[f"DeMarker({period})"]

        signal = pd.Series(0, index=demarker.index)
        signal[demarker < 0.2] = 1
        signal[demarker > 0.8] = -1

        return signal

    def _generate_donchian_signal(self, period: int) -> pd.Series:
        """Donchian Channel 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: 현재 종가 > 상단 밴드
        - 매도: 현재 종가 < 하단 밴드
        - 중립: 그 외
        """
        close = self.indicators_df["Close"]
        upper = self.indicators_df[f"Donchian_Upper({period})"]
        lower = self.indicators_df[f"Donchian_Lower({period})"]

        signal = pd.Series(0, index=close.index)
        signal[close > upper] = 1
        signal[close < lower] = -1

        return signal

    def _generate_pivot_signal(self, method: str) -> pd.Series:
        """Pivot Points 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: 현재 종가 < S1
        - 매도: 현재 종가 > R1
        - 중립: 그 외
        """
        close = self.indicators_df["Close"]
        r1 = self.indicators_df[f"Pivot_R1({method})"]
        s1 = self.indicators_df[f"Pivot_S1({method})"]

        signal = pd.Series(0, index=close.index)
        signal[close < s1] = 1
        signal[close > r1] = -1

        return signal

    def _generate_psy_signal(self, period: int) -> pd.Series:
        """Psychological Line 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: PSY < 30
        - 매도: PSY > 70
        - 중립: 그 외
        """
        psy = self.indicators_df[f"PSY({period})"]

        signal = pd.Series(0, index=psy.index)
        signal[psy < 30] = 1
        signal[psy > 70] = -1

        return signal

    def _generate_npsy_signal(self, period: int) -> pd.Series:
        """Negative Psychological Line 시그널을 생성합니다.
        
        시그널 생성 로직:
        - 매수: NPSY < 30
        - 매도: NPSY > 70
        - 중립: 그 외
        """
        npsy = self.indicators_df[f"NPSY({period})"]

        signal = pd.Series(0, index=npsy.index)
        signal[npsy < 30] = 1
        signal[npsy > 70] = -1

        return signal

    def save_signals(self) -> None:
        """시그널을 파일로 저장합니다."""
        try:
            # 디렉토리가 없으면 생성
            self.output_file.parent.mkdir(parents=True, exist_ok=True)

            # 저장
            self.signals_df.to_csv(self.output_file, index=False)
            logger.info(f"매매 시그널 저장 완료: {self.output_file}")

        except Exception as e:
            logger.error(f"매매 시그널 저장 실패: {str(e)}")
            raise


if __name__ == "__main__":
    # 시그널 생성 실행
    generator = SignalGenerator()
    generator.generate_all()
    generator.save_signals()
