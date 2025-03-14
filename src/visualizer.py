import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from mplfinance.original_flavor import candlestick_ohlc

def aligned_signal_candlestick(signal_file, price_file, last_n_trading_days=30, savefig=None, show=True):
    # 데이터 로드 및 병합
    signals_df = pd.read_csv(signal_file)
    price_df = pd.read_csv(price_file)
    
    signals_df['Date'] = pd.to_datetime(signals_df.iloc[:, 0])
    price_df['Date'] = pd.to_datetime(price_df['Date'])
    
    # 시그널을 하루 뒤로 이동 (N+1일의 의사결정)
    signals_df.set_index('Date', inplace=True)
    # 마지막 날짜에 다음 거래일 추가하고 NaN으로 채우기
    next_business_day = signals_df.index[-1] + pd.offsets.BDay(1)
    signals_df.loc[next_business_day] = np.nan
    signals_df = signals_df.shift(1)  # 시그널을 하루 앞으로 이동
    
    # 데이터프레임 병합
    merged_df = pd.merge(price_df, signals_df,
                        left_on='Date', right_index=True, how='outer')
    merged_df.set_index('Date', inplace=True)
    merged_df.sort_index(inplace=True)
    
    if len(merged_df) >= last_n_trading_days:
        merged_df = merged_df.iloc[-last_n_trading_days:]
    
    # 정수 인덱스로 변환
    dates = merged_df.index
    n_dates = len(dates)
    
    # OHLC 데이터 준비
    ohlc = []
    for i, (date, row) in enumerate(merged_df.iterrows()):
        ohlc.append((i, row['Open'], row['High'], row['Low'], row['Close']))
    
    # price 관련 칼럼 제외하고 원래 순서 유지
    signal_order = ['SMA', 'EMA', 'TSI', 'MACD', 'PSAR', 'ADX', 'Aroon', 'ADL', 'ADR', 
                   'Ichimoku', 'Keltner', 'RSI', 'BB', 'CCI', 'Stoch', 'Williams', 'CMO', 
                   'DeMarker', 'Donchian', 'Pivot', 'PSY', 'NPSY']
    signal_order = signal_order[::-1]  # 순서 반전
    signals = merged_df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], axis=1).copy()
    signals = signals.reindex(columns=signal_order)
    
    # 시그널 매핑 (-1 -> 0, 0 -> 1, 1 -> 2)
    heat_data = signals.replace({-1: 0, 0: 1, 1: 2}).to_numpy().T  # 매핑 순서 수정
    n_signals = heat_data.shape[0]
    
    # 그래프 생성
    fig = plt.figure(figsize=(15, 10))
    gs = plt.GridSpec(3, 1, height_ratios=[n_signals/2, 6, 2], hspace=0.10)
    
    # 1. 히트맵
    ax_heat = fig.add_subplot(gs[0])
    
    # 히트맵 플롯
    cmap = ListedColormap(['#ff4d4d', '#e6e6e6', '#4dff4d'])
    im = ax_heat.imshow(
        heat_data,
        aspect='auto',  # 주가 차트와 맞추기 위해 auto로 설정
        extent=[-0.5, n_dates - 0.5, -0.5, n_signals - 0.5],
        cmap=cmap,
        origin='lower'  # 시그널 순서를 아래에서 위로 표시
    )
    
    # 히트맵 설정
    ax_heat.set_yticks(range(n_signals))
    ax_heat.set_yticklabels(signal_order, fontsize=8)
    ax_heat.set_xticks([])
    ax_heat.set_ylabel('Signals', fontsize=10)
    
    # 히트맵 그리드 (흰색 구분선)
    ax_heat.grid(False)  # 기본 그리드 제거
    ax_heat.set_xticks(np.arange(-0.5, n_dates, 1), minor=True)
    ax_heat.set_yticks(np.arange(-0.5, n_signals, 1), minor=True)
    ax_heat.grid(True, which='minor', color='white', linewidth=1)
    
    # 히트맵 셀 텍스트
    for i in range(n_signals):
        for j in range(n_dates):
            val = signals[signal_order[i]].iloc[j]  # 올바른 순서로 접근
            if pd.notna(val):
                # 매핑된 값에 따라 텍스트 표시
                if val == 1:
                    txt = 'Buy'
                elif val == -1:
                    txt = 'Sell'
                else:
                    txt = ''
                ax_heat.text(j, i, txt, ha='center', va='center', fontsize=8)
    
    # 2. 캔들차트
    ax_candle = fig.add_subplot(gs[1])
    
    # 캔들차트 플롯
    candlestick_ohlc(ax_candle, ohlc, width=0.6, 
                     colorup='#4dff4d', colordown='#ff4d4d',
                     alpha=0.8)
    
    # 캔들차트 설정
    ax_candle.set_xlim(-0.5, n_dates - 0.5)
    ax_candle.grid(True, alpha=0.3)
    ax_candle.set_ylabel('Price', fontsize=10)
    ax_candle.set_xticklabels([])
    
    # 캔들차트 마지막 날짜 음영 처리
    rect_candle = plt.Rectangle((n_dates-1.5, ax_candle.get_ylim()[0]), 1, 
                              ax_candle.get_ylim()[1] - ax_candle.get_ylim()[0],
                              facecolor='yellow', alpha=0.3)
    ax_candle.add_patch(rect_candle)
    
    # 3. 볼륨차트
    ax_volume = fig.add_subplot(gs[2])
    volume_data = merged_df['Volume']
    
    # 상승/하락 거래량 색상 구분
    colors = np.where(merged_df['Close'] >= merged_df['Open'], '#4dff4d', '#ff4d4d')
    ax_volume.bar(range(len(volume_data)), volume_data, color=colors, alpha=0.7, width=0.8)
    
    # 볼륨차트 설정
    ax_volume.set_xlim(-0.5, n_dates - 0.5)
    ax_volume.grid(True, alpha=0.3)
    ax_volume.set_ylabel('Volume', fontsize=10)
    
    # 볼륨 차트의 y축 범위 설정
    min_volume = volume_data.min()
    max_volume = volume_data.max()
    volume_margin = (max_volume - min_volume) * 0.1  # 10% 여유 공간
    ax_volume.set_ylim(min_volume - volume_margin, max_volume + volume_margin)
    
    # 볼륨차트 마지막 날짜 음영 처리
    rect_volume = plt.Rectangle((n_dates-1.5, ax_volume.get_ylim()[0]), 1,
                              ax_volume.get_ylim()[1] - ax_volume.get_ylim()[0],
                              facecolor='yellow', alpha=0.3)
    ax_volume.add_patch(rect_volume)
    
    # x축 레이블 설정
    ax_volume.set_xticks(range(n_dates))
    date_labels = [date.strftime('%Y-%m-%d') if i == 0 else date.strftime('%d')
                  for i, date in enumerate(dates)]
    ax_volume.set_xticklabels(date_labels, rotation=45, ha='right')
    
    # 타이틀 설정
    if len(dates) > 0:
        title = (f'Trading Signals Analysis Dashboard\n'
                f'{dates[0].strftime("%Y-%m-%d")} ~ {dates[-1].strftime("%Y-%m-%d")}')
        fig.suptitle(title, fontsize=12, y=0.95)
    
    if savefig:
        plt.savefig(savefig, bbox_inches='tight', dpi=300)
    if show:
        plt.show()
        plt.close(fig)
    return fig

if __name__ == '__main__':
    aligned_signal_candlestick(
        'data/processed/trading_signals.csv',
        'data/raw/spy_data.csv',
        last_n_trading_days=20
    )
