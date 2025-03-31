#!/usr/bin/env python3

import os
import subprocess
import sys

def clone_repo(repo_name, repo_url):
    
    if not os.path.exists(repo_name):
        print(f"Cloning {repo_name}...")
        try:
            subprocess.run(['git', 'clone', repo_url, repo_name], check=True)
            print(f"Successfully cloned {repo_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error cloning {repo_name}: {e}")
    else:
        print(f"Directory {repo_name} already exists, skipping...")

def main():

    repos = {
        'altair': 'https://github.com/altair-viz/altair.git',
        'holoviews': 'https://github.com/holoviz/holoviews.git',
        'matplotlib': 'https://github.com/matplotlib/matplotlib.git',
        'plotly': 'https://github.com/plotly/plotly.py.git',
        'plotnine': 'https://github.com/has2k1/plotnine.git',
        'pygal': 'https://github.com/Kozea/pygal.git',
        'seaborn': 'https://github.com/mwaskom/seaborn.git'
    }
    

    for repo_name, repo_url in repos.items():
        clone_repo(repo_name, repo_url)


if __name__ == "__main__":
    main()