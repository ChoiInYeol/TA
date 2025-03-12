import numpy as np
import pandas as pd

__docformat__ = 'restructuredtext en'
__author__ = "<Tommy Lee>, <Joon Kim>"
__all__ = ['CORE16MomentumIndicator','CORE16ContrarianIndicator']

class CORE16MomentumIndicator(object):
    def __init__(
            self, ohlcv_data: pd.DataFrame,
            resample: str = 'W-FRI'
    ) -> None:
        self.ohlcv_data = ohlcv_data
        self.resample = resample

    def _resample_ohlcv_data(self):
        if self.resample != '1d':
            open_data = self.ohlcv_data['Open'].resample(self.resample).first()
            high_data = self.ohlcv_data['High'].resample(self.resample).max()
            low_data = self.ohlcv_data['Low'].resample(self.resample).min()
            close_data = self.ohlcv_data['Close'].resample(self.resample).last()
            if 'Adj Close' in self.ohlcv_data.columns:
                adjusted_close_data = self.ohlcv_data['Adj Close'].resample(self.resample).last()
            volume_data = self.ohlcv_data['Volume'].resample(self.resample).sum()

            # Combine the resampled volume data with the rest of the OHLCV data
            if 'Adj Close' in self.ohlcv_data.columns:
                data = pd.concat([open_data, high_data, low_data, close_data, adjusted_close_data, volume_data], axis=1)
                data.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
            else:
                data = pd.concat([open_data, high_data, low_data, close_data, volume_data], axis=1)
                data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

            data.ffill(inplace=True)
            return data
        else :
            return self.ohlcv_data

    def simple_moving_average(
            self, window_size: int = 20,
            column_name: str = 'Close'
    ) -> pd.Series:
        data = self._resample_ohlcv_data()
        res = data[column_name].rolling(window_size).mean()
        res.name = f'SMA({window_size})'
        return res

    def exponential_moving_average(
            self, window_size: int = 20,
            column_name: str = 'Close'
    ) -> pd.Series:
        data = self._resample_ohlcv_data()
        res = data[column_name].ewm(window_size).mean()
        res.name = f'EMA({window_size})'
        return res

    def true_strength_index(
            self, short_window_size: int = 2,
            long_window_size: int = 20,
            column_name: str = 'Close',
    ) -> pd.Series:
        data = self._resample_ohlcv_data()
        momentum = data[column_name].diff(1)
        abs_momentum = abs(momentum)

        double_smoothed_momentum = momentum.ewm(long_window_size).mean().ewm(short_window_size).mean()
        double_smoothed_abs_momentum = abs_momentum.ewm(long_window_size).mean().ewm(short_window_size).mean()

        res = 100 * (double_smoothed_momentum / double_smoothed_abs_momentum)
        res.name = f'TSI({short_window_size},{long_window_size})'

        return res

    def moving_average_convergence_divergence(
            self, short_window_size: int = 12,
            long_window_size: int = 26,
            signal_window_size: int = 9,
            column_name: str = 'Close'
    ) -> pd.DataFrame:
        res = pd.DataFrame()
        data = self._resample_ohlcv_data()

        res[f'EMA({short_window_size})'] = data[column_name].ewm(
            span=short_window_size, adjust=False
        ).mean()  # Calculate short-term EMA
        res[f'EMA({long_window_size})'] = data[column_name].ewm(
            span=long_window_size, adjust=False
        ).mean()  # Calculate long-term EMA

        res[f'MACD({short_window_size},{long_window_size})'] = res[f'EMA({short_window_size})'] - res[
            f'EMA({long_window_size})']  # Calculate MACD Line (difference between short and long EMA)
        res[f'MACD Signal({signal_window_size})'] = res[f'MACD({short_window_size},{long_window_size})'].ewm(
            span=signal_window_size, adjust=False).mean()  # Calculate Signal Line (EMA of MACD)
        return res

    def parabolic_stop_and_reverse(
            self,
            acceleration_factor_step: float = 0.02,
            acceleration_factor_max: float = 0.2
    ) -> pd.Series:

        data = self._resample_ohlcv_data()

        # 초기화 시 인덱스를 데이터와 동일하게 설정
        psar = pd.Series(index=data.index, dtype=float)
        psar_direction = pd.Series(index=data.index, dtype=str)
        psar_af = acceleration_factor_step

        # 초기값 설정
        psar.iloc[0] = data['Close'].iloc[0]
        psar_ep = data['High'].iloc[0] if data['Close'].iloc[1] > data['Close'].iloc[0] else data['Low'].iloc[0]
        uptrend = data['Close'].iloc[1] > data['Close'].iloc[0]

        for i in range(1, len(data)):
            previous_psar = psar.iloc[i - 1]
            if uptrend:
                psar.iloc[i] = previous_psar + psar_af * (psar_ep - previous_psar)
                if data['Low'].iloc[i] < psar.iloc[i]:
                    uptrend = False
                    psar.iloc[i] = psar_ep
                    psar_af = acceleration_factor_step
                    psar_ep = data['Low'].iloc[i]
            else:
                psar.iloc[i] = previous_psar - psar_af * (previous_psar - psar_ep)
                if data['High'].iloc[i] > psar.iloc[i]:
                    uptrend = True
                    psar.iloc[i] = psar_ep
                    psar_af = acceleration_factor_step
                    psar_ep = data['High'].iloc[i]

            if uptrend:
                if data['High'].iloc[i] > psar_ep:
                    psar_ep = data['High'].iloc[i]
                    psar_af = min(psar_af + acceleration_factor_step, acceleration_factor_max)
            else:
                if data['Low'].iloc[i] < psar_ep:
                    psar_ep = data['Low'].iloc[i]
                    psar_af = min(psar_af + acceleration_factor_step, acceleration_factor_max)

            psar_direction.iloc[i] = 'uptrend' if uptrend else 'downtrend'

        psar.name = f'PSAR({acceleration_factor_step})'
        return psar

    def accumulation_distribution_line(
            self,
            window_size: int = 20,
    ) -> pd.DataFrame:
        data = self._resample_ohlcv_data()

        mfm = ((data['Close'] - data['Low']) - (data['High'] - data['Close'])) / (data['High'] - data['Low'])
        mfv = mfm * data['Volume']
        adl = mfv.cumsum()

        res = adl.rolling(window_size).sum()
        res.name = f'ADL({window_size})'

        return res

    def average_daily_range(self, window_size: int = 20) -> pd.DataFrame:
        data = self._resample_ohlcv_data()
        daily_range = data['High'] - data['Low']

        adr = daily_range.rolling(window_size).mean()
        adr.name = f'ADR({window_size})'

        return adr

    def average_true_range(
            self,
            window_size: int = 20
    ) -> pd.Series:
        data = self._resample_ohlcv_data()

        data['High-Low'] = data['High'] - data['Low']  # a) Calculate [Current High price - Current Low Price]
        data['High-Close'] = np.abs(data['High'] - data[
            'Close'].shift())  # b) Calculate [High Price of Current Day - Adjusted Closing Price of Previous Day]
        data['Low-Close'] = np.abs(data['Low'] - data[
            'Close'].shift())  # c) Calculate [Low Price of Current Day - Adjusted Closing Price of Previous Day]
        data['True_Range'] = data[['High-Low', 'High-Close', 'Low-Close']].max(
            axis=1)  # Calculate True Range (TR) = max[a, b, c]

        atr = data['True_Range'].rolling(window_size).mean()  # Calculate ATR as the mean of the True Range
        atr.name = f'ATR({window_size})'
        return atr

    def average_directional_movement_index(
            self,
            window_size: int = 20
    ) -> pd.Series:
        data = self._resample_ohlcv_data()
        atr = self.average_true_range(window_size)

        dm_plus = np.where((data['High'] - data['High'].shift(1)) > (data['Low'].shift(1) - data['Low']),
                           np.maximum(data['High'] - data['High'].shift(1), 0), 0)
        dm_minus = np.where((data['Low'].shift(1) - data['Low']) > (data['High'] - data['High'].shift(1)),
                            np.maximum(data['Low'].shift(1) - data['Low'], 0), 0)

        dm_plus = pd.Series(dm_plus, index=data.index)
        dm_minus = pd.Series(dm_minus, index=data.index)

        di_plus = 100 * (dm_plus.rolling(window_size).mean() / atr)
        di_minus = 100 * (dm_minus.rolling(window_size).mean() / atr)

        dx = 100 * (np.abs(di_plus - di_minus) / (di_plus + di_minus))

        # Calculate the ADX as the moving average of DX
        adx = dx.rolling(window_size).mean()
        adx.name = f'ADX({window_size})'

        return adx

    def aroon_indicator(
            self, window_size: int = 20
    ) -> pd.DataFrame:
        data = self._resample_ohlcv_data()
        aroon_up = 100 * (window_size - data['High'].rolling(window=window_size).apply(lambda x: x[::-1].argmax())) / window_size
        # Calculate Aroon Down using the lowest low over the specified window
        aroon_down = 100 * (window_size - data['Low'].rolling(window=window_size).apply(lambda x: x[::-1].argmin())) / window_size
        # Calculate Aroon Oscillator as the difference between Aroon Up and Aroon Down
        aroon_oscillator = aroon_up - aroon_down

        res = pd.concat([aroon_up, aroon_down, aroon_oscillator], axis=1)
        res.columns = [f'Aroon({window_size}) up', f'Aroon({window_size}) down', f'Aroon({window_size}) Oscillator']

        return res

    def ichimoku_indicator(
            self,
            kijun_window: int = 26,
            senkouB_window: int = 52,
            tenkan_window: int = 9
    ) -> pd.DataFrame:

        data = self._resample_ohlcv_data()

        data[f'Tenkan({tenkan_window})'] = (data['High'].rolling(window=tenkan_window).max() + data['Low'].rolling(
            window=tenkan_window).min()) / 2  # Calculate Tenkan Sen (Conversion Line)
        data[f'Kijun({kijun_window})'] = (data['High'].rolling(window=kijun_window).max() + data['Low'].rolling(
            window=kijun_window).min()) / 2  # Calculate Kijun Sen (Base Line)
        data[f'Senkou({kijun_window})_A'] = (
                    (data[f'Tenkan({tenkan_window})'] + data[f'Kijun({kijun_window})']) / 2).shift(
            kijun_window)  # Calculate Senkou Span A (Leading Span A)

        # Calculate Senkou Span B (Leading Span B)
        data[f'Senkou({senkouB_window})_B'] = ((data['High'].rolling(window=senkouB_window).max() + data['Low'].rolling(
            window=senkouB_window).min()) / 2).shift(kijun_window)
        data[f'Chikou({kijun_window})'] = data['Close'].shift(-kijun_window)  # Calculate Chikou Span (Lagging Span)

        res = data[[f'Tenkan({tenkan_window})', f'Kijun({kijun_window})', f'Senkou({kijun_window})_A',
                    f'Senkou({senkouB_window})_B', f'Chikou({kijun_window})']].copy('deep')

        return res

    def keltner_channel(
            self, channel_window: int = 20,
            atr_window: int = 20,
            band_sigma: float = 2
    ) -> pd.DataFrame:
        data = self._resample_ohlcv_data()
        atr = self.average_true_range(atr_window)

        data[f'Keltner({channel_window})_mid'] = data['Close'].ewm(span=channel_window,
                                                                   adjust=False).mean()  # Calculate the middle band using the exponential moving average
        data[f'ATR({atr_window})'] = atr
        data[f'Keltner({channel_window})_upper'] = data[f'Keltner({channel_window})_mid'] + (
                    data[f'ATR({atr_window})'] * band_sigma)  # Calculate the upper band
        data[f'Keltner({channel_window})_lower'] = data[f'Keltner({channel_window})_mid'] - (
                    data[f'ATR({atr_window})'] * band_sigma)  # Calculate the lower band

        res = data[[f'Keltner({channel_window})_mid', f'Keltner({channel_window})_upper',
                    f'Keltner({channel_window})_lower']].copy('deep')
        return res
    
    def calculate_all_indicators(self) -> pd.DataFrame:
        """모든 기술적 지표 계산
        
        Returns:
            pd.DataFrame: 계산된 모든 기술적 지표
        """
        res = pd.DataFrame()
        
        # SMA (Series)
        sma = self.simple_moving_average()
        res[sma.name] = sma
        
        # EMA (Series)
        ema = self.exponential_moving_average()
        res[ema.name] = ema
        
        # TSI (Series)
        tsi = self.true_strength_index()
        res[tsi.name] = tsi
        
        # MACD (DataFrame)
        macd_df = self.moving_average_convergence_divergence()
        for col in macd_df.columns:
            res[col] = macd_df[col]
        
        # PSAR (Series)
        psar = self.parabolic_stop_and_reverse()
        res[psar.name] = psar
        
        # ADL (Series)
        adl = self.accumulation_distribution_line()
        res[adl.name] = adl
        
        # ADR (Series)
        adr = self.average_daily_range()
        res[adr.name] = adr
        
        # ATR (Series)
        atr = self.average_true_range()
        res[atr.name] = atr
        
        # ADX (Series)
        adx = self.average_directional_movement_index()
        res[adx.name] = adx
        
        aroon_df = self.aroon_indicator()
        for col in aroon_df.columns:
            res[col] = aroon_df[col]
        
        # Ichimoku (DataFrame)
        ichimoku_df = self.ichimoku_indicator()
        for col in ichimoku_df.columns:
            res[col] = ichimoku_df[col]
        
        # Keltner Channel (DataFrame)
        keltner_df = self.keltner_channel()
        for col in keltner_df.columns:
            res[col] = keltner_df[col]
            
        return res


