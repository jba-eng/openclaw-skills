#!/usr/bin/env python3
"""
Project Discovery Tool for Spec Creation
Finds projects and existing specification files efficiently.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional


def find_projects(base_path: str = "/home/jonathan/.openclaw/workspace/software-projects") -> List[str]:
    """List all project directories."""
    try:
        base = Path(base_path)
        if not base.exists():
            return []
        return sorted([d.name for d in base.iterdir() if d.is_dir() and not d.name.startswith('.')])
    except Exception as e:
        return []


def find_project_match(project_name: str, base_path: str = "/home/jonathan/.openclaw/workspace/software-projects") -> Optional[Dict]:
    """Find exact or fuzzy match for project name."""
    projects = find_projects(base_path)
    
    # Exact match
    if project_name in projects:
        return {"match_type": "exact", "project": project_name, "alternatives": []}
    
    # Fuzzy match (contains)
    matches = [p for p in projects if project_name.lower() in p.lower()]
    if len(matches) == 1:
        return {"match_type": "fuzzy_single", "project": matches[0], "alternatives": []}
    elif len(matches) > 1:
        return {"match_type": "fuzzy_multiple", "project": None, "alternatives": matches}
    
    return {"match_type": "none", "project": None, "alternatives": projects[:5]}


def check_existing_specs(project_path: str) -> Dict:
    """Check for existing specification files in project."""
    spec_dir = Path(project_path) / ".specifications"
    
    result = {
        "spec_dir_exists": spec_dir.exists(),
        "files": {
            "spec.md": False,
            "design.md": False,
            "tasks.md": False
        },
        "other_files": []
    }
    
    if spec_dir.exists():
        for file in spec_dir.iterdir():
            if file.is_file():
                if file.name in result["files"]:
                    result["files"][file.name] = True
                else:
                    result["other_files"].append(file.name)
    
    return result


def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: project_discovery.py <command> [args]"}))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        projects = find_projects()
        print(json.dumps({"projects": projects, "count": len(projects)}))
    
    elif command == "find":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: project_discovery.py find <project_name>"}))
            sys.exit(1)
        
        project_name = sys.argv[2]
        result = find_project_match(project_name)
        print(json.dumps(result))
    
    elif command == "check":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: project_discovery.py check <project_path>"}))
            sys.exit(1)
        
        project_path = sys.argv[2]
        result = check_existing_specs(project_path)
        print(json.dumps(result))
    
    elif command == "full":
        # Full discovery: list projects and check for a specific one
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: project_discovery.py full <project_name>"}))
            sys.exit(1)
        
        project_name = sys.argv[2]
        base_path = "/home/jonathan/.openclaw/workspace/software-projects"
        
        match_result = find_project_match(project_name, base_path)
        
        if match_result["project"]:
            project_path = os.path.join(base_path, match_result["project"])
            spec_result = check_existing_specs(project_path)
            
            print(json.dumps({
                "match": match_result,
                "project_path": project_path,
                "specs": spec_result
            }))
        else:
            print(json.dumps({
                "match": match_result,
                "project_path": None,
                "specs": None
            }))
    
    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
