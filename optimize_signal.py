import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
from itertools import combinations
from multiprocessing import Pool, cpu_count
from functools import partial

class SignalOptimizer:
    """시그널 최적화 클래스"""
    
    def __init__(self, signals_df: pd.DataFrame, price_data: pd.DataFrame):
        """
        Args:
            signals_df (pd.DataFrame): 시그널 데이터
            price_data (pd.DataFrame): 가격 데이터 (Close 가격 포함)
        """
        self.signals = signals_df
        self.prices = price_data
        
    def calculate_correlation_heatmap(self, save_path: str = 'signal_correlation.png') -> None:
        """시그널 간 상관관계 히트맵 생성 및 저장
        
        Args:
            save_path (str): 히트맵 저장 경로
        """
        # 한글 폰트 설정
        plt.rc('font', family='Malgun Gothic')
        
        # 상관관계 계산
        corr_matrix = self.signals.corr()
        
        # 히트맵 생성
        plt.figure(figsize=(15, 12))
        sns.heatmap(corr_matrix, 
                   annot=True,  # 상관계수 표시
                   cmap='RdYlBu',  # 색상맵
                   center=0,  # 중앙값 (0) 기준
                   fmt='.2f',  # 소수점 2자리
                   square=True)  # 정사각형 형태
        
        plt.title('시그널 간 상관관계 히트맵')
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        
    def calculate_signal_performance(self, 
                                   signal_combination: List[str], 
                                   lookback_period: int = 20,
                                   threshold: float = -0.05) -> Dict[str, float]:
        """시그널 조합의 성과 계산
        
        Args:
            signal_combination (List[str]): 분석할 시그널 컬럼명 리스트
            lookback_period (int): 수익률 계산 기간 (예: 20일)
            threshold (float): 하락 판단 기준 수익률 (예: -0.05는 5% 하락)
            
        Returns:
            Dict[str, float]: 성과 지표 딕셔너리
        """
        # 시그널 조합 (동일 가중치)
        # 선택된 시그널들의 평균값을 계산하여 통합 시그널 생성
        combined_signal = self.signals[signal_combination].mean(axis=1)
        # 음수 시그널을 -1로 변환하여 매도 시그널 생성
        sell_signal = (combined_signal < 0).astype(int) * -1
        
        # 미래 수익률 계산
        # lookback_period 기간 동안의 수익률을 계산하고 미래 시점으로 이동
        future_returns = self.prices['Close'].pct_change(lookback_period).shift(-lookback_period)
        
        # 매도 시그널 성과
        # 매도 시그널이 발생한 시점의 수익률만 추출
        sell_mask = sell_signal == -1
        sell_returns = future_returns[sell_mask]
        
        # 하락 예측 정확도 계산
        # threshold 이하로 하락한 경우를 실제 하락으로 판단
        actual_decline = future_returns < threshold
        # 매도 시그널이 실제 하락을 맞춘 경우 (진음성)
        true_negatives = ((sell_signal == -1) & actual_decline).sum()
        # 매도 시그널이 실제 하락을 틀린 경우 (위음성)
        false_negatives = ((sell_signal == -1) & ~actual_decline).sum()
        
        # 정확도 = 진음성 / (진음성 + 위음성)
        if (true_negatives + false_negatives) == 0:
            accuracy = 0
        else:
            accuracy = true_negatives / (true_negatives + false_negatives)
            
        # 상세 성과 지표 계산
        # 최대 손실: 매도 시그널 발생 시점의 최대 하락폭
        max_drawdown = sell_returns.min() if len(sell_returns) > 0 else 0
        # 변동성: 매도 시그널 발생 시점 수익률의 표준편차
        volatility = sell_returns.std() if len(sell_returns) > 0 else 0
        
        return {
            'Accuracy': accuracy,  # 하락 예측 정확도 (실제 하락을 맞춘 비율)
            'Mean_Return': sell_returns.mean() if len(sell_returns) > 0 else 0,  # 매도 시그널 평균 수익률
            'Win_Rate': (sell_returns < 0).mean() if len(sell_returns) > 0 else 0,  # 매도 시그널의 수익 실현 비율
            'Signal_Count': sell_mask.sum(),  # 전체 매도 시그널 발생 횟수
            'Max_Drawdown': max_drawdown,  # 매도 시그널 발생 시점의 최대 손실
            'Volatility': volatility,  # 매도 시그널 수익률의 변동성
            'Sharpe_Ratio': (-sell_returns.mean() / volatility if volatility != 0 else 0)  # 위험 조정 수익률 (음수 반환)
        }
    
    def _process_combination(self, combo: Tuple[str, ...]) -> Dict:
        """단일 시그널 조합 처리 (멀티프로세싱용)"""
        performance = self.calculate_signal_performance(list(combo))
        return {
            'Signals': combo,
            'Signal_Count': len(combo),
            'Accuracy': performance['Accuracy'],
            'Mean_Return': performance['Mean_Return'],
            'Win_Rate': performance['Win_Rate'],
            'Trade_Count': performance['Signal_Count'],
            'Max_Drawdown': performance['Max_Drawdown'],
            'Volatility': performance['Volatility'],
            'Sharpe_Ratio': performance['Sharpe_Ratio']
        }
    
    def find_optimal_combination(self, 
                               max_signals: int = 3,
                               min_signals: int = 2,
                               n_processes: int = None) -> List[Dict]:
        """멀티프로세싱을 활용한 최적 시그널 조합 찾기
        
        Args:
            max_signals (int): 최대 시그널 개수
            min_signals (int): 최소 시그널 개수
            n_processes (int): 사용할 프로세스 수 (None이면 CPU 코어 수 사용)
            
        Returns:
            List[Dict]: 성과가 좋은 시그널 조합 목록
        """
        if n_processes is None:
            n_processes = cpu_count()
            
        signal_columns = [col for col in self.signals.columns if col != 'Date']
        all_combinations = []
        
        # 모든 가능한 조합 생성
        for n in range(min_signals, max_signals + 1):
            all_combinations.extend(combinations(signal_columns, n))
        
        # 멀티프로세싱 실행
        with Pool(n_processes) as pool:
            results = pool.map(self._process_combination, all_combinations)
        
        # 결과 정렬 (정확도와 승률 기준)
        results.sort(key=lambda x: (-x['Accuracy'], -x['Win_Rate']))
        return results

def main():
    # 데이터 로드
    signals_df = pd.read_csv('trading_signals.csv')
    price_data = pd.read_csv('spy_data.csv')
    
    signals_df.set_index('Date', inplace=True)
    price_data.set_index('Date', inplace=True)
    
    optimizer = SignalOptimizer(signals_df, price_data)
    
    # 상관관계 히트맵 생성
    optimizer.calculate_correlation_heatmap()
    
    # 멀티프로세싱으로 최적 조합 찾기
    optimal_combinations = optimizer.find_optimal_combination(
        max_signals=len(signals_df.columns),
        min_signals=4,
        n_processes=cpu_count() - 2
    )
    
    # 결과 데이터프레임 생성 및 저장
    results_df = pd.DataFrame(optimal_combinations)
    
    print("=== 상위 10개 시그널 조합 성과 ===")
    print(results_df[['Signals', 'Accuracy', 'Mean_Return', 'Win_Rate', 
                     'Trade_Count', 'Sharpe_Ratio']].head(10))
    
    # 결과 저장
    results_df.to_csv('optimal_signal_combinations.csv', index=False)

if __name__ == "__main__":
    main()