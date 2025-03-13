import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def signal_heatmap_with_price(
    signal_file,
    price_file,
    figsize=(20, 12),
    annot_size=8,
    cbar=True,
    square=True,
    fontname="Arial",
    ylabel=True,
    savefig=None,
    show=True
):
    """
    주가 데이터와 시그널을 함께 시각화하는 함수
    
    Parameters
    ----------
    signal_file : str
        시그널 데이터가 저장된 CSV 파일 경로
    price_file : str
        주가 데이터가 저장된 CSV 파일 경로
    figsize : tuple, optional
        그래프 크기, by default (20, 12)
    annot_size : int, optional
        주석 텍스트 크기, by default 8
    cbar : bool, optional
        컬러바 표시 여부, by default True
    square : bool, optional
        정사각형 셀 사용 여부, by default False
    fontname : str, optional
        폰트 이름, by default "Arial"
    ylabel : bool, optional
        y축 레이블 표시 여부, by default True
    savefig : str, optional
        저장할 파일 경로, by default None
    show : bool, optional
        그래프 표시 여부, by default True
    
    Returns
    -------
    None or Figure
        show가 False인 경우 Figure 객체 반환
    """
    # 데이터 로드
    signals_df = pd.read_csv(signal_file)
    price_df = pd.read_csv(price_file)
    
    # 날짜 컬럼을 datetime으로 변환
    signals_df['Date'] = pd.to_datetime(signals_df.iloc[:, 0])
    price_df['Date'] = pd.to_datetime(price_df['Date'])
    
    # 최근 1주만 표시
    last_date = signals_df['Date'].max()
    signals_df = signals_df[signals_df['Date'] >= (last_date - pd.DateOffset(weeks=1))]
    price_df = price_df[price_df['Date'] >= (last_date - pd.DateOffset(weeks=1))]
    
    # 수익률 계산
    price_df['Returns'] = price_df['Close'].pct_change() * 100
    
    # 데이터 병합
    merged_df = signals_df.merge(price_df[['Date', 'Returns']], on='Date', how='left')
    
    # 시각화할 데이터 준비
    signals = merged_df.iloc[:, 1:-1]  # 날짜와 수익률 열을 제외한 시그널
    returns = merged_df['Returns']
    
    # 시각화
    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 2], hspace=0.3)
    
    # 주가 그래프
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(price_df['Date'], price_df['Close'], color='black', linewidth=1.5)
    ax1.set_title('SPY Price', fontsize=14, fontname=fontname, fontweight='bold', pad=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticklabels([])
    
    # 시그널 히트맵
    ax2 = fig.add_subplot(gs[1])
    
    # 커스텀 컬러맵 생성 (빨간색: Sell, 회색: Neu, 초록색: Buy)
    colors = ['#ff4d4d', '#e6e6e6', '#4dff4d']
    
    # 시그널 값을 텍스트로 매핑하는 함수
    def signal_to_text(val):
        if val == -1:
            return 'Sell'
        elif val == 0:
            return 'Neu'
        else:
            return 'Buy'
    
    # 시그널 데이터 준비
    signals_array = signals.values
    signals_text = np.vectorize(signal_to_text)(signals_array)
    
    # 히트맵 그리기 (시그널)
    sns.heatmap(signals_array.T, ax=ax2,
                annot=signals_text.T,
                fmt='',
                center=0,
                annot_kws={'size': annot_size},
                linewidths=0.5,
                square=square,
                cbar=cbar,
                cmap=sns.color_palette(colors),
                cbar_kws={'ticks': [-0.67, 0, 0.67],
                         'label': 'Signal Direction'},
                yticklabels=signals.columns)
    
    # 수직선으로 시그널과 수익률 구분
    ax2.axvline(x=signals.shape[1], color='black', linewidth=2)
    
    # 수익률 히트맵 추가
    returns_cmap = sns.diverging_palette(10, 133, as_cmap=True)
    returns_array = returns.values.reshape(-1, 1)
    
    # 수익률 히트맵의 y축 위치 계산
    returns_yticks = np.arange(len(signals.columns), len(signals.columns) + 1)
    
    returns_heatmap = sns.heatmap(returns_array.T,
                                 ax=ax2,
                                 cmap=returns_cmap,
                                 center=0,
                                 annot=True,
                                 fmt='.2f',
                                 annot_kws={'size': annot_size},
                                 cbar=True,
                                 cbar_kws={'label': 'Returns (%)'},
                                 xticklabels=date_labels,
                                 yticklabels=['Returns'])
    
    # x축 레이블 회전
    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
    
    if ylabel:
        ax2.set_ylabel('Technical Indicators', fontname=fontname, fontweight='bold', fontsize=12)
    
    ax2.set_xlabel('Date', fontname=fontname, fontweight='bold', fontsize=12)
    
    # 컬러바 레이블 수정
    if cbar:
        cbar = ax2.collections[0].colorbar
        cbar.set_ticks([-0.67, 0, 0.67])
        cbar.set_ticklabels(['Sell', 'Neu', 'Buy'])
    
    try:
        plt.subplots_adjust(left=0.15, right=0.9, bottom=0.15)
    except Exception:
        pass
    
    if savefig:
        if isinstance(savefig, dict):
            plt.savefig(**savefig)
        else:
            plt.savefig(savefig)
    
    if show:
        plt.show()
        plt.close()
        return None
    
    return fig

if __name__ == "__main__":
    # 예제 사용
    signal_heatmap_with_price(
        "data/processed/trading_signals.csv",
        "data/raw/spy_data.csv"
    )
