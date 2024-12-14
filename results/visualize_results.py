#!/usr/bin/env python3
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Tuple

def calculate_model_scores(data: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
    """Calculate success rate, efficiency rate and final score for each model."""
    scores = {}
    total_days = len(data['days'])

    for model in data['models']:
        successful_part1 = 0
        successful_part2 = 0
        total_attempts_part1 = 0
        total_attempts_part2 = 0
        attempted_part1 = 0
        attempted_part2 = 0

        for day in data['days']:
            result = day['results'].get(model, {'part1': '', 'part2': '', 'errors': []})
            
            part1 = result['part1']
            if part1 != 'X' and part1:
                successful_part1 += 1
                try:
                    total_attempts_part1 += int(part1)
                except ValueError:
                    total_attempts_part1 += 1
                attempted_part1 += 1
            
            part2 = result['part2']
            if part2 != 'X' and part2 != '-' and part2:
                successful_part2 += 1
                try:
                    total_attempts_part2 += int(part2)
                except ValueError:
                    total_attempts_part2 += 1
                attempted_part2 += 1

        success_rate = ((successful_part1 + successful_part2) / (2 * total_days)) * 100
        efficiency_rate = (
            (attempted_part1 / total_attempts_part1 if attempted_part1 > 0 else 0) +
            (attempted_part2 / total_attempts_part2 if attempted_part2 > 0 else 0)
        ) * 50
        final_score = (0.7 * success_rate) + (0.3 * efficiency_rate)

        scores[model] = {
            'successRate': success_rate,
            'efficiencyRate': efficiency_rate,
            'finalScore': final_score
        }

    return scores

def get_sorted_models(data: Dict[str, Any]) -> List[str]:
    """Get list of models sorted by their final score."""
    scores = calculate_model_scores(data)
    return sorted(
        data['models'],
        key=lambda m: scores[m]['finalScore'],
        reverse=True
    )

def get_cell_color(value: str) -> str:
    """Return the background color for a cell based on its value."""
    colors = {
        '1': '#90EE90',  # Light green
        '2': '#98FB98',  # Pale green
        '3': '#FFE4B5',  # Light orange
        '4': '#FFA07A',  # Light salmon
        '5': '#FFA500',  # Orange
        'X': '#FFB6C6',  # Light red
        '-': '#FFB6C6',  # Light red
    }
    return colors.get(value, '#FFFFFF')  # Default to white

def generate_rankings_table(data: Dict[str, Any], scores: Dict[str, Dict[str, float]], sorted_models: List[str]) -> str:
    """Generate the HTML for the rankings table."""
    html = ['<table>']
    html.append('    <tr>')
    html.append('        <th align="center">Rank</th>')
    html.append('        <th align="center">Model</th>')
    html.append('        <th align="center">Success Rate</th>')
    html.append('        <th align="center">Efficiency Rate</th>')
    html.append('        <th align="center">Final Score</th>')
    html.append('    </tr>')

    for i, model in enumerate(sorted_models, 1):
        score = scores[model]
        html.append('    <tr>')
        html.append(f'        <td align="center">{i}</td>')
        html.append(f'        <td align="center">{model}</td>')
        html.append(f'        <td align="center">{score["successRate"]:.1f}%</td>')
        html.append(f'        <td align="center">{score["efficiencyRate"]:.1f}%</td>')
        html.append(f'        <td align="center">{score["finalScore"]:.1f}</td>')
        html.append('    </tr>')

    html.append('</table>')
    return '\n'.join(html)

def generate_results_table(data: Dict[str, Any], sorted_models: List[str]) -> str:
    """Generate the HTML for the results table."""
    html = ['<table>']
    
    # Header row 1
    html.append('    <tr>')
    html.append('        <th align="center" rowspan="2">Day</th>')
    for model in sorted_models:
        html.append(f'        <th align="center" colspan="3">{model}</th>')
    html.append('    </tr>')
    
    # Header row 2
    html.append('    <tr>')
    for _ in sorted_models:
        html.append('        <th align="center">P1</th><th align="center">P2</th><th align="center">E</th>')
    html.append('    </tr>')
    
    # Data rows
    for day in data['days']:
        html.append('    <tr>')
        html.append(f'        <td align="center">{day["day"]}</td>')
        
        for model in sorted_models:
            result = day['results'].get(model, {'part1': '', 'part2': '', 'errors': []})
            p1_color = get_cell_color(result.get('part1', ''))
            p2_color = get_cell_color(result.get('part2', ''))
            errors = ','.join(result.get('errors', []))
            
            html.append(f'        <td align="center" bgcolor="{p1_color}">{result.get("part1", "")}</td>')
            html.append(f'        <td align="center" bgcolor="{p2_color}">{result.get("part2", "")}</td>')
            html.append(f'        <td align="center">{errors}</td>')
        
        html.append('    </tr>')
    
    html.append('</table>')
    return '\n'.join(html)

def prepare_data(data: Dict[str, Any]) -> pd.DataFrame:
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

def create_solve_rates_chart(df: pd.DataFrame, sorted_models: List[str], output_dir: Path) -> None:
    """Create a bar chart showing nominal solve counts and first-attempt solve counts."""
    plt.figure(figsize=(15, 8))
    
    nominal_solves = []
    first_attempt_solves = []
    
    for model in sorted_models:
        model_data = df[df['Model'] == model]
        
        # Count nominal solves (anything except 'X' or '-')
        part1_solved = model_data['Part1'].apply(lambda x: x != 'X').sum()
        part2_solved = model_data['Part2'].apply(lambda x: x not in ['X', '-']).sum()
        nominal_solves.append(part1_solved + part2_solved)
        
        # Count first-attempt solves
        part1_first = model_data['Part1'].apply(lambda x: x == '1').sum()
        part2_first = model_data['Part2'].apply(lambda x: x == '1').sum()
        first_attempt_solves.append(part1_first + part2_first)
    
    x = np.arange(len(sorted_models))
    width = 0.8
    
    plt.bar(x, nominal_solves, width, label='Nominal Solves', color='lightblue')
    plt.bar(x, first_attempt_solves, width, label='First Attempt Solves', color='darkblue')
    
    plt.xlabel('Models')
    plt.ylabel('Number of Problems Solved')
    plt.title('Problem Solving Success (out of 16 total problems)')
    plt.xticks(x, sorted_models, rotation=45, ha='right')
    plt.legend()
    plt.grid(True, axis='y')
    
    plt.gca().yaxis.set_major_locator(plt.MultipleLocator(1))
    
    plt.tight_layout()
    plt.savefig(output_dir / 'solve_rates.png', dpi=300, bbox_inches='tight')
    plt.close()

def process_attempt_value(x: str) -> float:
    """Convert attempt values to numerical form, X and - both count as 6"""
    if x in ['X', '-']:
        return 6
    return float(x) if x.isdigit() else 6

def create_metrics_chart(df: pd.DataFrame, sorted_models: List[str], output_dir: Path) -> None:
    """Create a chart showing various average metrics for each model."""
    metrics = {}
    
    for model in sorted_models:
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
    
    plt.figure(figsize=(15, 8))
    
    x = np.arange(len(sorted_models))
    width = 0.2
    
    plt.bar(x - 1.5*width, metrics_df['Avg Attempts Part1'], width, label='Avg Attempts Part 1', color='skyblue')
    plt.bar(x - 0.5*width, metrics_df['Avg Attempts Part2'], width, label='Avg Attempts Part 2', color='lightgreen')
    plt.bar(x + 0.5*width, metrics_df['Avg Attempts Overall'], width, label='Avg Attempts Overall', color='purple')
    plt.bar(x + 1.5*width, metrics_df['Error Rate'], width, label='Error Rate', color='salmon')
    
    plt.xlabel('Models')
    plt.ylabel('Value')
    plt.title('Model Performance Metrics')
    plt.xticks(x, sorted_models, rotation=45, ha='right')
    
    max_value = max(
        metrics_df['Avg Attempts Part1'].max(),
        metrics_df['Avg Attempts Part2'].max(),
        metrics_df['Avg Attempts Overall'].max(),
        metrics_df['Error Rate'].max()
    )
    plt.ylim(0, max_value * 1.1)
    
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
        
        # Load data
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        # Calculate scores and get sorted models
        scores = calculate_model_scores(data)
        sorted_models = get_sorted_models(data)
        
        # Generate tables
        rankings_html = generate_rankings_table(data, scores, sorted_models)
        results_html = generate_results_table(data, sorted_models)
        
        # Save tables
        with open(script_dir / 'rankings.html', 'w', encoding='utf-8') as f:
            f.write(rankings_html)
        with open(script_dir / 'results.html', 'w', encoding='utf-8') as f:
            f.write(results_html)
        
        # Create visualizations
        df = prepare_data(data)
        create_solve_rates_chart(df, sorted_models, output_dir)
        create_metrics_chart(df, sorted_models, output_dir)
        
        print('Generated:')
        print(f'- {script_dir}/rankings.html')
        print(f'- {script_dir}/results.html')
        print(f'- {output_dir}/solve_rates.png')
        print(f'- {output_dir}/performance_metrics.png')
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()