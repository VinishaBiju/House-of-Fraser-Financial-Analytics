"""
House of Fraser Financial Ratio Analysis
Author: Vinisha Biju
Project: House of Fraser Financial Analytics
Description: Calculate and analyze key financial ratios for performance evaluation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class FinancialRatioAnalyzer:
    """
    Calculate and analyze comprehensive financial ratios including:
    - Profitability ratios
    - Liquidity ratios
    - Leverage ratios
    - Efficiency ratios
    """
    
    def __init__(self, income_statement: pd.DataFrame, balance_sheet: pd.DataFrame):
        self.income = income_statement
        self.balance = balance_sheet
        self.ratios = {}
        
    def calculate_profitability_ratios(self) -> Dict:
        """
        Calculate profitability metrics:
        - Gross profit margin
        - Operating profit margin (EBIT margin)
        - Net profit margin
        - Return on Assets (ROA)
        - Return on Equity (ROE)
        """
        print("Calculating profitability ratios...")
        
        profitability = pd.DataFrame({
            'Year': self.income['Year'],
            'Gross_Margin_%': (self.income['Gross_Profit'] / self.income['Revenue']) * 100,
            'EBIT_Margin_%': (self.income['EBIT'] / self.income['Revenue']) * 100,
            'Net_Margin_%': (self.income['Net_Income'] / self.income['Revenue']) * 100
        })
        
        # ROA and ROE
        profitability['ROA_%'] = (self.income['Net_Income'] / self.balance['Total_Assets']) * 100
        profitability['ROE_%'] = (self.income['Net_Income'] / self.balance['Shareholders_Equity']) * 100
        
        self.ratios['profitability'] = profitability
        print("✓ Profitability ratios calculated")
        return profitability
    
    def calculate_liquidity_ratios(self) -> Dict:
        """
        Calculate liquidity metrics:
        - Current ratio
        - Quick ratio (if data available)
        - Working capital
        """
        print("Calculating liquidity ratios...")
        
        liquidity = pd.DataFrame({
            'Year': self.balance['Year'],
            'Current_Ratio': self.balance['Current_Assets'] / self.balance['Current_Liabilities'],
            'Working_Capital': self.balance['Current_Assets'] - self.balance['Current_Liabilities']
        })
        
        # Calculate working capital as % of revenue
        liquidity['WC_to_Revenue_%'] = (liquidity['Working_Capital'] / self.income['Revenue']) * 100
        
        self.ratios['liquidity'] = liquidity
        print("✓ Liquidity ratios calculated")
        return liquidity
    
    def calculate_leverage_ratios(self) -> Dict:
        """
        Calculate leverage/solvency metrics:
        - Debt-to-equity ratio
        - Debt-to-assets ratio
        - Interest coverage ratio
        - Equity multiplier
        """
        print("Calculating leverage ratios...")
        
        leverage = pd.DataFrame({
            'Year': self.balance['Year'],
            'Debt_to_Equity': self.balance['Long_Term_Debt'] / self.balance['Shareholders_Equity'],
            'Debt_to_Assets': self.balance['Long_Term_Debt'] / self.balance['Total_Assets'],
            'Equity_Multiplier': self.balance['Total_Assets'] / self.balance['Shareholders_Equity']
        })
        
        # Interest coverage ratio (EBIT / Interest Expense)
        leverage['Interest_Coverage'] = self.income['EBIT'] / self.income['Interest_Expense']
        
        self.ratios['leverage'] = leverage
        print("✓ Leverage ratios calculated")
        return leverage
    
    def calculate_efficiency_ratios(self) -> Dict:
        """
        Calculate efficiency/activity metrics:
        - Asset turnover ratio
        - Inventory turnover (if data available)
        - Days sales outstanding
        """
        print("Calculating efficiency ratios...")
        
        efficiency = pd.DataFrame({
            'Year': self.income['Year'],
            'Asset_Turnover': self.income['Revenue'] / self.balance['Total_Assets'],
            'Fixed_Asset_Turnover': self.income['Revenue'] / self.balance['Fixed_Assets']
        })
        
        # Calculate efficiency trend
        efficiency['Asset_Turnover_Change_%'] = efficiency['Asset_Turnover'].pct_change() * 100
        
        self.ratios['efficiency'] = efficiency
        print("✓ Efficiency ratios calculated")
        return efficiency
    
    def analyze_dupont_model(self) -> pd.DataFrame:
        """
        Perform DuPont analysis to decompose ROE:
        ROE = Net Margin × Asset Turnover × Equity Multiplier
        """
        print("\nPerforming DuPont analysis...")
        
        dupont = pd.DataFrame({
            'Year': self.income['Year'],
            'Net_Margin_%': (self.income['Net_Income'] / self.income['Revenue']) * 100,
            'Asset_Turnover': self.income['Revenue'] / self.balance['Total_Assets'],
            'Equity_Multiplier': self.balance['Total_Assets'] / self.balance['Shareholders_Equity']
        })
        
        # Calculate ROE from components
        dupont['ROE_Calculated_%'] = (
            dupont['Net_Margin_%'] / 100 * 
            dupont['Asset_Turnover'] * 
            dupont['Equity_Multiplier']
        ) * 100
        
        # Actual ROE for verification
        dupont['ROE_Actual_%'] = (self.income['Net_Income'] / self.balance['Shareholders_Equity']) * 100
        
        print("✓ DuPont analysis complete")
        return dupont
    
    def identify_ratio_trends(self) -> Dict:
        """
        Identify positive and negative trends in key ratios
        """
        print("\nAnalyzing ratio trends...")
        
        trends = {
            'improving': [],
            'declining': [],
            'stable': []
        }
        
        # Analyze each ratio category
        for category, df in self.ratios.items():
            for col in df.columns:
                if col != 'Year' and df[col].dtype in ['float64', 'int64']:
                    values = df[col].dropna()
                    if len(values) > 1:
                        # Calculate overall trend
                        trend = (values.iloc[-1] - values.iloc[0]) / abs(values.iloc[0]) if values.iloc[0] != 0 else 0
                        
                        if trend > 0.1:  # 10% improvement
                            trends['improving'].append(f"{category}.{col}")
                        elif trend < -0.1:  # 10% decline
                            trends['declining'].append(f"{category}.{col}")
                        else:
                            trends['stable'].append(f"{category}.{col}")
        
        print("✓ Trend analysis complete")
        return trends
    
    def generate_ratio_summary(self) -> pd.DataFrame:
        """
        Generate comprehensive summary of all key ratios
        """
        print("\nGenerating ratio summary...")
        
        summary = pd.DataFrame({
            'Year': self.income['Year'],
            'Gross_Margin_%': self.ratios['profitability']['Gross_Margin_%'],
            'EBIT_Margin_%': self.ratios['profitability']['EBIT_Margin_%'],
            'ROE_%': self.ratios['profitability']['ROE_%'],
            'Current_Ratio': self.ratios['liquidity']['Current_Ratio'],
            'Debt_to_Equity': self.ratios['leverage']['Debt_to_Equity'],
            'Asset_Turnover': self.ratios['efficiency']['Asset_Turnover']
        })
        
        print("✓ Summary generated")
        return summary
    
    def benchmark_against_industry(self, industry_benchmarks: Dict) -> pd.DataFrame:
        """
        Compare ratios against industry benchmarks
        Industry benchmarks for UK retail sector
        """
        print("\nBenchmarking against industry standards...")
        
        # Default industry benchmarks for UK retail
        if not industry_benchmarks:
            industry_benchmarks = {
                'Gross_Margin_%': 35.0,
                'EBIT_Margin_%': 5.0,
                'ROE_%': 12.0,
                'Current_Ratio': 1.5,
                'Debt_to_Equity': 1.0,
                'Asset_Turnover': 1.2
            }
        
        summary = self.generate_ratio_summary()
        
        # Calculate variance from industry benchmark
        benchmark_analysis = pd.DataFrame({'Year': summary['Year']})
        
        for metric, benchmark in industry_benchmarks.items():
            if metric in summary.columns:
                benchmark_analysis[f"{metric}_vs_Industry"] = summary[metric] - benchmark
                benchmark_analysis[f"{metric}_Performance"] = benchmark_analysis[f"{metric}_vs_Industry"].apply(
                    lambda x: 'Above' if x > 0 else 'Below'
                )
        
        print("✓ Benchmarking complete")
        return benchmark_analysis
    
    def export_ratios(self, output_path='data/processed/'):
        """
        Export all calculated ratios to CSV files
        """
        print("\nExporting ratio analysis...")
        
        for category, df in self.ratios.items():
            filename = f"{output_path}ratios_{category}.csv"
            # df.to_csv(filename, index=False)
            print(f"✓ Exported {category} ratios to {filename}")
        
        print("\n=== Ratio analysis complete ===")


if __name__ == "__main__":
    print("="*60)
    print("House of Fraser Financial Ratio Analysis")
    print("="*60)
    
    # Sample data - in production, load from data extraction module
    income_data = {
        'Year': [2015, 2016, 2017, 2018],
        'Revenue': [784.9, 826.6, 836.3, 573.1],
        'COGS': [324.7, 342.4, 353.2, 348.9],
        'Gross_Profit': [460.2, 484.2, 483.1, 224.2],
        'Operating_Expenses': [435.5, 465.2, 451.3, 451.3],
        'EBIT': [24.7, 19.0, 31.8, -0.4],
        'Interest_Expense': [15.5, 18.5, 19.7, 19.8],
        'Net_Income': [2.5, 18.4, 14.7, 2.2]
    }
    
    balance_data = {
        'Year': [2015, 2016, 2017, 2018],
        'Total_Assets': [1250.0, 1320.0, 1290.0, 980.0],
        'Current_Assets': [450.0, 480.0, 460.0, 320.0],
        'Fixed_Assets': [800.0, 840.0, 830.0, 660.0],
        'Total_Liabilities': [950.0, 1020.0, 1010.0, 820.0],
        'Current_Liabilities': [380.0, 410.0, 395.0, 290.0],
        'Long_Term_Debt': [570.0, 610.0, 615.0, 530.0],
        'Shareholders_Equity': [300.0, 300.0, 280.0, 160.0]
    }
    
    income_df = pd.DataFrame(income_data)
    balance_df = pd.DataFrame(balance_data)
    
    # Initialize analyzer
    analyzer = FinancialRatioAnalyzer(income_df, balance_df)
    
    # Calculate all ratios
    profitability = analyzer.calculate_profitability_ratios()
    liquidity = analyzer.calculate_liquidity_ratios()
    leverage = analyzer.calculate_leverage_ratios()
    efficiency = analyzer.calculate_efficiency_ratios()
    
    # DuPont analysis
    dupont = analyzer.analyze_dupont_model()
    print(f"\nDuPont ROE (2018): {dupont['ROE_Calculated_%'].iloc[-1]:.2f}%")
    
    # Trend analysis
    trends = analyzer.identify_ratio_trends()
    print(f"\nRatios improving: {len(trends['improving'])}")
    print(f"Ratios declining: {len(trends['declining'])}")
    
    # Industry benchmarking
    benchmark = analyzer.benchmark_against_industry({})
    
    # Export results
    analyzer.export_ratios()
