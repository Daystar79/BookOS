#!/usr/bin/env python3
"""
Psyche Matrix Framework Linter
------------------------------
Scans drafted prose files or directories for system leaks, psychological jargon,
banned dialogue markers, and repetitive filler phrases.
"""

import os
import re
import sys
import argparse

# Define regex patterns for system leaks and psychological jargon
SYSTEM_LEAKS = {
    "Framework Jargon": [
        (r"\bRealm (I|II|III|IV|V|VI|VII|VIII|IX|X|\d+)\b", "Realm [N] references on-page"),
        (r"\bFocus Lock\b", "Focus Lock status leak"),
        (r"\bBias State\b", "Bias State status leak"),
        (r"\btransformation_weights\b", "transformation_weights leak"),
        (r"\btransformation_history\b", "transformation_history leak"),
        (r"\bPrism Distortion\b", "Prism Distortion engine reference"),
        (r"\bGreat Wheel\b", "Great Wheel reference"),
    ],
    "Psychological Labels (Therapy Speak)": [
        (r"\b(trauma|reframe|coping mechanism|wound|trigger)\b", "Psychological/therapy labels (show body instead)"),
    ],
    "Engine Bias Names": [
        (r"\bDebt Ledger\b", "Debt Ledger bias name leak"),
        (r"\bSaviour Complex\b", "Saviour Complex bias name leak"),
        (r"\bSystem Architect\b", "System Architect bias name leak"),
        (r"\bMirror\b", "Mirror bias name leak"),
        (r"\bInsulation\b", "Insulation bias name leak"),
        (r"\bDissolution\b", "Dissolution bias name leak"),
    ],
    "Out-of-Character Lookup / Temporal Leaks": [
        (r"\b(look up|database|search the web|search web|as an AI|my database|retriev\w+ records|external search)\b", "Out-of-character AI lookup / temporal leak"),
    ],
    "AI Safety / Preachy Tone Leaks": [
        (r"\b(it'?s important to remember|to be fair|let'?s look at this|while that is a common|actually, from a|safety guidelines?|safety protocols?|respectful conversation|inappropriate content|moral perspective|ethical considerations?|cannot fulfill this request)\b", "AI safety tone / preachiness / correction leak"),
    ],
}

# Define regex patterns for banned dialogue tags and filler phrases
BANNED_PHRASES = {
    "Dialogue Tags & Markers": [
        (r"\bwhispered\b", "Banned dialogue tag 'whispered'"),
        (r"\bAre you okay\??", "Banned dialogue filler 'Are you okay?'"),
        (r"\bI understand how you feel\b", "Banned dialogue filler 'I understand how you feel'"),
        (r"\bsaid quietly\b", "Banned dialogue marker 'said quietly'"),
        (r"\bsaid gently\b", "Banned dialogue marker 'said gently'"),
    ],
    "Filler Phrases (Watchlist)": [
        (r"\blooked at\b", "Repetitive filler 'looked at'"),
        (r"\bfor a moment\b", "Repetitive filler 'for a moment'"),
        (r"\ba long moment\b", "Repetitive filler 'a long moment'"),
        (r"\bgenuinely\b", "Repetitive filler 'genuinely'"),
    ],
}

# Continuous action separators rule
ACTION_SEPARATORS = r"^---$"

