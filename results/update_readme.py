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
    """Update README.md by inserting the HTML table content."""
    try:
        # Set paths relative to script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        readme_path = os.path.join(os.path.dirname(script_dir), 'README.md')
        html_path = os.path.join(script_dir, 'results.html')

        # Read the current README.md and results.html
        readme_content = read_file(readme_path)
        try:
            html_table = read_file(html_path)
        except FileNotFoundError:
            print("Could not find results.html")
            return False

        # Define the pattern for the section to replace
        # This captures everything between "## Results" and the next heading or end of file
        results_pattern = r'(## Results\s*)(.*?)(?=\n###|\Z)'
        
        # Create the replacement content with the HTML table
        replacement = r'\1\n\n' + html_table + '\n\n'
        
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
        print("Successfully updated README.md with the HTML table content")
        return True
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    update_readme()