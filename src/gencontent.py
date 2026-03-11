import os 
import sys
from block_split import *


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Title not found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating path from {from_path} to {dest_path} using {template_path}.")

    with open(from_path, "r") as from_file, open(template_path, "r") as template_file:
        from_content = from_file.read()
        template_content = template_file.read()

        title = extract_title(from_content)

        html_node = markdown_to_html_node(from_content)
        content_html = html_node.to_html()

        final_html = template_content.replace("{{ Title }}", title)
        final_html = final_html.replace("{{ Content }}", content_html)

        final_html = final_html.replace('href="/', 'href="' + basepath)
        final_html = final_html.replace('src="/', 'src="' + basepath)


        dest_dir_path = os.path.dirname(dest_path)
        if dest_dir_path != "":
            os.makedirs(dest_dir_path, exist_ok=True)

        with open(dest_path, "w") as dest_file:
            dest_file.write(final_html)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        current_path = os.path.join(dir_path_content, entry)
        #full path to destination will also include the path from the content folder and its name
        dest_path = os.path.join(dest_dir_path, entry)

        if not os.path.isfile(current_path):
            generate_pages_recursive(current_path, template_path, dest_path, basepath)
        else:
            if current_path.endswith(".md"):
                dest_html_path = dest_path.replace(".md", ".html")
                generate_page(current_path, template_path, dest_html_path, basepath)
    
        


