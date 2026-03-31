#!/usr/bin/env python3
"""
Task Validator Tool for Spec Coding
Validates done_when conditions for tasks.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def parse_task(content: str, task_id: str) -> Dict:
    """Parse a specific task from tasks.md with flexible regex."""
    # Find task section (flexible whitespace, supports ## or ###)
    task_pattern = rf'#{2,3}\s+{re.escape(task_id)}\s*:\s*(.+?)(?:\n|$)'
    match = re.search(task_pattern, content)
    
    if not match:
        return None
    
    description = match.group(1).strip()
    
    # Find the section boundaries
    start_pos = match.end()
    next_task = re.search(r'#{2,3}\s+T\d+\s*:', content[start_pos:])
    end_pos = start_pos + next_task.start() if next_task else len(content)
    task_section = content[start_pos:end_pos]
    
    # Extract status (flexible whitespace and optional bold markers)
    status_match = re.search(r'\*{0,2}\s*Status\s*\*{0,2}\s*:\s*(\w+)', task_section, re.IGNORECASE)
    status = status_match.group(1) if status_match else 'unknown'
    
    # Extract done_when (flexible whitespace)
    done_when_match = re.search(r'\*{0,2}\s*Done\s+When\s*\*{0,2}\s*:\s*(.+?)(?:\n\n|\*\*|---|\Z)', task_section, re.DOTALL | re.IGNORECASE)
    done_when_text = done_when_match.group(1).strip() if done_when_match else ''
    
    # Parse done_when conditions (bullet points or numbered list)
    conditions = []
    for line in done_when_text.split('\n'):
        line = line.strip()
        # Match bullet points or numbered items (flexible whitespace)
        if re.match(r'^[-*•]\s+', line) or re.match(r'^\d+\.\s+', line):
            condition = re.sub(r'^[-*•]\s+', '', line)
            condition = re.sub(r'^\d+\.\s+', '', condition)
            if condition:
                conditions.append(condition.strip())
        elif line and not line.startswith('**') and not line.startswith('*'):
            # Single line condition
            conditions.append(line)
    
    return {
        'id': task_id,
        'description': description,
        'status': status,
        'done_when': conditions
    }


def validate_conditions(conditions: List[str], context: Dict = None) -> List[Dict]:
    """
    Validate done_when conditions.
    Returns list of condition results with status.
    
    Note: This is a template validator. Actual validation requires
    running tests, checking API responses, etc.
    """
    results = []
    
    for i, condition in enumerate(conditions, 1):
        # Check if condition is well-formed
        is_testable = any([
            'test' in condition.lower(),
            'return' in condition.lower(),
            'response' in condition.lower(),
            'file' in condition.lower(),
            'exist' in condition.lower(),
            'pass' in condition.lower(),
            'complete' in condition.lower(),
            'implement' in condition.lower()
        ])
        
        results.append({
            'index': i,
            'condition': condition,
            'testable': is_testable,
            'status': 'pending',  # Agent must manually verify
            'note': 'Manual verification required'
        })
    
    return results


def check_task_readiness(task: Dict) -> Tuple[bool, List[str]]:
    """Check if task is ready for execution."""
    issues = []
    
    if not task:
        return False, ["Task not found"]
    
    if not task.get('done_when'):
        issues.append("No done_when conditions defined")
    
    if task['status'] not in ['planned', 'in_progress', 'in-progress']:
        issues.append(f"Task status is '{task['status']}', expected 'planned' or 'in_progress'")
    
    return len(issues) == 0, issues


def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: task_validator.py <command> [args]"}))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "Usage: task_validator.py check <tasks_file> <task_id>"}))
            sys.exit(1)
        
        tasks_file = Path(sys.argv[2])
        task_id = sys.argv[3]
        
        if not tasks_file.exists():
            print(json.dumps({"error": f"File not found: {tasks_file}"}))
            sys.exit(1)
        
        content = tasks_file.read_text()
        task = parse_task(content, task_id)
        
        if not task:
            print(json.dumps({"error": f"Task {task_id} not found"}))
            sys.exit(1)
        
        ready, issues = check_task_readiness(task)
        condition_results = validate_conditions(task['done_when'])
        
        result = {
            "task": task,
            "ready": ready,
            "issues": issues,
            "conditions": condition_results,
            "total_conditions": len(condition_results),
            "note": "Agent must manually verify each condition"
        }
        
        print(json.dumps(result, indent=2))
        sys.exit(0 if ready else 1)
    
    elif command == "list":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: task_validator.py list <tasks_file>"}))
            sys.exit(1)
        
        tasks_file = Path(sys.argv[2])
        
        if not tasks_file.exists():
            print(json.dumps({"error": f"File not found: {tasks_file}"}))
            sys.exit(1)
        
        content = tasks_file.read_text()
        
        # Find all task IDs (flexible whitespace)
        task_ids = re.findall(r'#{2,3}\s+(T\d+)\s*:', content)
        
        all_tasks = []
        for task_id in task_ids:
            task = parse_task(content, task_id)
            if task:
                ready, issues = check_task_readiness(task)
                all_tasks.append({
                    "id": task['id'],
                    "description": task['description'],
                    "status": task['status'],
                    "conditions_count": len(task['done_when']),
                    "ready": ready
                })
        
        print(json.dumps({"tasks": all_tasks, "total": len(all_tasks)}, indent=2))
    
    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
