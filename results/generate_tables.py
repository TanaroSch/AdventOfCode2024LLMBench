import json
from typing import Dict, Any

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
            # Get result with default empty values if model isn't present
            result = day['results'].get(model, {'part1': '', 'part2': '', 'errors': []})
            
            part1 = result['part1']
            if part1 != 'X' and part1:  # Check if not 'X' and not empty
                successful_part1 += 1
                try:
                    total_attempts_part1 += int(part1)
                except ValueError:
                    total_attempts_part1 += 1  # Default to 1 attempt if value is invalid
                attempted_part1 += 1
            
            part2 = result['part2']
            if part2 != 'X' and part2 != '-' and part2:  # Check if not 'X', not '-', and not empty
                successful_part2 += 1
                try:
                    total_attempts_part2 += int(part2)
                except ValueError:
                    total_attempts_part2 += 1  # Default to 1 attempt if value is invalid
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

def generate_rankings_table(data: Dict[str, Any], scores: Dict[str, Dict[str, float]]) -> str:
    """Generate the HTML for the rankings table."""
    sorted_models = sorted(
        data['models'],
        key=lambda m: scores[m]['finalScore'],
        reverse=True
    )

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

def generate_results_table(data: Dict[str, Any], sorted_models: list) -> str:
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
            # Get result with default empty values if model isn't present
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

def generate_tables(data_path: str, rankings_path: str, results_path: str) -> None:
    """Main function to generate both HTML tables."""
    try:
        # Read the JSON data
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Calculate scores
        scores = calculate_model_scores(data)
        sorted_models = sorted(
            data['models'],
            key=lambda m: scores[m]['finalScore'],
            reverse=True
        )

        # Generate and save rankings table
        rankings_html = generate_rankings_table(data, scores)
        with open(rankings_path, 'w', encoding='utf-8') as f:
            f.write(rankings_html)

        # Generate and save results table
        results_html = generate_results_table(data, sorted_models)
        with open(results_path, 'w', encoding='utf-8') as f:
            f.write(results_html)

        print('Generated:')
        print(f'- {rankings_path}')
        print(f'- {results_path}')

    except Exception as e:
        print(f'Error generating tables: {str(e)}')

if __name__ == '__main__':
    generate_tables('data.json', 'rankings.html', 'results.html')