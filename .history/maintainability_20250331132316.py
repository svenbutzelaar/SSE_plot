#!/usr/bin/env python3

import os
import sys
import math	
import statistics
from collections import defaultdict
import radon.metrics as metrics
import radon.complexity as complexity
from radon.visitors import ComplexityVisitor, HalsteadVisitor
import ast
from radon.raw import analyze
from radon.visitors import ComplexityVisitor
from radon.metrics import h_visit_ast, h_visit, mi_visit
from radon.complexity import cc_visit

from visualization_repos.plotly._plotly_utils.basevalidators import copy_to_readonly_numpy_array
def calculate_maintainability_index(file_path):
    """
    Calculate maintainability index for a file using radon
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        raw_metrics = analyze(content)
        loc = raw_metrics.lloc
        ast_code = ast.parse(content)

        cc_score  =   ComplexityVisitor.from_ast(ast_code).total_complexity
        halstead_volume =  h_visit(ast_code).total.volume

        if halstead_volume <= 0  or loc <= 0:
            return 100.0
    
        # result  = 171 - 5.2 * math.log(halstead_volume) - 0.23 * cc_score - 16.2 * math.log(loc)
        # result = mi_visit(content, True)
        result = max(0, (171 -  5.2 * math.log(halstead_volume) - 0.23 * cc_score - 16.2 * math.log(loc))*100 /171  )
        return result
    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return None

def analyze_repos(base_dir="visualization_repos"):

    repo_scores = defaultdict(list)
    
    repos = [d for d in os.listdir(base_dir) 
             if os.path.isdir(os.path.join(base_dir, d))]
    
    for repo in repos:
        repo_path = os.path.join(base_dir, repo)
        
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    mi_score = calculate_maintainability_index(file_path)
                    
                    if mi_score is not None:
                        repo_scores[repo].append(mi_score)
                      
    print("\n=== Repository Maintainability Summary ===")
    print("Repo Name                 | Avg. MI | # Files | Interpretation")
    print("-" * 65)
    
    for repo, scores in sorted(repo_scores.items(), 
                              key=lambda x: statistics.mean(x[1]) if x[1] else 0, 
                              reverse=True):
        if scores:
            avg_score = statistics.mean(scores)
            interpretation = interpret_mi_score(avg_score)
            print(f"{repo:<25} | {avg_score:>7.2f} | {len(scores):>7d} | {interpretation}")
        else:
            print(f"{repo:<25} | No Python files found")

def interpret_mi_score(score):
    if score >= 85:
        return "Excellent maintainability"
    elif score >= 65:
        return "Good maintainability"
    elif score >= 40:
        return "Moderate maintainability"
    else:
        return "Poor maintainability"

if __name__ == "__main__":
    print("Analyzing repository maintainability...")
    analyze_repos()
    print("\nAnalysis complete!")