from textnode import *
import os
import shutil
from gencontent import *
import sys


def copy_files(source, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)
    
    for item in os.listdir(source):
        from_path = os.path.join(source, item)
        to_path = os.path.join(dest, item)

        print(f" * {from_path} -> {to_path}")

        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            copy_files(from_path, to_path)


def main():

    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]


    source_static = "./static"
    dest_public = "./docs"

    print("Cleaning public dir before copying...")
    if os.path.exists(dest_public):
        shutil.rmtree(dest_public)
    
    print("Copying static files into docs dir...")
    copy_files(source_static, dest_public)

    generate_pages_recursive("./content", "./template.html", dest_public, basepath)
    



if __name__ == "__main__":
    main()
