import os
import shutil
import argparse
import nbformat

def copy_and_rename_template(template_folder, destination_folder, new_name):
    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Get list of files in template folder
    for root, dirs, files in os.walk(template_folder):
        # Get the relative path from the template folder
        rel_path = os.path.relpath(root, template_folder)
        dest_root = os.path.join(destination_folder, rel_path)

        # Create directories if they don't exist
        for dir_name in dirs:
            dest_dir = os.path.join(dest_root, dir_name)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

        # Copy files that don't exist
        for filename in files:
            src_file = os.path.join(root, filename)
            dest_file = os.path.join(dest_root, filename)

            # Only copy if file doesn't exist in destination
            if not os.path.exists(dest_file):
                # If it's a notebook file, copy and modify
                if filename.endswith(".ipynb"):
                    with open(src_file, 'r', encoding='utf-8') as f:
                        nb = nbformat.read(f, as_version=4)
                    
                    # Modify the first cell if it's a Markdown cell
                    if nb.cells and nb.cells[0].cell_type == 'markdown':
                        first_cell = nb.cells[0]
                        if first_cell.source.startswith("# Day XX -"):
                            first_cell.source = first_cell.source.replace("XX", new_name)
                    
                    # Write the modified notebook to destination
                    with open(dest_file, 'w', encoding='utf-8') as f:
                        nbformat.write(nb, f)
                else:
                    # For non-notebook files, just copy
                    shutil.copy2(src_file, dest_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Copy template folder and rename files.')
    parser.add_argument('--name', required=True, help='New name to replace XX in the files')
    
    args = parser.parse_args()
    
    template_folder = os.path.join(os.getcwd(), 'template')
    destination_folder = os.path.join(os.getcwd(), args.name)
    
    copy_and_rename_template(template_folder, destination_folder, args.name)