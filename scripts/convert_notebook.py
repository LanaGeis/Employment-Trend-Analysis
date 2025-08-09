import os
import sys

def convert_notebook(notebook_path='../notebooks/milestone5_geissinger.ipynb'):

    # Create output directory path (one level up + output folder)
    output_dir = os.path.join('..', 'output')
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    # Construct and execute the conversion command
    command = f'jupyter nbconvert --to html "{notebook_path}" ' \
              f'--output-dir="{output_dir}" ' \
              '--HTMLExporter.template_name=classic ' \
              '--HTMLExporter.theme=light ' \
              '--TemplateExporter.exclude_input_prompt=True ' \
              '--TagRemovePreprocessor.remove_cell_tags="{\'hide_input\'}" ' \
              '--HTMLExporter.anchor_link_text="" ' \
              '--HTMLExporter.embed_images=True'
    os.system(command)
    # Verify the HTML file was created
    base_name = os.path.basename(notebook_path)
    html_filename = base_name.replace('.ipynb', '.html')
    html_path = os.path.join(output_dir, html_filename)
    if os.path.exists(html_path):
        print(f"HTML file successfully created at: {html_path}")
    else:
        print("Error: HTML file was not created")

if __name__ == "__main__":
    convert_notebook()