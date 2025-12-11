#!/usr/bin/env python3
"""
Create a correlation heatmap showing which lifestyle factors occur together.
Converts YES_MANUAL to True and all other values to False.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def load_and_process_data(csv_path):
    """Load CSV and convert YES_MANUAL to True, everything else to False."""
    # Load the data
    df = pd.read_csv(csv_path)
    
    # Skip the Date column
    data_columns = df.columns[1:]
    
    # Create a binary dataframe (True for YES_MANUAL, False for everything else)
    binary_df = pd.DataFrame()
    for col in data_columns:
        binary_df[col] = df[col] == 'YES_MANUAL'
    
    return binary_df

def create_correlation_heatmap(binary_df, output_path='correlation_heatmap.png'):
    """Create and save a correlation heatmap."""
    # Calculate correlation matrix
    correlation_matrix = binary_df.corr()
    
    # Create a figure with appropriate size
    plt.figure(figsize=(24, 20))
    
    # Create the heatmap
    sns.heatmap(
        correlation_matrix,
        annot=False,  # Don't show values in cells (too many columns)
        cmap='RdBu_r',  # Red-Blue colormap (red = positive correlation)
        center=0,  # Center colormap at 0
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8, "label": "Correlation Coefficient"}
    )
    
    # Rotate labels for better readability
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    
    # Add title
    plt.title('Lifestyle Factors Co-occurrence Heatmap\n(YES_MANUAL only)', 
              fontsize=16, pad=20)
    
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Heatmap saved to: {output_path}")
    
    return correlation_matrix

def find_top_correlations(correlation_matrix, n=20):
    """Find and display the top N correlated factor pairs."""
    # Get the correlation matrix as a series, excluding diagonal
    corr_pairs = correlation_matrix.unstack()
    
    # Remove self-correlations and duplicates
    corr_pairs = corr_pairs[corr_pairs < 1.0]
    
    # Sort by absolute correlation value
    top_correlations = corr_pairs.abs().sort_values(ascending=False).head(n)
    
    print(f"\nTop {n} Factor Correlations (YES_MANUAL only):")
    print("=" * 80)
    
    for (factor1, factor2), _ in top_correlations.items():
        corr_value = correlation_matrix.loc[factor1, factor2]
        print(f"{factor1:30s} <-> {factor2:30s} : {corr_value:6.3f}")
    
    return top_correlations

def print_summary_statistics(binary_df):
    """Print summary statistics about the data."""
    print("\nData Summary:")
    print("=" * 80)
    print(f"Total number of records: {len(binary_df)}")
    print(f"Total number of factors: {len(binary_df.columns)}")
    print(f"\nFactor occurrence counts (YES_MANUAL):")
    print("-" * 80)
    
    # Count YES_MANUAL occurrences for each factor
    counts = binary_df.sum().sort_values(ascending=False)
    
    for factor, count in counts.items():
        if count > 0:  # Only show factors with at least one YES_MANUAL
            percentage = (count / len(binary_df)) * 100
            print(f"{factor:40s}: {count:4d} times ({percentage:5.1f}%)")

def main():
    # Set up paths
    script_dir = Path(__file__).parent
    csv_path = script_dir / 'Checkmarks.csv'
    output_path = script_dir / 'correlation_heatmap.png'
    
    print("Loading and processing data...")
    binary_df = load_and_process_data(csv_path)
    
    # Print summary statistics
    print_summary_statistics(binary_df)
    
    # Create correlation heatmap
    print("\nCreating correlation heatmap...")
    correlation_matrix = create_correlation_heatmap(binary_df, output_path)
    
    # Find and display top correlations
    find_top_correlations(correlation_matrix, n=30)
    
    # Save correlation matrix to CSV for further analysis
    corr_csv_path = script_dir / 'correlation_matrix.csv'
    correlation_matrix.to_csv(corr_csv_path)
    print(f"\nCorrelation matrix saved to: {corr_csv_path}")

if __name__ == '__main__':
    main()

