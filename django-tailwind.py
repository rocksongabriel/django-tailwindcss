"""
    Author: Gabriel Rockson
    Purpose of Script: To set up tailwindcss in the base of a django project using the postcss method.
"""

import json
import os
import subprocess
import sys

# the original working directory in which the script is run
original_working_directory = os.getcwd()

# geneate the package.json file
init_process = subprocess.run(["npm", "init", "-y"])

# install the required packages
if init_process.returncode == 0:
    install_process = subprocess.run(["npm", "install", "tailwindcss", "postcss", "postcss-cli", "autoprefixer"])

# creating tailwind.config.js file for later customization
if init_process.returncode == 0:
    gen_tailwindconfig_process = subprocess.run(["npx", "tailwindcss", "init"])

# create the postcss.config.js file in the same directory as tailwind.config.js
if gen_tailwindconfig_process == 0:
    touch_postcss_process = subprocess.run(["touch", "postcss.config.js"])

# write the base config lines to the postcss.config.js file
with open("postcss.config.js", "w") as file:
    file.write(
        "module.exports = {\n\tplugins: [\n\t\trequire('tailwindcss'),\n\t\trequire('autoprefixer'),\n\t]\n}"
    )

# create a base css file in a css directory and add the 3 base directives
if os.path.isdir("css"):
    os.chdir(os.getcwd() + "/css")
    if os.path.isfile("tailwind.css"):
        print("tailwindcss already exists")
    else:
        create_base_css_dir_process = subprocess.run(["touch", "tailwind.css"])
else:
    os.mkdir("css")
    os.chdir(os.getcwd() + "/css")
create_base_css_dir_process = subprocess.run(["touch", "tailwind.css"])

# add the base directives to the css file
with open("tailwind.css", "w") as file: 
    file.write(
        "@tailwind base\n@tailwind components\n@tailwind utilities\n"
    )

os.chdir(original_working_directory) # change to the dir the script was run in


# get the directory to put the build file in

# make sure that the static directory exists and we are working there
project_name = sys.argv[1]
os.chdir(os.getcwd() + f"/{project_name}")
if os.path.isdir("static"):
    os.chdir(os.getcwd() + "/static")
    if os.path.isdir("css"):
        os.chdir(os.getcwd() + "/css")
    else:
        os.mkdir("css")
else:
    os.makedirs("static/css/")
    os.chdir(os.getcwd() + "/static/css")

build_css = os.getcwd() + "/tailwind.css"

os.chdir(original_working_directory) # change to the dir the script was run in

# write add the build script to the package.json
# read the package.json file into a dict
with open("package.json") as f:
    data = json.load(f)

# write the dict to the package.json
with open("package.json", "w") as f:
    data["scripts"]["build"] = f"build css/tailwind.css -o {build_css}"
    json.dump(data, f, indent=4)

# Now run the build
build_process = subprocess.run(["npm", "run", "build"])
if build_process.returncode == 0:
    print("The build happened successfully")


# TODO - add the node_modules to .gitignore