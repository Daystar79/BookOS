#!/usr/bin/env python3
"""
Framework Pull Script — BookOS
------------------------------
Pulls the latest core framework files and writing mechanics from the upstream 
CognitiveMiddleware (Authors_Framework) to keep this project in sync.
"""

import os
import shutil
import sys

# Upstream source directory containing the Psyche Matrix Framework
UPSTREAM_NAME = "Authors_Framework"

FRAMEWORK_FILES = [
    "Framework/Main.md",
    "Framework/Rules_Index.md",
    "Framework/Psychology/realm_data.yaml",
    "Framework/natural_prose.md",
    "Framework/psyche_framework.md",      # stub → Main
    "Framework/Drafting_Workflow.md",     # stub → Main
    "Framework/formatting_rules.md",
    "Framework/Design_QA_Protocol.md",
    "Framework/Drafting_Prompt.md",
    "Framework/Modules.md",
    "Framework/linter.py",
    "Framework/Continuity_Ledger.md",
    "Framework/Character_Change_Log.md",
    "Framework/source_changes.md",
    "Framework/degradation_protocol.md",
    "Characters/_template.md",
    "Characters/_log_template.yaml",
    "Characters/README.md",
    "Characters/Relations.md",
    # Demo cast cards (YAML-only format; optional for novels)
    "Characters/cass.md",
    "Characters/helen.md",
    "Characters/lior.md",
    "Characters/nora.md",
    "Characters/reed.md",
    "Characters/wren.md",
    ".gitignore",
    "README.md",
]

FRAMEWORK_DIRS = [
    "Framework/Mechanics",
    "Framework/Psychology",
    "Framework/Prompts",
    "Simulator",
]

def get_project_root():
    # This script is located in Build/
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_upstream_dir(root):
    parent = os.path.dirname(root)
    return os.path.join(parent, UPSTREAM_NAME)

def merge_gitignore(src, dst):
    if not os.path.exists(dst):
        shutil.copyfile(src, dst)
        print(f"  Pulled (new): .gitignore")
        return
    with open(src, "r", encoding="utf-8") as f:
        src_lines = f.readlines()
    with open(dst, "r", encoding="utf-8") as f:
        dst_lines = f.readlines()
        
    dst_cleaned = [line.strip() for line in dst_lines]
    dst_set = set(line for line in dst_cleaned if line and not line.startswith("#"))
    
    lines_to_add = []
    for line in src_lines:
        cleaned = line.strip()
        if cleaned and not cleaned.startswith("#") and cleaned not in dst_set:
            lines_to_add.append(cleaned)
            
    if lines_to_add:
        with open(dst, "a", encoding="utf-8") as f:
            f.write("\n# Merged from upstream framework\n")
            for line in lines_to_add:
                f.write(f"{line}\n")
        print(f"  Merged upstream rules into: .gitignore")
    else:
        print(f"  Up to date (no rules to merge): .gitignore")

def copy_file(src, dst):
    dst_dir = os.path.dirname(dst)
    os.makedirs(dst_dir, exist_ok=True)
    if os.path.basename(dst) == ".gitignore":
        merge_gitignore(src, dst)
    else:
        shutil.copyfile(src, dst)
        print(f"  Pulled: {os.path.relpath(dst, get_project_root())}")

def copy_directory(src_dir, dst_dir):
    if not os.path.exists(src_dir):
        print(f"  [WARNING] Upstream directory not found: {src_dir}")
        return
    os.makedirs(dst_dir, exist_ok=True)
    for root, dirs, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        target_root = dst_dir if rel_path == '.' else os.path.join(dst_dir, rel_path)
        os.makedirs(target_root, exist_ok=True)
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_root, file)
            shutil.copyfile(src_file, dst_file)
    print(f"  Pulled directory: {os.path.relpath(dst_dir, get_project_root())}")

def update_file_list(root):
    """Automatically rebuild file_list.txt based on tracked files in the repo."""
    print("  Updating file_list.txt...")
    # List files ignoring .git, .venv, etc.
    ignored_prefixes = ['.git', '.venv', '__pycache__', 'Releases', 'Archives', 'scripts']
    files_found = []
    
    for dirpath, dirnames, filenames in os.walk(root):
        # Prune ignored directories in-place to prevent walking into them
        dirnames[:] = [d for d in dirnames if d not in ignored_prefixes and not d.startswith('.')]
        
        for f in filenames:
            # Skip hidden files except .gitignore and .gitkeep
            if f.startswith('.') and f not in ['.gitignore', '.gitkeep']:
                continue
            full_path = os.path.join(dirpath, f)
            rel_path = os.path.relpath(full_path, root)
            # Skip file_list.txt itself
            if rel_path == 'file_list.txt':
                continue
            files_found.append(rel_path)
            
    files_found.sort()
    file_list_path = os.path.join(root, "file_list.txt")
    with open(file_list_path, "w") as out:
        out.write(f"Total files: {len(files_found)}\n")
        for f in files_found:
            out.write(f"{f}\n")
    print(f"  ✓ Updated file_list.txt (Total files: {len(files_found)})")

def main():
    root = get_project_root()
    upstream = get_upstream_dir(root)
    
    print("==================================================")
    print("      Pulling Psyche Matrix Framework from Core   ")
    print("==================================================")
    print(f"Source: {upstream}")
    print(f"Target: {root}\n")
    
    if not os.path.exists(upstream):
        print(f"[-] Error: Upstream framework directory '{UPSTREAM_NAME}' not found at: {upstream}")
        print("Please check that Authors_Framework exists in the same parent directory.")
        sys.exit(1)
        
    # Pull individual files
    for rel_file in FRAMEWORK_FILES:
        src = os.path.join(upstream, rel_file)
        dst = os.path.join(root, rel_file)
        if os.path.exists(src):
            copy_file(src, dst)
        else:
            print(f"  [WARNING] Upstream file not found: {rel_file}")
            
    # Pull directories
    for rel_dir in FRAMEWORK_DIRS:
        src = os.path.join(upstream, rel_dir)
        dst = os.path.join(root, rel_dir)
        copy_directory(src, dst)
        
    # Update file_list.txt to keep tracked files in sync
    update_file_list(root)
    
    print("\n[✓] Framework sync from CognitiveMiddleware completed successfully!")

if __name__ == "__main__":
    main()
