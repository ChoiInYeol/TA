import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe


def calculate_returns(price_data: pd.DataFrame) -> pd.DataFrame:
    returns = price_data['Close'].pct_change()
    return pd.DataFrame({'Date': price_data.index, 'Return': returns})


def create_neuromorphic_style():
    plt.style.use('seaborn-v0_8-darkgrid')
    background_color = '#E0E5EC'
    text_color = '#2D4263'
    plt.rcParams.update({
        'figure.facecolor': background_color,
        'axes.facecolor': background_color,
        'axes.edgecolor': text_color,
        'axes.labelcolor': text_color,
        'text.color': text_color,
        'xtick.color': text_color,
        'ytick.color': text_color,
        'grid.color': '#CCD1D9',
        'font.family': 'Arial'
    })
    return background_color, text_color


def signal_heatmap_with_price(
    signal_file: str,
    price_file: str,
    start_date: str = None,
    end_date: str = None,
    last_n_trading_days: int = None,
    figsize: tuple = (15, 10),
    annot_size: int = 8,
    cbar: bool = False,
    square: bool = True,
    fontname: str = "Arial",
    ylabel: bool = True,
    savefig: str = None,
    show: bool = True
) -> None:
    bg_color, text_color = create_neuromorphic_style()
    
    # 데이터 로드
    signals_df = pd.read_csv(signal_file)
    price_df = pd.read_csv(price_file, index_col='Date', parse_dates=True)
    
    signals_df['Date'] = pd.to_datetime(signals_df.iloc[:, 0])
    signals_df.set_index('Date', inplace=True)
    
    # 원본 데이터 백업
    original_price_df = price_df.copy()
    original_signals_df = signals_df.copy()
    
    # 1. 주가 데이터 필터링 - 전체 데이터에서 한 번에 필요한 범위만 필터링
    if last_n_trading_days:
        # 거래일 기준으로 마지막 n일 선택
        end_date = original_price_df.index.max()
        trading_days = original_price_df.index.tolist()
        if len(trading_days) >= last_n_trading_days:
            start_date = trading_days[-last_n_trading_days]
    
    # 시작일과 종료일 기준으로 필터링
    if start_date:
        start_date = pd.to_datetime(start_date) if isinstance(start_date, str) else start_date
        price_df = original_price_df[original_price_df.index >= start_date]
    
    if end_date:
        end_date = pd.to_datetime(end_date) if isinstance(end_date, str) else end_date
        price_df = price_df[price_df.index <= end_date]
    
    # 2. 시그널 데이터 필터링 - 주가 데이터의 거래일에 맞게 필터링
    signals_df = original_signals_df[original_signals_df.index.isin(price_df.index)]
    
    # 3. 시그널 날짜 기준으로 주가 데이터 범위 확장 (직전 거래일 포함)
    signal_dates = signals_df.index
    
    if len(signal_dates) > 0:
        first_signal_date = signal_dates[0]
        
        # 첫 번째 시그널 날짜 이전의 가장 최근 거래일 찾기
        prev_trading_days = original_price_df.index[original_price_df.index < first_signal_date]
        
        if len(prev_trading_days) > 0:
            # 직전 거래일 찾기
            prev_trading_day = prev_trading_days[-1]
            
            # 최종 필터링 범위 설정 (직전 거래일부터 마지막 시그널 날짜까지)
            final_start_date = prev_trading_day
            final_end_date = signal_dates[-1]
            
            # 원본 데이터에서 최종 범위로 필터링
            price_df = original_price_df[(original_price_df.index >= final_start_date) & 
                                        (original_price_df.index <= final_end_date)]
        else:
            # 이전 거래일이 없는 경우 첫 번째 시그널 날짜부터 마지막 시그널 날짜까지
            price_df = original_price_df[(original_price_df.index >= first_signal_date) & 
                                        (original_price_df.index <= signal_dates[-1])]
    
    # Prepare data for visualization: 시그널과 주가 데이터의 날짜를 동일하게 맞춤
    common_dates = price_df.index
    signals_df = signals_df.reindex(common_dates, fill_value=np.nan)
    signals = signals_df.T  # Transpose so columns become dates
    
    # 날짜 레이블 형식 변경: 첫 날짜만 YYYY-MM-DD, 나머지는 DD
    date_labels = []
    for i, d in enumerate(common_dates):
        if i == 0:
            date_labels.append(d.strftime('%Y-%m-%d'))
        else:
            date_labels.append(d.strftime('%d'))
    
    n_dates = len(date_labels)
    
    # Figure & GridSpec: Two subplots with aligned x-axis
    fig = plt.figure(figsize=figsize)
    
    # 그리드스펙 생성 시 세로 간격 넓히기 (hspace 값 증가)
    gs = GridSpec(2, 1, height_ratios=[3, 1], figure=fig, hspace=0.2)
    
    ax_heatmap = fig.add_subplot(gs[0])
    
    colors = ['#ff4d4d', '#e6e6e6', '#4dff4d']
    
    def signal_to_text(val):
        if pd.isna(val):
            return ''
        elif val == -1:
            return 'Sell'
        elif val == 0:
            return ''
        elif val == 1:
            return 'Buy'
    
    # heatmap 생성 - square=True로 설정하여 정사각형 셀로 그리기
    sns.heatmap(signals, ax=ax_heatmap,
                annot=np.vectorize(signal_to_text)(signals),
                fmt='',
                center=0,
                annot_kws={'size': annot_size, 'color': text_color},
                linewidths=0.5,
                square=square,  # 정사각형 셀로 설정
                cbar=cbar,
                cmap=sns.color_palette(colors),
                xticklabels=date_labels)
    
    # 모든 날짜 표시
    ax_heatmap.set_xticks(np.arange(len(date_labels)))
    ax_heatmap.set_xticklabels(date_labels, rotation=90, ha='center')
    # x축 레이블 숨기기 (price plot과 중복 방지)
    ax_heatmap.set_xlabel('')
    ax_heatmap.tick_params(axis='x', labelsize=9)
    
    if ylabel:
        ax_heatmap.set_ylabel('Signals', fontname=fontname, fontweight='bold', fontsize=12)
    
    # 가로 넓이를 정확히 맞추기 위해 position 조정
    pos_heatmap = ax_heatmap.get_position()
    
    ax_price = fig.add_subplot(gs[1])
    
    # 주가 데이터 플롯
    all_trading_dates = price_df.index.tolist()
    
    # 모든 날짜에 대한 주가 데이터 준비
    aligned_price_data = price_df['Close'].values
    
    # 날짜 위치에 맞게 x 값 설정
    x_values = np.arange(len(all_trading_dates))
    
    # 최초 가격 데이터가 표시되도록 ylim 설정
    if len(aligned_price_data) > 0:
        min_price = min(aligned_price_data) * 0.995  # 최소값보다 약간 작게 설정
        max_price = max(aligned_price_data) * 1.005  # 최대값보다 약간 크게 설정
        
        # 주가 그래프에 선과 점 모두 표시
        ax_price.plot(x_values, aligned_price_data, color='#2D4263', linewidth=2, label='Price')
        ax_price.scatter(x_values, aligned_price_data, color='#2D4263', s=30, zorder=5)  # 각 지점에 점 추가
        
        ax_price.set_ylim(min_price, max_price)  # y축 범위 설정
        
        # 시그널 날짜에 해당하는 인덱스 찾기
        signal_indices = []
        for date in signal_dates:
            if date in price_df.index:
                signal_indices.append(price_df.index.get_loc(date))
        
        if signal_indices:
            # 마지막 시그널 날짜 강조
            last_signal_idx = signal_indices[-1]
            ax_price.axvline(x=last_signal_idx, color='red', linestyle='--', linewidth=1, label='Today Signal')
    
    # 날짜 레이블 형식 변경: 첫 날짜만 YYYY-MM-DD, 나머지는 DD
    all_date_labels = []
    for i, d in enumerate(all_trading_dates):
        if i == 0:
            all_date_labels.append(d.strftime('%Y-%m-%d'))
        else:
            all_date_labels.append(d.strftime('%d'))
    
    ax_price.set_xticks(np.arange(len(all_date_labels)))
    ax_price.set_xticklabels(all_date_labels, rotation=90, ha='center')
    ax_price.set_xlabel('Date', fontname=fontname, fontweight='bold', fontsize=12)
    ax_price.set_ylabel('Price', fontname=fontname, fontweight='bold', fontsize=12)
    ax_price.tick_params(axis='both', labelsize=9)
    ax_price.grid(True, alpha=0.3)
    
    # 가로 넓이를 정확히 맞추기 위해 position 조정
    pos_price = ax_price.get_position()
    ax_price.set_position([pos_heatmap.x0, pos_price.y0, pos_heatmap.width, pos_price.height])
    
    # 두 plot 간 정확한 가로 정렬을 위해 x축 범위 동일하게 설정
    ax_heatmap.set_xlim(-0.5, len(date_labels) - 0.5)
    ax_price.set_xlim(-0.5, len(all_trading_dates) - 0.5)
    
    # heatmap의 각 셀과 주가 플롯의 각 위치가 정확히 매핑되도록 조정
    if len(date_labels) > 0 and len(all_trading_dates) > 0:
        ax_heatmap.set_aspect('equal')  # 히트맵 셀 비율 유지
        ax_price.set_aspect('auto')  # 주가 플롯 비율 자동 조정

    if len(all_trading_dates) > 0:
        title = (f'Trading Signals Analysis Dashboard\n'
                f'{all_trading_dates[0].strftime("%Y-%m-%d")} ~ '
                f'{all_trading_dates[-1].strftime("%Y-%m-%d")}')
        fig.suptitle(title, fontsize=16, fontweight='bold', color=text_color, y=0.98)
    
    for ax in [ax_heatmap, ax_price]:
        ax.patch.set_facecolor(bg_color)
        shadow_rect = FancyBboxPatch(
            (0, 0), 1, 1, transform=ax.transAxes, zorder=-1,
            boxstyle="round,pad=0.05", facecolor=bg_color,
            path_effects=[pe.withSimplePatchShadow(offset=(4, -4),
                                                  shadow_rgbFace='#c8ccd1',
                                                  alpha=0.5)]
        )
        ax.add_patch(shadow_rect)

    if savefig:
        if isinstance(savefig, dict):
            plt.savefig(**savefig, bbox_inches='tight', dpi=300)
        else:
            plt.savefig(savefig, bbox_inches='tight', dpi=300)
    
    if show:
        plt.show()
        plt.close()
        return None
    return fig


if __name__ == "__main__":
    signal_heatmap_with_price(
        signal_file="data/processed/trading_signals.csv",
        price_file="data/raw/spy_data.csv",
        last_n_trading_days=30,
        annot_size=8,
        square=True,
        fontname="Arial",
        ylabel=True,
        savefig="data/processed/trading_signals_heatmap.png",
    )