def audit_file(filepath):
    """Audits a single file and returns a list of findings."""
    findings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return [{"line": 0, "type": "Error", "message": f"Could not read file: {e}"}]
        
    hr_count = 0
    in_yaml = False
    
    for line_idx, line in enumerate(lines, start=1):
        # Handle YAML frontmatter (skip checking leaks/fillers in headers)
        if line.strip() == "---":
            hr_count += 1
            if line_idx == 1:
                in_yaml = True
                continue
            elif in_yaml:
                in_yaml = False
                continue
                
        if in_yaml:
            continue
            
        # 1. Audit System Leaks
        for category, patterns in SYSTEM_LEAKS.items():
            for pattern, desc in patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    findings.append({
                        "line": line_idx,
                        "type": "System Leak",
                        "category": category,
                        "match": match.group(0),
                        "message": desc
                    })
                    
        # 2. Audit Banned Phrases
        for category, patterns in BANNED_PHRASES.items():
            for pattern, desc in patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    findings.append({
                        "line": line_idx,
                        "type": "Banned/Filler Phrase",
                        "category": category,
                        "match": match.group(0),
                        "message": desc
                    })
                    
    # 3. Check for excess horizontal rules (excluding frontmatter)
    # If there are multiple '---' outside frontmatter, warn about continuous action breaks
    actual_hr_count = hr_count
    if lines and lines[0].strip() == "---":
        # Subtract the frontmatter block start/end
        actual_hr_count = max(0, hr_count - 2)
        
    if actual_hr_count > 2:
        findings.append({
            "line": 0,
            "type": "Formatting Violation",
            "category": "Continuous Action Break",
            "match": "---",
            "message": f"Found {actual_hr_count} horizontal rules. Rules must never separate continuous real-time action (use standard paragraph breaks instead)."
        })
        
    return findings

def audit_directory(path, extensions=None):
    """Recursively audits a directory for matching file extensions."""
    if extensions is None:
        extensions = [".md", ".txt"]
        
    results = {}
    for root, _, files in os.walk(path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                # Ignore system logs, templates, framework configs, and character cards
                rel_root = os.path.relpath(root, path)
                root_parts = rel_root.split(os.path.sep)
                if any(ignored in root_parts for ignored in [".system_generated", "__pycache__", "Characters", "Framework", "RolePlaying"]) or file.startswith("_template"):
                    continue
                filepath = os.path.join(root, file)
                findings = audit_file(filepath)
                if findings:
                    results[filepath] = findings
    return results

def main():
    parser = argparse.ArgumentParser(description="Psyche Matrix Prose Linter")
    parser.add_argument("target", help="File or directory path to audit")
    parser.add_argument("--ext", help="File extensions to scan (comma-separated, default: .md,.txt)", default=".md,.txt")
    
    args = parser.parse_args()
    
    target_path = os.path.abspath(args.target)
    if not os.path.exists(target_path):
        print(f"Error: Target path does not exist: {target_path}")
        sys.exit(1)
        
    extensions = [ext.strip() if ext.startswith('.') else f".{ext.strip()}" for ext in args.ext.split(',')]
    
    print("==================================================")
    print("      Psyche Matrix Framework Prose Linter        ")
    print("==================================================")
    print(f"Scanning target: {target_path}")
    print(f"Extensions: {', '.join(extensions)}")
    print("--------------------------------------------------")
    
    total_findings = 0
    file_count = 0
    has_critical = False
    
    if os.path.isdir(target_path):
        results = audit_directory(target_path, extensions)
        file_count = len(results)
        for filepath, findings in results.items():
            rel_path = os.path.relpath(filepath, target_path)
            print(f"\n[!] File: {rel_path} ({len(findings)} findings)")
            for f in findings:
                total_findings += 1
                line_str = f"Line {f['line']}" if f['line'] > 0 else "File-level"
                print(f"    - {line_str} | [{f['type']}] ({f['category']}): Found '{f['match']}' -> {f['message']}")
                if f['type'] == "System Leak":
                    has_critical = True
    else:
        file_count = 1
        findings = audit_file(target_path)
        if findings:
            print(f"\n[!] File: {os.path.basename(target_path)} ({len(findings)} findings)")
            for f in findings:
                total_findings += 1
                line_str = f"Line {f['line']}" if f['line'] > 0 else "File-level"
                print(f"    - {line_str} | [{f['type']}] ({f['category']}): Found '{f['match']}' -> {f['message']}")
                if f['type'] == "System Leak":
                    has_critical = True
                    
    print("\n--------------------------------------------------")
    print(f"Scan complete. Audited {file_count} file(s) with {total_findings} total finding(s).")
    
    if total_findings > 0:
        if has_critical:
            print("[STATUS] FAIL: Critical system leaks detected. Cleanup required before saving.")
            sys.exit(1)
        else:
            print("[STATUS] WARNING: Non-critical filler/banned phrases detected.")
            sys.exit(0)
    else:
        print("[STATUS] PASS: Prose is clean and compliant with framework standards.")
        sys.exit(0)

if __name__ == "__main__":
    main()
