import os
import shutil
import argparse
import nbformat

def copy_and_rename_template(template_folder, destination_folder, new_name):
    # Copy the template folder to the new destination
    shutil.copytree(template_folder, destination_folder)

    # Iterate over all files in the destination folder
    for filename in os.listdir(destination_folder):
        if filename.endswith(".ipynb"):
            file_path = os.path.join(destination_folder, filename)
            
            # Read the notebook
            with open(file_path, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
            
            # Modify the first cell if it's a Markdown cell
            if nb.cells and nb.cells[0].cell_type == 'markdown':
                first_cell = nb.cells[0]
                if first_cell.source.startswith("# Day XX -"):
                    first_cell.source = first_cell.source.replace("XX", new_name)
            
            # Write the modified notebook back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Copy template folder and rename files.')
    parser.add_argument('--name', required=True, help='New name to replace XX in the files')
    
    args = parser.parse_args()
    
    template_folder = os.path.join(os.getcwd(), 'template')
    destination_folder = os.path.join(os.getcwd(), args.name)
    
    copy_and_rename_template(template_folder, destination_folder, args.name)