"""
Owner: Kevin B
Contributors: N/A
Date Created: 20211008

Summary:
    Quick script to install python libraries/packages

"""

# Preinstall Python Packages
import os
import sys
import subprocess

# Install a packagae using pip from CMD line - Thank you stackoverflow
def install(package_name):
    """Execute pip install from command line """
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# Updates pip
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

# Getting the path of the script and extracting dir name
folder_path = os.path.dirname(os.path.realpath(__file__))

# Forming abs file path to text file
file_path = os.path.join(folder_path, "requirements.txt")

# Getting list of packages to install from text file
with open(file_path) as f:
    text = f.read()

# Splitting test files
packages_list = text.split("\n")

# Installing each package
for pkg in packages_list:
    install(pkg)
