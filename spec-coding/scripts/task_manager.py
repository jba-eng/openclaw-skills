#!/usr/bin/env python3
"""
Task Manager Tool for Spec Coding
Manages task state, finds next tasks, and updates status.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def parse_tasks(content: str) -> List[Dict]:
    """Parse tasks from tasks.md content with flexible regex."""
    tasks = []
    
    # Match task headers: ## T1: Description or ### T1: Description (flexible whitespace)
    task_pattern = r'#{2,3}\s+(T\d+)\s*:\s*(.+?)(?:\n|$)'
    task_matches = list(re.finditer(task_pattern, content))
    
    for i, match in enumerate(task_matches):
        task_id = match.group(1)
        description = match.group(2).strip()
        
        # Extract the section for this task
        start_pos = match.end()
        end_pos = task_matches[i + 1].start() if i + 1 < len(task_matches) else len(content)
        task_section = content[start_pos:end_pos]
        
        # Extract status (flexible whitespace and optional bold markers)
        status_match = re.search(r'\*{0,2}\s*Status\s*\*{0,2}\s*:\s*(\w+)', task_section, re.IGNORECASE)
        status = status_match.group(1) if status_match else 'unknown'
        
        # Extract done_when (flexible whitespace)
        done_when_match = re.search(r'\*{0,2}\s*Done\s+When\s*\*{0,2}\s*:\s*(.+?)(?:\n\n|\*\*|---|\Z)', task_section, re.DOTALL | re.IGNORECASE)
        done_when = done_when_match.group(1).strip() if done_when_match else ''
        
        # Extract dependencies (flexible whitespace)
        deps_match = re.search(r'\*{0,2}\s*Dependencies\s*\*{0,2}\s*:\s*(.+?)(?:\n|$)', task_section, re.IGNORECASE)
        dependencies = []
        if deps_match:
            deps_str = deps_match.group(1).strip()
            if deps_str and deps_str.lower() != 'none':
                dependencies = [d.strip() for d in re.split(r'[,\s]+', deps_str) if d.strip()]
        
        tasks.append({
            'id': task_id,
            'description': description,
            'status': status,
            'done_when': done_when,
            'dependencies': dependencies
        })
    
    return tasks


def find_next_task(tasks: List[Dict]) -> Optional[Dict]:
    """Find the first task with status 'planned'."""
    for task in tasks:
        if task['status'] == 'planned':
            return task
    return None


def find_in_progress_task(tasks: List[Dict]) -> Optional[Dict]:
    """Find task with status 'in_progress'."""
    for task in tasks:
        if task['status'] in ['in_progress', 'in-progress']:
            return task
    return None


def get_task_stats(tasks: List[Dict]) -> Dict:
    """Get statistics about tasks."""
    stats = {
        'total': len(tasks),
        'planned': 0,
        'in_progress': 0,
        'done': 0,
        'blocked': 0,
        'deferred': 0
    }
    
    for task in tasks:
        status = task['status'].lower().replace('-', '_')
        if status in stats:
            stats[status] += 1
    
    return stats


def update_task_status(content: str, task_id: str, new_status: str) -> Tuple[str, bool]:
    """Update task status in tasks.md content with flexible regex."""
    # Normalize line endings first
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Find the task section (supports ## or ###, flexible whitespace)
    # Match status pattern: **Status:** value or Status: value
    task_pattern = rf'(#{2,3}\s+{re.escape(task_id)}\s*:.*?)(\*{{0,2}}\s*Status\s*\*{{0,2}}\s*:\s*)(\w+)(\s*)'
    
    match = re.search(task_pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        return content, False
    
    # Preserve the original formatting of the Status label
    original_label = match.group(2)
    
    # Replace the status (keep the trailing spaces)
    updated = re.sub(
        task_pattern,
        rf'\1{re.escape(original_label)}{new_status}\4',
        content,
        count=1,
        flags=re.DOTALL | re.IGNORECASE
    )
    
    return updated, True


def auto_complete_task(tasks_file_path: str, task_id: str) -> Tuple[bool, str]:
    """
    Automatically mark task as DONE after validation.
    
    Args:
        tasks_file_path: Path to tasks.md
        task_id: Task ID to mark complete
        
    Returns:
        Tuple of (success, message)
    """
    try:
        tasks_file = Path(tasks_file_path)
        if not tasks_file.exists():
            return False, f"File not found: {tasks_file_path}"
        
        content = tasks_file.read_text()
        updated_content, success = update_task_status(content, task_id, "done")
        
        if success:
            # Write the updated content
            tasks_file.write_text(updated_content)
            return True, f"Task {task_id} marked as DONE"
        else:
            return False, f"Task {task_id} not found"
    
    except Exception as e:
        return False, f"Error: {str(e)}"


def discover_project(project_name: str, base_path: str = None) -> Dict:
    """Discover project and verify spec files exist."""
    if base_path is None:
        # Try multiple possible project base paths
        possible_bases = [
            Path.home() / ".openclaw" / "workspace" / "software-projects",
            Path("software-projects"),
            Path.cwd() / "software-projects"
        ]
        
        base = None
        for possible_base in possible_bases:
            if possible_base.exists():
                base = possible_base
                break
        
        if base is None:
            base = possible_bases[0]
    else:
        base = Path(base_path)
    
    if not base.exists():
        return {"error": f"Base path not found: {base}"}
    
    # Find project
    projects = [d.name for d in base.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    if project_name in projects:
        project_path = base / project_name
    else:
        # Fuzzy match
        matches = [p for p in projects if project_name.lower() in p.lower()]
        if len(matches) == 1:
            project_path = base / matches[0]
        elif len(matches) > 1:
            return {
                "error": "Multiple matches found",
                "alternatives": matches
            }
        else:
            return {
                "error": "Project not found",
                "available": projects[:5]
            }
    
    # Check for spec files in both root and .specifications/
    spec_dir = project_path / ".specifications"
    required_files = ["spec.md", "specs.md", "design.md", "tasks.md"]
    
    result = {
        "project": project_path.name,
        "project_path": str(project_path),
        "spec_dir_exists": spec_dir.exists(),
        "files": {}
    }
    
    # Check root directory first
    for file in required_files:
        root_file = project_path / file
        spec_dir_file = spec_dir / file if spec_dir.exists() else None
        
        result["files"][file] = {
            "root": root_file.exists(),
            "spec_dir": spec_dir_file.exists() if spec_dir.exists() else False,
            "path": str(root_file) if root_file.exists() else (str(spec_dir_file) if spec_dir.exists() and spec_dir_file.exists() else None)
        }
    
    # Determine if ready (need at least one spec file, design.md, and tasks.md)
    has_spec = result["files"]["spec.md"]["root"] or result["files"]["spec.md"]["spec_dir"] or result["files"]["specs.md"]["root"] or result["files"]["specs.md"]["spec_dir"]
    has_design = result["files"]["design.md"]["root"] or result["files"]["design.md"]["spec_dir"]
    has_tasks = result["files"]["tasks.md"]["root"] or result["files"]["tasks.md"]["spec_dir"]
    
    result["ready"] = has_spec and has_design and has_tasks
    
    return result


def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: task_manager.py <command> [args]"}))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "discover":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: task_manager.py discover <project_name>"}))
            sys.exit(1)
        
        project_name = sys.argv[2]
        result = discover_project(project_name)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result.get("ready", False) else 1)
    
    elif command == "status":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: task_manager.py status <tasks_file>"}))
            sys.exit(1)
        
        tasks_file = Path(sys.argv[2])
        if not tasks_file.exists():
            print(json.dumps({"error": f"File not found: {tasks_file}"}))
            sys.exit(1)
        
        content = tasks_file.read_text()
        tasks = parse_tasks(content)
        stats = get_task_stats(tasks)
        next_task = find_next_task(tasks)
        in_progress = find_in_progress_task(tasks)
        
        result = {
            "stats": stats,
            "next_task": next_task,
            "in_progress_task": in_progress,
            "all_tasks": tasks
        }
        
        print(json.dumps(result, indent=2))
    
    elif command == "next":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: task_manager.py next <tasks_file>"}))
            sys.exit(1)
        
        tasks_file = Path(sys.argv[2])
        if not tasks_file.exists():
            print(json.dumps({"error": f"File not found: {tasks_file}"}))
            sys.exit(1)
        
        content = tasks_file.read_text()
        tasks = parse_tasks(content)
        next_task = find_next_task(tasks)
        
        if next_task:
            print(json.dumps(next_task, indent=2))
        else:
            print(json.dumps({"message": "No planned tasks remaining"}))
            sys.exit(1)
    
    elif command == "update":
        if len(sys.argv) < 5:
            print(json.dumps({"error": "Usage: task_manager.py update <tasks_file> <task_id> <new_status>"}))
            sys.exit(1)
        
        tasks_file = Path(sys.argv[2])
        task_id = sys.argv[3]
        new_status = sys.argv[4]
        
        if not tasks_file.exists():
            print(json.dumps({"error": f"File not found: {tasks_file}"}))
            sys.exit(1)
        
        content = tasks_file.read_text()
        updated_content, success = update_task_status(content, task_id, new_status)
        
        if success:
            # Don't write, just return the updated content
            print(json.dumps({
                "success": True,
                "task_id": task_id,
                "new_status": new_status,
                "updated_content": updated_content
            }))
        else:
            print(json.dumps({
                "success": False,
                "error": f"Task {task_id} not found"
            }))
            sys.exit(1)
    
    elif command == "auto_complete":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "Usage: task_manager.py auto_complete <tasks_file> <task_id>"}))
            sys.exit(1)
        
        tasks_file_path = sys.argv[2]
        task_id = sys.argv[3]
        
        success, message = auto_complete_task(tasks_file_path, task_id)
        
        if success:
            print(json.dumps({
                "success": True,
                "message": message
            }))
        else:
            print(json.dumps({
                "success": False,
                "error": message
            }))
            sys.exit(1)
    
    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
