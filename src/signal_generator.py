import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class SignalGenerator:
    """기술적 지표 기반 매매 신호 생성기"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Args:
            data (pd.DataFrame): 기술적 지표가 포함된 데이터프레임
        """
        self.data = data
        
    def generate_sma_signals(self, window_size: int = 20) -> pd.Series:
        """단순이동평균(SMA) 신호 생성
        
        매수 신호: 종가가 SMA를 상향 돌파
        매도 신호: 종가가 SMA를 하향 돌파
        
        Args:
            window_size (int): 이동평균 기간
            
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        sma_col = f'SMA({window_size})'
        signals = pd.Series(0, index=self.data.index)
        
        # 상향/하향 돌파 계산
        signals[self.data['Close'] > self.data[sma_col]] = 1
        signals[self.data['Close'] < self.data[sma_col]] = -1
        
        # 당일 신호를 다음 거래일에 실행하도록 시프트
        return signals.shift(1)

    def generate_ema_signals(self, window_size: int = 20) -> pd.Series:
        """지수이동평균(EMA) 신호 생성
        
        매수 신호: 종가가 EMA를 상향 돌파
        매도 신호: 종가가 EMA를 하향 돌파
        
        Args:
            window_size (int): 이동평균 기간
            
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        ema_col = f'EMA({window_size})'
        signals = pd.Series(0, index=self.data.index)
        
        signals[self.data['Close'] > self.data[ema_col]] = 1
        signals[self.data['Close'] < self.data[ema_col]] = -1
        
        return signals.shift(1)

    def generate_tsi_signals(self) -> pd.Series:
        """True Strength Index (TSI) 신호 생성
        
        매수 신호: TSI가 0선을 상향 돌파
        매도 신호: TSI가 0선을 하향 돌파
        
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        tsi_col = 'TSI(2,20)'
        signals = pd.Series(0, index=self.data.index)
        
        signals[self.data[tsi_col] > 0] = 1
        signals[self.data[tsi_col] < 0] = -1
        
        return signals.shift(1)

    def generate_macd_signals(self) -> pd.Series:
        """MACD 신호 생성
        
        매수 신호: MACD가 시그널선을 상향 돌파
        매도 신호: MACD가 시그널선을 하향 돌파
        
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        signals = pd.Series(0, index=self.data.index)
        
        signals[self.data['MACD(12,26)'] > self.data['MACD Signal(9)']] = 1
        signals[self.data['MACD(12,26)'] < self.data['MACD Signal(9)']] = -1
        
        return signals.shift(1)

    def generate_psar_signals(self) -> pd.Series:
        """Parabolic SAR 신호 생성
        
        매수 신호: 종가가 PSAR을 상향 돌파
        매도 신호: 종가가 PSAR을 하향 돌파
        
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        psar_col = 'PSAR(0.02)'
        signals = pd.Series(0, index=self.data.index)
        
        signals[self.data['Close'] > self.data[psar_col]] = 1
        signals[self.data['Close'] < self.data[psar_col]] = -1
        
        return signals.shift(1)

    def generate_adx_signals(self, threshold: int = 25) -> pd.Series:
        """ADX 신호 생성
        
        매수 신호: ADX > threshold (강한 추세)
        매도 신호: ADX < threshold (약한 추세)
        
        Args:
            threshold (int): ADX 임계값
            
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        adx_col = 'ADX(20)'
        signals = pd.Series(0, index=self.data.index)
        
        signals[self.data[adx_col] > threshold] = 1
        signals[self.data[adx_col] < threshold] = -1
        
        return signals.shift(1)

    def generate_aroon_signals(self) -> pd.Series:
        """Aroon 신호 생성
        
        매수 신호: Aroon Up이 Aroon Down을 상향 돌파
        매도 신호: Aroon Up이 Aroon Down을 하향 돌파
        
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        signals = pd.Series(0, index=self.data.index)
        
        signals[self.data['Aroon(20) up'] > self.data['Aroon(20) down']] = 1
        signals[self.data['Aroon(20) up'] < self.data['Aroon(20) down']] = -1
        
        return signals.shift(1)

    def generate_rsi_signals(self, overbought: int = 70, oversold: int = 30) -> pd.Series:
        """RSI 신호 생성
        
        매수 신호: RSI < oversold (과매도)
        매도 신호: RSI > overbought (과매수)
        
        Args:
            overbought (int): 과매수 기준값
            oversold (int): 과매도 기준값
            
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        rsi_col = 'RSI(14)'
        signals = pd.Series(0, index=self.data.index)
        
        signals[self.data[rsi_col] < oversold] = 1
        signals[self.data[rsi_col] > overbought] = -1
        
        return signals.shift(1)

    def generate_bb_signals(self) -> pd.Series:
        """볼린저 밴드 신호 생성
        
        매수 신호: 종가가 하단 밴드 하향 돌파
        매도 신호: 종가가 상단 밴드 상향 돌파
        
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        signals = pd.Series(0, index=self.data.index)
        
        signals[self.data['Close'] < self.data['BB_DOWN(20)']] = 1
        signals[self.data['Close'] > self.data['BB_UP(20)']] = -1
        
        return signals.shift(1)

    def generate_cci_signals(self, overbought: int = 100, oversold: int = -100) -> pd.Series:
        """CCI 신호 생성
        
        매수 신호: CCI < oversold (과매도)
        매도 신호: CCI > overbought (과매수)
        
        Args:
            overbought (int): 과매수 기준값
            oversold (int): 과매도 기준값
            
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        cci_col = 'CCI(20)'
        signals = pd.Series(0, index=self.data.index)
        
        signals[self.data[cci_col] < oversold] = 1
        signals[self.data[cci_col] > overbought] = -1
        
        return signals.shift(1)

    def generate_stochastic_signals(self, overbought: int = 80, oversold: int = 20) -> pd.Series:
        """스토캐스틱 신호 생성
        
        매수 신호: %K가 %D를 상향 돌파하며 과매도 구간
        매도 신호: %K가 %D를 하향 돌파하며 과매수 구간
        
        Args:
            overbought (int): 과매수 기준값
            oversold (int): 과매도 기준값
            
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        k_col = 'stochastic_oscillator %K(14)'
        d_col = 'stochastic_oscillator %D(3)'
        signals = pd.Series(0, index=self.data.index)
        
        # 매수 신호: %K가 %D를 상향 돌파하며 과매도 구간
        buy_condition = (
            (self.data[k_col] > self.data[d_col]) & 
            (self.data[k_col] < oversold)
        )
        signals[buy_condition] = 1
        
        # 매도 신호: %K가 %D를 하향 돌파하며 과매수 구간
        sell_condition = (
            (self.data[k_col] < self.data[d_col]) & 
            (self.data[k_col] > overbought)
        )
        signals[sell_condition] = -1
        
        return signals.shift(1)

    def generate_williams_r_signals(self, overbought: int = -20, oversold: int = -80) -> pd.Series:
        """Williams %R 신호 생성
        
        매수 신호: Williams %R < oversold (과매도)
        매도 신호: Williams %R > overbought (과매수)
        
        Args:
            overbought (int): 과매수 기준값
            oversold (int): 과매도 기준값
            
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        williams_col = 'Williams(14)'
        signals = pd.Series(0, index=self.data.index)
        
        signals[self.data[williams_col] < oversold] = 1
        signals[self.data[williams_col] > overbought] = -1
        
        return signals.shift(1)

    def generate_cmo_signals(self, overbought: int = 50, oversold: int = -50) -> pd.Series:
        """Chande Momentum Oscillator (CMO) 신호 생성
        
        매수 신호: CMO < oversold (과매도)
        매도 신호: CMO > overbought (과매수)
        
        Args:
            overbought (int): 과매수 기준값
            oversold (int): 과매도 기준값
            
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        cmo_col = 'CMO(14)'
        signals = pd.Series(0, index=self.data.index)
        
        signals[self.data[cmo_col] < oversold] = 1
        signals[self.data[cmo_col] > overbought] = -1
        
        return signals.shift(1)

    def generate_demark_signals(self, threshold: float = 0.7) -> pd.Series:
        """DeMarker Indicator 신호 생성
        
        매수 신호: DeMarker < 0.3 (과매도)
        매도 신호: DeMarker > 0.7 (과매수)
        
        Args:
            threshold (float): 과매수/과매도 기준값
            
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        demark_col = 'DEMARK(14)'
        signals = pd.Series(0, index=self.data.index)
        
        signals[self.data[demark_col] < (1 - threshold)] = 1
        signals[self.data[demark_col] > threshold] = -1
        
        return signals.shift(1)

    def generate_donchian_signals(self) -> pd.Series:
        """Donchian Channel 신호 생성
        
        매수 신호: 
        1. 종가가 상단 밴드에 근접 (상단 밴드의 99% 이상)
        2. 이전 종가가 더 낮았을 때
        
        매도 신호: 
        1. 종가가 하단 밴드에 근접 (하단 밴드의 101% 이하)
        2. 이전 종가가 더 높았을 때
        
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        signals = pd.Series(0, index=self.data.index)
        
        # 상단/하단 밴드 근접 범위 설정
        upper_threshold = self.data['Donchian(20) up'] * 0.99
        lower_threshold = self.data['Donchian(20) down'] * 1.01
        
        # 매수 조건: 상단 밴드 근접 및 상승 추세
        buy_condition = (
            (self.data['Close'] >= upper_threshold) & 
            (self.data['Close'] > self.data['Close'].shift(1))
        )
        
        # 매도 조건: 하단 밴드 근접 및 하락 추세
        sell_condition = (
            (self.data['Close'] <= lower_threshold) & 
            (self.data['Close'] < self.data['Close'].shift(1))
        )
        
        signals[buy_condition] = 1
        signals[sell_condition] = -1
        
        return signals.shift(1)
    
    def generate_pivot_signals(self) -> pd.Series:
        """Pivot Points 신호 생성
        
        매수 신호: 종가가 지지선 근처에서 반등
        매도 신호: 종가가 저항선 근처에서 하락
        
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        signals = pd.Series(0, index=self.data.index)
        
        # 지지선/저항선 근처 범위 설정 (1% 이내)
        support_zone = self.data['Support'] * 1.01
        resistance_zone = self.data['Resistance'] * 0.99
        
        # 매수 신호: 종가가 지지선 근처에서 상승
        buy_condition = (
            (self.data['Close'] > self.data['Close'].shift(1)) & 
            (self.data['Close'] < support_zone)
        )
        signals[buy_condition] = 1
        
        # 매도 신호: 종가가 저항선 근처에서 하락
        sell_condition = (
            (self.data['Close'] < self.data['Close'].shift(1)) & 
            (self.data['Close'] > resistance_zone)
        )
        signals[sell_condition] = -1
        
        return signals.shift(1)

    def generate_psy_signals(self, overbought: int = 75, oversold: int = 25) -> pd.Series:
        """Psychological Line (PSY) 신호 생성
        
        매수 신호: PSY < oversold (과매도)
        매도 신호: PSY > overbought (과매수)
        
        Args:
            overbought (int): 과매수 기준값
            oversold (int): 과매도 기준값
            
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        psy_col = 'PSY(12)'
        signals = pd.Series(0, index=self.data.index)
        
        signals[self.data[psy_col] < oversold] = 1
        signals[self.data[psy_col] > overbought] = -1
        
        return signals.shift(1)

    def generate_npsy_signals(self, threshold: int = 50) -> pd.Series:
        """Normalized Psychological Line (NPSY) 신호 생성
        
        매수 신호: NPSY < -threshold
        매도 신호: NPSY > threshold
        
        Args:
            threshold (int): 신호 발생 임계값
            
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        npsy_col = 'NPSY(12)'
        signals = pd.Series(0, index=self.data.index)
        
        signals[self.data[npsy_col] < -threshold] = 1
        signals[self.data[npsy_col] > threshold] = -1
        
        return signals.shift(1)

    def generate_adl_signals(self, window_size: int = 20) -> pd.Series:
        """Accumulation Distribution Line (ADL) 신호 생성
        
        매수 신호: ADL이 상승 추세 (이전 값보다 증가)
        매도 신호: ADL이 하락 추세 (이전 값보다 감소)
        
        Args:
            window_size (int): 이동평균 기간
            
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        adl_col = f'ADL({window_size})'
        signals = pd.Series(0, index=self.data.index)
        
        signals[self.data[adl_col] > self.data[adl_col].shift(1)] = 1
        signals[self.data[adl_col] < self.data[adl_col].shift(1)] = -1
        
        return signals.shift(1)

    def generate_adr_signals(self, window_size: int = 20, threshold: float = 1.5) -> pd.Series:
        """Average Daily Range (ADR) 신호 생성
        
        매수 신호: 당일 범위가 ADR의 threshold배 이상
        매도 신호: 당일 범위가 ADR의 1/threshold배 이하
        
        Args:
            window_size (int): ADR 계산 기간
            threshold (float): 신호 발생 임계값
            
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        adr_col = f'ADR({window_size})'
        signals = pd.Series(0, index=self.data.index)
        
        daily_range = self.data['High'] - self.data['Low']
        
        signals[daily_range > (self.data[adr_col] * threshold)] = 1
        signals[daily_range < (self.data[adr_col] / threshold)] = -1
        
        return signals.shift(1)

    def generate_keltner_signals(self) -> pd.Series:
        """Keltner Channel 신호 생성
        
        매수 신호: 종가가 하단 밴드 하향 돌파
        매도 신호: 종가가 상단 밴드 상향 돌파
        
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        signals = pd.Series(0, index=self.data.index)
        
        signals[self.data['Close'] < self.data['Keltner(20)_lower']] = 1
        signals[self.data['Close'] > self.data['Keltner(20)_upper']] = -1
        
        return signals.shift(1)

    def generate_ichimoku_signals(self) -> pd.Series:
        """Ichimoku Cloud 신호 생성
        
        매수 신호: 
        1. 전환선이 기준선을 상향 돌파
        2. 가격이 구름대 위에 위치
        
        매도 신호:
        1. 전환선이 기준선을 하향 돌파
        2. 가격이 구름대 아래에 위치
        
        Returns:
            pd.Series: 1 (매수), -1 (매도), 0 (중립)
        """
        signals = pd.Series(0, index=self.data.index)
        
        # 매수 조건
        buy_condition = (
            (self.data['Tenkan(9)'] > self.data['Kijun(26)'])
        )
        signals[buy_condition] = 1
        
        # 매도 조건
        sell_condition = (
            (self.data['Tenkan(9)'] < self.data['Kijun(26)'])
        )
        signals[sell_condition] = -1
        
        return signals.shift(1)

    def generate_momentum_signals(self) -> pd.DataFrame:
        """모멘텀 지표 기반 신호 생성"""
        signals = pd.DataFrame(index=self.data.index)
        
        # 각 모멘텀 지표별 신호 생성
        signals['SMA'] = self.generate_sma_signals()
        signals['EMA'] = self.generate_ema_signals()
        signals['TSI'] = self.generate_tsi_signals()
        signals['MACD'] = self.generate_macd_signals()
        signals['PSAR'] = self.generate_psar_signals()
        signals['ADX'] = self.generate_adx_signals()
        signals['Aroon'] = self.generate_aroon_signals()
        signals['ADL'] = self.generate_adl_signals()
        signals['ADR'] = self.generate_adr_signals()
        signals['Ichimoku'] = self.generate_ichimoku_signals()
        signals['Keltner'] = self.generate_keltner_signals()
        
        return signals
    
    def generate_contrarian_signals(self) -> pd.DataFrame:
        """반추세 지표 기반 신호 생성"""
        signals = pd.DataFrame(index=self.data.index)
        
        # 각 반추세 지표별 신호 생성
        signals['RSI'] = self.generate_rsi_signals()
        signals['BB'] = self.generate_bb_signals()
        signals['CCI'] = self.generate_cci_signals()
        signals['Stoch'] = self.generate_stochastic_signals()
        signals['Williams'] = self.generate_williams_r_signals()
        signals['CMO'] = self.generate_cmo_signals()
        signals['DeMarker'] = self.generate_demark_signals()
        signals['Donchian'] = self.generate_donchian_signals()
        signals['Pivot'] = self.generate_pivot_signals()
        signals['PSY'] = self.generate_psy_signals()
        # signals['NPSY'] = self.generate_npsy_signals()
        
        return signals
    
    def calculate_signal_performance(self, signals: pd.DataFrame, 
                                  forward_periods: List[int] = [1, 5, 10, 20]) -> Dict[str, pd.DataFrame]:
        """신호별 성과 계산
        
        Args:
            signals (pd.DataFrame): 신호 데이터프레임
            forward_periods (List[int]): 성과 측정 기간 리스트
            
        Returns:
            Dict[str, pd.DataFrame]: 신호별 성과 지표
        """
        performance = {}
        
        for col in signals.columns:
            perf_df = pd.DataFrame(index=signals.index)
            
            for period in forward_periods:
                # 수익률 계산
                returns = (self.data['Close'].shift(-period) - self.data['Close']) / self.data['Close']
                
                # 매수 신호 성과
                buy_mask = signals[col] == 1
                perf_df[f'{period}D_Buy_Return'] = np.where(buy_mask, returns, np.nan)
                perf_df[f'{period}D_Buy_Win_Rate'] = np.where(
                    buy_mask, 
                    np.where(returns > 0, 1, 0), 
                    np.nan
                )
                
                # 매도 신호 성과
                sell_mask = signals[col] == -1
                perf_df[f'{period}D_Sell_Return'] = np.where(sell_mask, -returns, np.nan)
                perf_df[f'{period}D_Sell_Win_Rate'] = np.where(
                    sell_mask,
                    np.where(returns < 0, 1, 0),
                    np.nan
                )
            
            performance[col] = perf_df
            
        return performance
    
    def get_signal_summary(self, performance: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """신호별 성과 요약
        
        Args:
            performance (Dict[str, pd.DataFrame]): 신호별 성과 데이터
            
        Returns:
            pd.DataFrame: 성과 요약 데이터프레임
        """
        summary = []
        
        for signal_name, perf_df in performance.items():
            signal_summary = {}
            signal_summary['Signal'] = signal_name
            
            # 매수/매도 신호 성과 계산
            for direction in ['Buy', 'Sell']:
                for period in [1, 5, 10, 20]:
                    returns = perf_df[f'{period}D_{direction}_Return'].mean()
                    win_rate = perf_df[f'{period}D_{direction}_Win_Rate'].mean()
                    
                    signal_summary[f'{period}D_{direction}_Avg_Return'] = returns
                    signal_summary[f'{period}D_{direction}_Win_Rate'] = win_rate
            
            summary.append(signal_summary)
            
        return pd.DataFrame(summary)