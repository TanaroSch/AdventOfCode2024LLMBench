#!/usr/bin/env python3
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

def load_data(filename):
    """Load and parse the JSON data."""
    with open(filename, 'r') as f:
        return json.load(f)

def prepare_data(data):
    """Convert JSON data into a pandas DataFrame for easier analysis."""
    rows = []
    for day in data['days']:
        day_num = day['day']
        for model in data['models']:
            result = day['results'].get(model, {})
            part1 = result.get('part1', 'X')
            part2 = result.get('part2', 'X')
            errors = result.get('errors', [])
            
            rows.append({
                'Day': int(day_num),
                'Model': model,
                'Part1': part1,
                'Part2': part2,
                'Errors': ','.join(errors) if errors else ''
            })
    
    return pd.DataFrame(rows)

def create_solve_rates_chart(df, output_dir):
    """Create a bar chart showing nominal solve counts and first-attempt solve counts."""
    plt.figure(figsize=(15, 8))
    
    models = df['Model'].unique()
    
    nominal_solves = []
    first_attempt_solves = []
    
    for model in models:
        model_data = df[df['Model'] == model]
        
        # Count nominal solves (anything except 'X' or '-')
        part1_solved = model_data['Part1'].apply(lambda x: x != 'X').sum()
        part2_solved = model_data['Part2'].apply(lambda x: x not in ['X', '-']).sum()
        nominal_solves.append(part1_solved + part2_solved)
        
        # Count first-attempt solves
        part1_first = model_data['Part1'].apply(lambda x: x == '1').sum()
        part2_first = model_data['Part2'].apply(lambda x: x == '1').sum()
        first_attempt_solves.append(part1_first + part2_first)
    
    x = np.arange(len(models))
    width = 0.8
    
    plt.bar(x, nominal_solves, width, label='Nominal Solves', color='lightblue')
    plt.bar(x, first_attempt_solves, width, label='First Attempt Solves', color='darkblue')
    
    plt.xlabel('Models')
    plt.ylabel('Number of Problems Solved')
    plt.title('Problem Solving Success (out of 16 total problems)')
    plt.xticks(x, models, rotation=45, ha='right')
    plt.legend()
    plt.grid(True, axis='y')
    
    # Set y-axis to show whole numbers
    plt.gca().yaxis.set_major_locator(plt.MultipleLocator(1))
    
    plt.tight_layout()
    plt.savefig(output_dir / 'solve_rates.png', dpi=300, bbox_inches='tight')
    plt.close()

def process_attempt_value(x):
    """Convert attempt values to numerical form, X and - both count as 6"""
    if x in ['X', '-']:
        return 6
    return float(x) if x.isdigit() else 6

def create_metrics_chart(df, output_dir):
    """Create a chart showing various average metrics for each model."""
    models = df['Model'].unique()
    metrics = {}
    
    for model in models:
        model_data = df[df['Model'] == model]
        
        # Convert attempts to numerical values
        part1_attempts = model_data['Part1'].apply(process_attempt_value)
        part2_attempts = model_data['Part2'].apply(process_attempt_value)
        
        # Calculate averages
        metrics[model] = {
            'Avg Attempts Part1': part1_attempts.mean(),
            'Avg Attempts Part2': part2_attempts.mean(),
            'Avg Attempts Overall': pd.concat([part1_attempts, part2_attempts]).mean(),
            'Error Rate': len(model_data[model_data['Errors'] != '']) / len(model_data)
        }
    
    # Convert to DataFrame for plotting
    metrics_df = pd.DataFrame(metrics).T
    
    # Create the visualization
    plt.figure(figsize=(15, 8))
    
    x = np.arange(len(models))
    width = 0.2  # Reduced width to accommodate fourth bar
    
    # Plot bars
    plt.bar(x - 1.5*width, metrics_df['Avg Attempts Part1'], width, label='Avg Attempts Part 1', color='skyblue')
    plt.bar(x - 0.5*width, metrics_df['Avg Attempts Part2'], width, label='Avg Attempts Part 2', color='lightgreen')
    plt.bar(x + 0.5*width, metrics_df['Avg Attempts Overall'], width, label='Avg Attempts Overall', color='purple')
    plt.bar(x + 1.5*width, metrics_df['Error Rate'], width, label='Error Rate', color='salmon')
    
    plt.xlabel('Models')
    plt.ylabel('Value')
    plt.title('Model Performance Metrics')
    plt.xticks(x, models, rotation=45, ha='right')
    
    # Set y-axis limits dynamically
    max_value = max(
        metrics_df['Avg Attempts Part1'].max(),
        metrics_df['Avg Attempts Part2'].max(),
        metrics_df['Avg Attempts Overall'].max(),
        metrics_df['Error Rate'].max()
    )
    plt.ylim(0, max_value * 1.1)  # Add 10% padding
    
    # Add grid
    plt.grid(True, axis='y')
    
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(output_dir / 'performance_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    try:
        # Set up directories
        script_dir = Path(__file__).parent
        data_file = script_dir / 'data.json'
        output_dir = script_dir / 'graphs'
        output_dir.mkdir(exist_ok=True)
        
        # Load and prepare data
        data = load_data(data_file)
        df = prepare_data(data)
        
        # Create visualizations
        create_solve_rates_chart(df, output_dir)
        create_metrics_chart(df, output_dir)
        
        print("Graphs have been generated in the 'graphs' directory.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()