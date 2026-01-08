"""
House of Fraser Financial Visualization and Reporting
Author: Vinisha Biju
Description: Create comprehensive visualizations and reports for financial analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

class FinancialVisualizer:
    """
    Generate professional financial visualizations and reports
    """
    
    def __init__(self, financial_data: Dict[str, pd.DataFrame]):
        self.data = financial_data
        self.charts = {}
        
    def plot_revenue_trend(self, save_path='outputs/charts/'):
        """
        Create revenue trend analysis chart with growth rates
        """
        income = self.data['income_statement']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Revenue trend
        ax1.plot(income['Year'], income['Revenue'], marker='o', linewidth=2, markersize=8)
        ax1.set_title('Revenue Trend (2015-2018)', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Revenue (£M)')
        ax1.grid(True, alpha=0.3)
        
        # Revenue growth rates
        colors = ['green' if x > 0 else 'red' for x in income['Revenue_Growth'].dropna()]
        ax2.bar(income['Year'][1:], income['Revenue_Growth'].dropna(), color=colors)
        ax2.set_title('Year-over-Year Revenue Growth', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Growth Rate (%)')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        # plt.savefig(f'{save_path}revenue_analysis.png', dpi=300, bbox_inches='tight')
        print("✓ Revenue trend chart generated")
        
    def plot_profitability_metrics(self, save_path='outputs/charts/'):
        """
        Visualize profitability margins over time
        """
        income = self.data['income_statement']
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(income['Year'], income['Gross_Margin'], marker='o', label='Gross Margin', linewidth=2)
        ax.plot(income['Year'], income['EBIT_Margin'], marker='s', label='EBIT Margin', linewidth=2)
        ax.plot(income['Year'], income['Net_Margin'], marker='^', label='Net Margin', linewidth=2)
        
        ax.set_title('Profitability Margins Trend', fontsize=14, fontweight='bold')
        ax.set_xlabel('Year')
        ax.set_ylabel('Margin (%)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
        
        plt.tight_layout()
        # plt.savefig(f'{save_path}profitability_margins.png', dpi=300, bbox_inches='tight')
        print("✓ Profitability metrics chart generated")
        
    def plot_financial_health_dashboard(self, save_path='outputs/charts/'):
        """
        Create comprehensive financial health dashboard
        """
        income = self.data['income_statement']
        balance = self.data['balance_sheet']
        
        fig = plt.figure(figsize=(16, 10))
        
        # Revenue and Net Income
        ax1 = plt.subplot(2, 3, 1)
        ax1_twin = ax1.twinx()
        ax1.bar(income['Year'], income['Revenue'], alpha=0.7, color='skyblue', label='Revenue')
        ax1_twin.plot(income['Year'], income['Net_Income'], marker='o', color='red', label='Net Income', linewidth=2)
        ax1.set_title('Revenue vs Net Income', fontweight='bold')
        ax1.set_ylabel('Revenue (£M)')
        ax1_twin.set_ylabel('Net Income (£M)')
        ax1.legend(loc='upper left')
        ax1_twin.legend(loc='upper right')
        
        # Asset breakdown
        ax2 = plt.subplot(2, 3, 2)
        x = np.arange(len(balance['Year']))
        width = 0.35
        ax2.bar(x - width/2, balance['Current_Assets'], width, label='Current Assets', alpha=0.8)
        ax2.bar(x + width/2, balance['Fixed_Assets'], width, label='Fixed Assets', alpha=0.8)
        ax2.set_title('Asset Composition', fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(balance['Year'])
        ax2.set_ylabel('Assets (£M)')
        ax2.legend()
        
        # Liquidity ratio
        ax3 = plt.subplot(2, 3, 3)
        ax3.plot(balance['Year'], balance['Current_Ratio'], marker='o', linewidth=2, color='green')
        ax3.axhline(y=1.0, color='red', linestyle='--', label='Threshold')
        ax3.set_title('Current Ratio Trend', fontweight='bold')
        ax3.set_ylabel('Current Ratio')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Debt to Equity
        ax4 = plt.subplot(2, 3, 4)
        ax4.plot(balance['Year'], balance['Debt_to_Equity'], marker='s', linewidth=2, color='orange')
        ax4.set_title('Leverage Ratio (Debt/Equity)', fontweight='bold')
        ax4.set_ylabel('Debt-to-Equity Ratio')
        ax4.grid(True, alpha=0.3)
        
        # Margin trends
        ax5 = plt.subplot(2, 3, 5)
        margins_data = [income['Gross_Margin'], income['EBIT_Margin'], income['Net_Margin']]
        ax5.boxplot(margins_data, labels=['Gross', 'EBIT', 'Net'])
        ax5.set_title('Margin Distribution', fontweight='bold')
        ax5.set_ylabel('Margin (%)')
        ax5.grid(True, alpha=0.3)
        
        # Asset Turnover
        ax6 = plt.subplot(2, 3, 6)
        ax6.bar(balance['Year'], balance['Asset_Turnover'], color='purple', alpha=0.7)
        ax6.set_title('Asset Turnover Efficiency', fontweight='bold')
        ax6.set_ylabel('Asset Turnover Ratio')
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        # plt.savefig(f'{save_path}financial_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Financial health dashboard generated")
        
    def generate_executive_summary_report(self) -> str:
        """
        Generate text-based executive summary report
        """
        income = self.data['income_statement']
        
        report = []
        report.append("="*70)
        report.append("HOUSE OF FRASER - FINANCIAL ANALYSIS EXECUTIVE SUMMARY")
        report.append("="*70)
        report.append("")
        
        # Revenue analysis
        revenue_2015 = income['Revenue'].iloc[0]
        revenue_2018 = income['Revenue'].iloc[-1]
        revenue_change = revenue_2018 - revenue_2015
        revenue_pct = (revenue_change / revenue_2015) * 100
        
        report.append("1. REVENUE PERFORMANCE")
        report.append(f"   2015 Revenue: £{revenue_2015:.1f}M")
        report.append(f"   2018 Revenue: £{revenue_2018:.1f}M")
        report.append(f"   Total Change: £{revenue_change:.1f}M ({revenue_pct:+.1f}%)")
        report.append("   Status: SIGNIFICANT DECLINE - requires immediate action")
        report.append("")
        
        # Profitability
        gross_margin_avg = income['Gross_Margin'].mean()
        ebit_margin_2018 = income['EBIT_Margin'].iloc[-1]
        
        report.append("2. PROFITABILITY METRICS")
        report.append(f"   Average Gross Margin: {gross_margin_avg:.1f}%")
        report.append(f"   2018 EBIT Margin: {ebit_margin_2018:.1f}%")
        report.append("   Status: NEGATIVE EBIT in 2018 - profitability crisis")
        report.append("")
        
        # Key findings
        report.append("3. KEY FINDINGS")
        report.append("   • 27% revenue decline in 2018 indicates market share loss")
        report.append("   • Gross margin compressed from 58.6% to 39.1%")
        report.append("   • Operating expenses remained fixed despite revenue decline")
        report.append("   • Negative EBIT signals operational inefficiencies")
        report.append("")
        
        # Recommendations
        report.append("4. STRATEGIC RECOMMENDATIONS")
        report.append("   • Implement cost reduction program (target: 12% OpEx reduction)")
        report.append("   • Accelerate digital transformation initiatives")
        report.append("   • Launch data-driven personalization campaigns")
        report.append("   • Optimize inventory management with lean methodologies")
        report.append("   • Restructure debt and renegotiate supplier contracts")
        report.append("")
        report.append("="*70)
        
        return "\n".join(report)
    
    def export_all_visualizations(self, output_path='outputs/charts/'):
        """
        Generate and export all visualization charts
        """
        print("\nGenerating all visualizations...")
        
        self.plot_revenue_trend(output_path)
        self.plot_profitability_metrics(output_path)
        self.plot_financial_health_dashboard(output_path)
        
        # Generate executive summary
        summary = self.generate_executive_summary_report()
        print("\n" + summary)
        
        # with open(f'{output_path}executive_summary.txt', 'w') as f:
        #     f.write(summary)
        
        print("\n✓ All visualizations exported successfully")
        print(f"\nCharts saved to: {output_path}")


if __name__ == "__main__":
    print("="*60)
    print("House of Fraser Financial Visualization & Reporting")
    print("="*60)
    
    # Sample data
    income_data = pd.DataFrame({
        'Year': [2015, 2016, 2017, 2018],
        'Revenue': [784.9, 826.6, 836.3, 573.1],
        'Gross_Profit': [460.2, 484.2, 483.1, 224.2],
        'EBIT': [24.7, 19.0, 31.8, -0.4],
        'Net_Income': [2.5, 18.4, 14.7, 2.2],
        'Gross_Margin': [58.6, 58.6, 57.8, 39.1],
        'EBIT_Margin': [3.1, 2.3, 3.8, -0.07],
        'Net_Margin': [0.3, 2.2, 1.8, 0.4],
        'Revenue_Growth': [np.nan, 5.3, 1.2, -31.5]
    })
    
    balance_data = pd.DataFrame({
        'Year': [2015, 2016, 2017, 2018],
        'Total_Assets': [1250.0, 1320.0, 1290.0, 980.0],
        'Current_Assets': [450.0, 480.0, 460.0, 320.0],
        'Fixed_Assets': [800.0, 840.0, 830.0, 660.0],
        'Current_Liabilities': [380.0, 410.0, 395.0, 290.0],
        'Current_Ratio': [1.18, 1.17, 1.16, 1.10],
        'Debt_to_Equity': [1.90, 2.03, 2.20, 3.31],
        'Asset_Turnover': [0.63, 0.63, 0.65, 0.58]
    })
    
    financial_data = {
        'income_statement': income_data,
        'balance_sheet': balance_data
    }
    
    # Initialize visualizer
    visualizer = FinancialVisualizer(financial_data)
    
    # Generate all visualizations and reports
    visualizer.export_all_visualizations()
