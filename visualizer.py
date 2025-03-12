import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Dict

class TAVisualizer:
    """기술적 지표 시각화 클래스"""
    
    def __init__(self, data: pd.DataFrame, signals: pd.DataFrame):
        """
        Args:
            data (pd.DataFrame): 원본 데이터와 기술적 지표가 포함된 데이터프레임
            signals (pd.DataFrame): 신호 데이터프레임
        """
        # 거래일만 필터링
        self.data = data[data['Volume'] > 0].copy()
        self.signals = signals.loc[self.data.index].copy()
        self.fig = None
        
    def create_base_chart(self, height: int = 1000) -> None:
        """기본 차트 생성"""
        # 서브플롯 생성
        self.fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.4, 0.2, 0.2, 0.2]
        )
        
        # 캔들스틱 차트
        self.fig.add_trace(
            go.Candlestick(
                x=self.data.index,
                open=self.data['Open'],
                high=self.data['High'],
                low=self.data['Low'],
                close=self.data['Close'],
                name='OHLC'
            ),
            row=1, col=1
        )
        
        # 볼륨 차트
        colors = ['red' if close < open else 'green' 
                 for close, open in zip(self.data['Close'], self.data['Open'])]
        
        self.fig.add_trace(
            go.Bar(
                x=self.data.index,
                y=self.data['Volume'],
                name='Volume',
                marker_color=colors
            ),
            row=2, col=1
        )
        
        # 차트 레이아웃 설정
        self.fig.update_layout(
            template='plotly_dark',
            height=height,
            title='Technical Analysis Dashboard',
            xaxis_rangeslider_visible=False,
            # X축 날짜 포맷 설정
            xaxis=dict(
                type='category',
                tickformat='%Y-%m-%d',
                tickmode='auto',
                nticks=20
            )
        )
        
        # Y축 그리드 설정
        self.fig.update_yaxes(gridcolor='rgba(128, 128, 128, 0.2)', minor_gridcolor='rgba(128, 128, 128, 0.1)')
        
    def add_momentum_indicators(self) -> None:
        """모멘텀 지표 추가"""
        # MACD
        self.fig.add_trace(
            go.Scatter(
                x=self.data.index,
                y=self.data['MACD(12,26)'],
                name='MACD',
                line=dict(color='blue')
            ),
            row=3, col=1
        )
        
        self.fig.add_trace(
            go.Scatter(
                x=self.data.index,
                y=self.data['MACD Signal(9)'],
                name='Signal',
                line=dict(color='orange')
            ),
            row=3, col=1
        )
        
        # TSI
        self.fig.add_trace(
            go.Scatter(
                x=self.data.index,
                y=self.data['TSI(2,20)'],
                name='TSI',
                line=dict(color='purple')
            ),
            row=4, col=1
        )
        
    def add_contrarian_indicators(self) -> None:
        """반추세 지표 추가"""
        # 볼린저 밴드
        self.fig.add_trace(
            go.Scatter(
                x=self.data.index,
                y=self.data['BB_UP(20)'],
                name='BB Upper',
                line=dict(color='gray', dash='dash'),
                opacity=0.5
            ),
            row=1, col=1
        )
        
        self.fig.add_trace(
            go.Scatter(
                x=self.data.index,
                y=self.data['BB_DOWN(20)'],
                name='BB Lower',
                line=dict(color='gray', dash='dash'),
                opacity=0.5,
                fill='tonexty'  # 밴드 사이 영역 채우기
            ),
            row=1, col=1
        )
        
        # RSI
        self.fig.add_trace(
            go.Scatter(
                x=self.data.index,
                y=self.data['RSI(14)'],
                name='RSI',
                line=dict(color='yellow')
            ),
            row=4, col=1
        )
        
        # RSI 기준선
        self.fig.add_hline(y=70, line_dash="dash", line_color="red", row=4, col=1)
        self.fig.add_hline(y=30, line_dash="dash", line_color="green", row=4, col=1)
        
    def add_signals(self) -> None:
        """매매 신호 추가"""
        for col in self.signals.columns:
            # 매수 신호
            buy_signals = self.signals[self.signals[col] == 1].index
            if len(buy_signals) > 0:
                self.fig.add_trace(
                    go.Scatter(
                        x=buy_signals,
                        y=self.data.loc[buy_signals, 'Low'] * 0.99,
                        mode='markers',
                        marker=dict(
                            symbol='triangle-up',
                            size=10,
                            color='green'
                        ),
                        name=f'{col} Buy'
                    ),
                    row=1, col=1
                )
            
            # 매도 신호
            sell_signals = self.signals[self.signals[col] == -1].index
            if len(sell_signals) > 0:
                self.fig.add_trace(
                    go.Scatter(
                        x=sell_signals,
                        y=self.data.loc[sell_signals, 'High'] * 1.01,
                        mode='markers',
                        marker=dict(
                            symbol='triangle-down',
                            size=10,
                            color='red'
                        ),
                        name=f'{col} Sell'
                    ),
                    row=1, col=1
                )
            
    def show(self) -> None:
        """차트 표시"""
        self.fig.show()
        
    def save(self, filename: str) -> None:
        """차트 저장
        
        Args:
            filename (str): 저장할 파일명
        """
        self.fig.write_html(filename) 