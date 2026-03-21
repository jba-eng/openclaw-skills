#!/usr/bin/env python3
"""
Spec Validator Tool
Validates spec.md, design.md, and tasks.md structure and content.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def validate_spec_md(content: str) -> Tuple[bool, List[str]]:
    """Validate spec.md structure and content."""
    issues = []
    
    # Check required sections
    required_sections = ["Context", "Users", "Requirements", "Acceptance Criteria"]
    for section in required_sections:
        if f"## {section}" not in content and f"# {section}" not in content:
            issues.append(f"Missing required section: {section}")
    
    # Extract requirements
    req_pattern = r'-\s*\*?\*?([R]\d+)\*?\*?:'
    requirements = re.findall(req_pattern, content)
    
    if not requirements:
        issues.append("No requirements found (expected format: - **R1**: description)")
    
    # Check acceptance criteria
    ac_section = content.split("## Acceptance Criteria")[-1] if "## Acceptance Criteria" in content else ""
    
    for req_id in requirements:
        if req_id not in ac_section:
            issues.append(f"Requirement {req_id} has no acceptance criteria section")
        else:
            # Count ACs for this requirement
            req_section = ac_section.split(f"### {req_id}")[-1].split("###")[0] if f"### {req_id}" in ac_section else ""
            ac_count = len(re.findall(r'-\s*\*?\*?AC\d+\*?\*?:', req_section))
            
            if ac_count < 2:
                issues.append(f"Requirement {req_id} has only {ac_count} acceptance criteria (expected 2-3)")
            elif ac_count > 3:
                issues.append(f"Requirement {req_id} has {ac_count} acceptance criteria (expected 2-3)")
    
    # Check minimum length
    if len(content) < 500:
        issues.append(f"Spec is too short ({len(content)} chars, expected 500+)")
    
    return len(issues) == 0, issues


def validate_design_md(content: str) -> Tuple[bool, List[str]]:
    """Validate design.md structure."""
    issues = []
    
    # Check required sections
    required_sections = ["Components", "Data Flow", "Interfaces"]
    for section in required_sections:
        if f"## {section}" not in content and f"# {section}" not in content:
            issues.append(f"Missing required section: {section}")
    
    # Check for at least one component
    if "### " not in content.split("## Components")[-1].split("## Data Flow")[0]:
        issues.append("No components defined (expected ### Component Name)")
    
    return len(issues) == 0, issues


def validate_tasks_md(content: str) -> Tuple[bool, List[str]]:
    """Validate tasks.md structure."""
    issues = []
    
    # Extract tasks
    task_pattern = r'##\s+([T]\d+):'
    tasks = re.findall(task_pattern, content)
    
    if not tasks:
        issues.append("No tasks found (expected format: ## T1: description)")
    
    # Check each task has required fields
    for task_id in tasks:
        task_section = content.split(f"## {task_id}:")[-1].split("##")[0]
        
        if "**Status**:" not in task_section:
            issues.append(f"Task {task_id} missing Status field")
        
        if "**Done When**:" not in task_section:
            issues.append(f"Task {task_id} missing Done When field")
    
    return len(issues) == 0, issues


def validate_file(file_path: str) -> Dict:
    """Validate a specification file."""
    path = Path(file_path)
    
    if not path.exists():
        return {
            "valid": False,
            "file": file_path,
            "issues": [f"File not found: {file_path}"]
        }
    
    content = path.read_text()
    file_name = path.stem  # spec, design, tasks, or spec_template, etc.
    
    # Handle template files
    if file_name.endswith("_template"):
        file_type = file_name.replace("_template", "")
    else:
        file_type = file_name
    
    if file_type == "spec":
        valid, issues = validate_spec_md(content)
    elif file_type == "design":
        valid, issues = validate_design_md(content)
    elif file_type == "tasks":
        valid, issues = validate_tasks_md(content)
    else:
        return {
            "valid": False,
            "file": file_path,
            "issues": [f"Unknown file type: {file_type}. Expected: spec, design, or tasks"]
        }
    
    return {
        "valid": valid,
        "file": file_path,
        "issues": issues,
        "line_count": len(content.split('\n')),
        "char_count": len(content)
    }


def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: spec_validator.py <file_path> [file_path2 ...]"}))
        sys.exit(1)
    
    results = []
    all_valid = True
    
    for file_path in sys.argv[1:]:
        result = validate_file(file_path)
        results.append(result)
        if not result["valid"]:
            all_valid = False
    
    output = {
        "all_valid": all_valid,
        "results": results,
        "summary": {
            "total": len(results),
            "valid": sum(1 for r in results if r["valid"]),
            "invalid": sum(1 for r in results if not r["valid"])
        }
    }
    
    print(json.dumps(output, indent=2))
    
    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
