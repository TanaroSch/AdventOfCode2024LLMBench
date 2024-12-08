#!/usr/bin/env python3
import re
import os

def read_file(filename):
    """Read the content of a file."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filename, content):
    """Write content to a file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def update_readme():
    """Update README.md by inserting both rankings and results tables."""
    try:
        # Set paths relative to script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        readme_path = os.path.join(os.path.dirname(script_dir), 'README.md')
        results_path = os.path.join(script_dir, 'results.html')
        rankings_path = os.path.join(script_dir, 'rankings.html')

        # Read the current files
        readme_content = read_file(readme_path)
        try:
            results_table = read_file(results_path)
            rankings_table = read_file(rankings_path)
        except FileNotFoundError as e:
            print(f"Could not find table file: {e.filename}")
            return False

        # Define the pattern for the section to replace
        # This captures everything between "## Results" and the next heading or end of file
        results_pattern = r'(## Results\s*)(.*?)(?=\n### Data|\Z)'
        
        # Create the replacement content with both tables and proper sections
        replacement = r'\1\n\n' + \
            '### Model Rankings\n' + \
            'The models are ranked using a composite score:\n' + \
            '- **Success Rate** (70% weight): Percentage of problems solved (both parts)\n' + \
            '- **Efficiency Rate** (30% weight): Average solve efficiency (1/number of attempts)\n' + \
            '- **Final Score** = (Success Rate × 0.7) + (Efficiency Rate × 0.3)\n\n' + \
            rankings_table + \
            '\n\n### Detailed Results\n' + \
            'Color coding:\n' + \
            '- 🟩 One attempt (green)\n' + \
            '- 🟨 Multiple attempts (yellow/orange)\n' + \
            '- 🟥 Failed/Not attempted (red)\n' + \
            '- E column shows error types: (l)ogic, (s)yntax\n\n' + \
            results_table + '\n'
        
        # Check if we can find the Results section
        if not re.search(results_pattern, readme_content, re.DOTALL):
            print("Could not find the Results section in README.md")
            return False
        
        # Replace the content
        new_content = re.sub(
            results_pattern,
            replacement,
            readme_content,
            flags=re.DOTALL
        )
        
        # Write the updated content back to README.md
        write_file(readme_path, new_content)
        print("Successfully updated README.md with both rankings and results tables")
        return True
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    update_readme()