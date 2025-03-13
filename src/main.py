import pandas as pd
from technical_indicator import CORE16MomentumIndicator, CORE16ContrarianIndicator
from signal_generator import SignalGenerator
from visualizer import TAVisualizer

def main():
    # 데이터 로드
    
    data = pd.read_csv('data/raw/spy_data.csv', index_col='Date', parse_dates=True)
    
    input_data = data.copy()
    
    # 기술적 지표 계산
    momentum_indicator = CORE16MomentumIndicator(input_data, resample='1d')
    contrarian_indicator = CORE16ContrarianIndicator(input_data, resample='1d')
    
    # 지표 계산
    momentum_df = momentum_indicator.calculate_all_indicators()
    contrarian_df = contrarian_indicator.calculate_all_indicators()
    
    # 모든 지표를 하나의 데이터프레임으로 통합
    combined_df = pd.concat([data, momentum_df, contrarian_df], axis=1).round(4)
    combined_df.to_csv('data/processed/combined_indicators.csv')
    
    # 신호 생성
    signal_generator = SignalGenerator(combined_df)
    momentum_signals = signal_generator.generate_momentum_signals()
    contrarian_signals = signal_generator.generate_contrarian_signals()
    
    # 모든 신호를 하나의 데이터프레임으로 통합
    all_signals = pd.concat([momentum_signals, contrarian_signals], axis=1).round(4)
    
    all_signals.to_csv('data/processed/trading_signals.csv')
    
    # 시각화
    visualizer = TAVisualizer(combined_df, all_signals)
    visualizer.create_base_chart()
    visualizer.add_momentum_indicators()
    visualizer.add_contrarian_indicators()
    visualizer.add_signals()
    visualizer.save('output/figures/technical_analysis.html')
    visualizer.show()
    

if __name__ == "__main__":
    main() 