class CORE16ContrarianIndicator(object):
    def __init__(
            self, ohlcv_data: pd.DataFrame,
            resample: str = 'W-FRI'
    ) -> None:
        self.ohlcv_data = ohlcv_data
        self.resample = resample

    def _resample_ohlcv_data(self):
        if self.resample != '1d':
            open_data = self.ohlcv_data['Open'].resample(self.resample).first()
            high_data = self.ohlcv_data['High'].resample(self.resample).max()
            low_data = self.ohlcv_data['Low'].resample(self.resample).min()
            close_data = self.ohlcv_data['Close'].resample(self.resample).last()
            if 'Adj Close' in self.ohlcv_data.columns:
                adjusted_close_data = self.ohlcv_data['Adj Close'].resample(self.resample).last()
            volume_data = self.ohlcv_data['Volume'].resample(self.resample).sum()

            # Combine the resampled volume data with the rest of the OHLCV data
            if 'Adj Close' in self.ohlcv_data.columns:
                data = pd.concat([open_data, high_data, low_data, close_data, adjusted_close_data, volume_data], axis=1)
                data.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
            else:
                data = pd.concat([open_data, high_data, low_data, close_data, volume_data], axis=1)
                data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

            data.ffill(inplace=True)

            return data
        else :
            return self.ohlcv_data

    def relative_strength_index(
            self, window_size: int = 14,
            column_name: str = 'Close',
            method: str = 'simple'
    ) -> pd.Series:
        data = self._resample_ohlcv_data()

        delta = data[column_name].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        if method == 'simple':
            avg_gain = gain.rolling(window_size).mean()
            avg_loss = loss.rolling(window_size).mean()
        elif method == 'exponential':
            avg_gain = gain.ewm(window_size).mean()
            avg_loss = loss.ewm(window_size).mean()
        else:
            raise NotImplementedError('Method must be either simple or exponential')

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        rsi.name = f'RSI({window_size})'

        return rsi

    def bollinger_band(
            self, window_size: int = 20,
            band_sigma: int = 2,
            column_name: str = 'Close',
            method: str = 'simple'
    ) -> pd.DataFrame:
        data = self._resample_ohlcv_data()

        if method == 'simple':
            mavg = data[column_name].rolling(window_size).mean()
            band_std = data[column_name].rolling(window_size).std()
        elif method == 'exponential':
            mavg = data[column_name].ewm(window_size).mean()
            band_std = data[column_name].ewm(window_size).std()
        else:
            raise NotImplementedError('Method must be either simple or exponential')

        up = mavg + (band_sigma * band_std)
        down = mavg - (band_sigma * band_std)

        res = pd.concat([mavg, up, down], axis=1)
        res.columns = [f'BB_MAVG({window_size})', f'BB_UP({window_size})', f'BB_DOWN({window_size})']

        return res

    def commodity_channel_index(self, window_size: int = 20, scale_const: float = 0.015) -> pd.Series:
        data = self._resample_ohlcv_data()

        tp = (data['High'] + data['Low'] + data['Close']) / 3
        short_sma = tp.rolling(window_size).mean()
        short_mad = tp.rolling(window_size).apply(
            lambda x: np.fabs(x - x.mean()).mean()
        )
        cci = (tp - short_sma) / (scale_const * short_mad)

        cci.name = f'CCI({window_size})'
        return cci

    def chande_momentum_oscillator(self, window_size: int = 14) -> pd.Series:
        data = self._resample_ohlcv_data()

        data['Change'] = data['Close'].diff()
        data['Gain'] = np.where(data['Change'] > 0, data['Change'], 0)
        data['Loss'] = np.where(data['Change'] < 0, -data['Change'], 0)

        data['Sum_Gain'] = data['Gain'].rolling(window_size).sum()
        data['Sum_Loss'] = data['Loss'].rolling(window_size).sum()

        cmo = 100 * (data['Sum_Gain'] - data['Sum_Loss']) / (data['Sum_Gain'] + data['Sum_Loss'])
        cmo.name = f'CMO({window_size})'

        return cmo

    def demarker_indicator(self, window_size: int = 14) -> pd.Series:
        data = self._resample_ohlcv_data()

        data['DeMax'] = np.where(data['High'] > data['High'].shift(1), data['High'] - data['High'].shift(1), 0)
        data['DeMin'] = np.where(data['Low'] < data['Low'].shift(1), data['Low'].shift(1) - data['Low'], 0)

        data['DeMax_SMA'] = data['DeMax'].rolling(window_size).mean()
        data['DeMin_SMA'] = data['DeMin'].rolling(window_size).mean()

        demark = data['DeMax_SMA'] / (data['DeMax_SMA'] + data['DeMin_SMA'])

        demark.name = f'DEMARK({window_size})'
        return demark

    def donchian_channel(self, window_size: int = 20) -> pd.DataFrame:
        data = self._resample_ohlcv_data()

        data['Upper_Band'] = data['High'].rolling(window_size).max()
        data['Lower_Band'] = data['Low'].rolling(window_size).min()
        data['Mid_Band'] = (data['Upper_Band'] + data['Lower_Band']) / 2

        res = data[['Mid_Band', 'Upper_Band', 'Lower_Band']].copy('deep')
        res.columns = [f'Donchian({window_size}) mid', f'Donchian({window_size}) up', f'Donchian({window_size}) down']

        return res

    def pivot(self, scale_const: float = 2.0) -> pd.DataFrame:
        data = self._resample_ohlcv_data()

        data['Pivot_Point'] = (data['High'].shift(1) + data['Low'].shift(1) + data['Close'].shift(1)) / 3
        data['Support_1'] = (scale_const * data['Pivot_Point']) - data['High'].shift(1)
        data['Resistance_1'] = (scale_const * data['Pivot_Point']) - data['Low'].shift(1)

        res = data[['Pivot_Point', 'Support_1', 'Resistance_1']]
        res.columns = ['Pivot', 'Support', 'Resistance']

        return res

    def stochastic_oscillator(self, k_window_size: int = 14, d_window_size: int = 3) -> pd.DataFrame:
        data = self._resample_ohlcv_data()

        low = data['Low'].rolling(k_window_size).min()
        high = data['High'].rolling(k_window_size).max()
        k_per = 100 * ((data['Close'] - low) / (high - low))
        d_per = k_per.rolling(d_window_size).mean()

        res = pd.concat([low, high, k_per, d_per], axis=1)
        res.columns = [f'stochastic_oscillator Low({k_window_size})', f'stochastic_oscillator High({k_window_size})', f'stochastic_oscillator %K({k_window_size})',
                       f'stochastic_oscillator %D({d_window_size})']

        return res

    def williams_oscillator(self, window_size: int = 14) -> pd.Series:
        data = self._resample_ohlcv_data()

        data['Highest_High'] = data['High'].rolling(window_size).max()
        data['Lowest_Low'] = data['Low'].rolling(window_size).min()

        res = (data['Highest_High'] - data['Close']) / (data['Highest_High'] - data['Lowest_Low']) * -100
        res.name = f'Williams({window_size})'
        return res

    def psycological_line(self, window_size: int = 12, column_name: str = 'Close') -> pd.Series:
        data = self._resample_ohlcv_data()

        data['Up'] = np.where(data[column_name] > data[column_name].shift(1), 1, 0)
        # Calculate the PSY as the percentage of 'Up' days over the specified window period
        psy = data['Up'].rolling(window_size).sum() / window_size * 100

        psy.name = f'PSY({window_size})'
        return psy

    def normalized_psycological_line(self, window_size: int = 12, column_name: str = 'Close') -> pd.Series:
        data = self._resample_ohlcv_data()
        data['Up'] = np.where(data[column_name] > data[column_name].shift(1), 1,
                              0)  # Calculate Up values: 1 if current close > previous close, else 0
        npsy = (data['Up'].rolling(window_size).sum() - (window_size / 2)) / (
                    window_size / 2) * 100  # Calculate NPSY as a percentage

        npsy.name = f'NPSY({window_size})'
        return npsy
    
    def calculate_all_indicators(self) -> pd.DataFrame:
        res = pd.DataFrame()
        
        # RSI (Series)
        rsi = self.relative_strength_index()
        res[rsi.name] = rsi
        
        # Bollinger Bands (DataFrame)
        bb_df = self.bollinger_band()
        for col in bb_df.columns:
            res[col] = bb_df[col]
        
        # CCI (Series)
        cci = self.commodity_channel_index()
        res[cci.name] = cci
        
        # CMO (Series)
        cmo = self.chande_momentum_oscillator()
        res[cmo.name] = cmo
        
        # DeMarker (Series)
        demark = self.demarker_indicator()
        res[demark.name] = demark
        
        # Donchian Channel (DataFrame)
        donchian_df = self.donchian_channel()
        for col in donchian_df.columns:
            res[col] = donchian_df[col]
        
        # Pivot Points (DataFrame)
        pivot_df = self.pivot()
        for col in pivot_df.columns:
            res[col] = pivot_df[col]
        
        # Stochastic Oscillator (DataFrame)
        stochastic_df = self.stochastic_oscillator()
        for col in stochastic_df.columns:
            res[col] = stochastic_df[col]
        
        # Williams %R (Series)
        williams = self.williams_oscillator()
        res[williams.name] = williams
        
        # PSY (Series)
        psy = self.psycological_line()
        res[psy.name] = psy
        
        # NPSY (Series)
        npsy = self.normalized_psycological_line()
        res[npsy.name] = npsy
        
        return res
