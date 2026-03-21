#!/usr/bin/env python3
"""
Spec Diff Tool
Compares specification files and generates human-readable diffs.
"""

import json
import sys
from difflib import unified_diff
from pathlib import Path
from typing import Dict, List


def generate_diff(old_content: str, new_content: str, filename: str) -> List[str]:
    """Generate unified diff between two contents."""
    old_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)
    
    diff = list(unified_diff(
        old_lines,
        new_lines,
        fromfile=f"{filename} (old)",
        tofile=f"{filename} (new)",
        lineterm=''
    ))
    
    return diff


def analyze_diff(diff_lines: List[str]) -> Dict:
    """Analyze diff to extract statistics."""
    additions = sum(1 for line in diff_lines if line.startswith('+') and not line.startswith('+++'))
    deletions = sum(1 for line in diff_lines if line.startswith('-') and not line.startswith('---'))
    
    # Extract changed sections
    sections_changed = []
    for line in diff_lines:
        if line.startswith('@@'):
            sections_changed.append(line)
    
    return {
        "additions": additions,
        "deletions": deletions,
        "total_changes": additions + deletions,
        "sections_changed": len(sections_changed)
    }


def compare_files(old_path: str, new_path: str) -> Dict:
    """Compare two specification files."""
    old_file = Path(old_path)
    new_file = Path(new_path)
    
    if not old_file.exists():
        return {
            "error": f"Old file not found: {old_path}",
            "has_changes": False
        }
    
    if not new_file.exists():
        return {
            "error": f"New file not found: {new_path}",
            "has_changes": False
        }
    
    old_content = old_file.read_text()
    new_content = new_file.read_text()
    
    if old_content == new_content:
        return {
            "has_changes": False,
            "message": "Files are identical"
        }
    
    diff_lines = generate_diff(old_content, new_content, old_file.name)
    stats = analyze_diff(diff_lines)
    
    return {
        "has_changes": True,
        "old_file": old_path,
        "new_file": new_path,
        "stats": stats,
        "diff": diff_lines
    }


def compare_content(old_content: str, new_content: str, label: str = "content") -> Dict:
    """Compare two content strings."""
    if old_content == new_content:
        return {
            "has_changes": False,
            "message": "Content is identical"
        }
    
    diff_lines = generate_diff(old_content, new_content, label)
    stats = analyze_diff(diff_lines)
    
    return {
        "has_changes": True,
        "stats": stats,
        "diff": diff_lines
    }


def main():
    """Main CLI interface."""
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: spec_diff.py <old_file> <new_file> [--format json|text]"}))
        sys.exit(1)
    
    old_path = sys.argv[1]
    new_path = sys.argv[2]
    output_format = "text"
    
    if len(sys.argv) > 4 and sys.argv[3] == "--format":
        output_format = sys.argv[4]
    
    result = compare_files(old_path, new_path)
    
    if output_format == "json":
        # Convert diff lines to strings for JSON
        if "diff" in result:
            result["diff"] = [line.rstrip() for line in result["diff"]]
        print(json.dumps(result, indent=2))
    else:
        # Human-readable text output
        if "error" in result:
            print(f"Error: {result['error']}")
            sys.exit(1)
        
        if not result["has_changes"]:
            print(result["message"])
        else:
            print(f"\nComparing: {result['old_file']} → {result['new_file']}\n")
            print(f"Changes: +{result['stats']['additions']} -{result['stats']['deletions']}")
            print(f"Sections changed: {result['stats']['sections_changed']}\n")
            print("=" * 80)
            for line in result["diff"]:
                print(line.rstrip())
    
    sys.exit(0 if not result.get("has_changes", False) else 1)


if __name__ == "__main__":
    main()
