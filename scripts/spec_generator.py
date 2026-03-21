#!/usr/bin/env python3
"""
Spec Generator Tool
Generates spec.md, design.md, and tasks.md from structured input.
"""

import json
import sys
from datetime import datetime
from typing import Dict, List


def generate_spec_md(data: Dict) -> str:
    """Generate spec.md content from structured data."""
    feature = data.get("feature_name", "Feature")
    context = data.get("context", "")
    users = data.get("users", [])
    requirements = data.get("requirements", [])
    acceptance_criteria = data.get("acceptance_criteria", {})
    
    content = f"""# {feature} Specification

## Context

{context}

## Users

"""
    
    for user in users:
        content += f"### {user.get('role', 'User')}\n"
        content += f"{user.get('description', '')}\n\n"
        if user.get('devices'):
            content += f"**Devices**: {user.get('devices')}\n"
        if user.get('location'):
            content += f"**Location**: {user.get('location')}\n"
        content += "\n"
    
    content += "## Requirements\n\n"
    
    for req in requirements:
        content += f"- **{req.get('id', 'R?')}**: {req.get('description', '')}\n"
    
    content += "\n## Acceptance Criteria\n\n"
    
    for req_id, criteria in acceptance_criteria.items():
        content += f"### {req_id}\n\n"
        for i, criterion in enumerate(criteria, 1):
            content += f"- **AC{i}**: {criterion}\n"
        content += "\n"
    
    content += f"\n---\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    return content


def generate_design_md(data: Dict) -> str:
    """Generate design.md content from structured data."""
    feature = data.get("feature_name", "Feature")
    components = data.get("components", [])
    data_flow = data.get("data_flow", "")
    interfaces = data.get("interfaces", [])
    
    content = f"""# {feature} Design

## Components

"""
    
    for comp in components:
        content += f"### {comp.get('name', 'Component')}\n"
        content += f"{comp.get('description', '')}\n\n"
        if comp.get('responsibilities'):
            content += "**Responsibilities**:\n"
            for resp in comp['responsibilities']:
                content += f"- {resp}\n"
            content += "\n"
    
    content += "## Data Flow\n\n"
    content += f"{data_flow}\n\n"
    
    content += "## Interfaces/API\n\n"
    
    for interface in interfaces:
        content += f"### {interface.get('name', 'Interface')}\n"
        content += f"{interface.get('description', '')}\n\n"
        if interface.get('methods'):
            content += "**Methods**:\n"
            for method in interface['methods']:
                content += f"- `{method}`\n"
            content += "\n"
    
    content += f"\n---\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    return content


def generate_tasks_md(data: Dict) -> str:
    """Generate tasks.md content from structured data."""
    feature = data.get("feature_name", "Feature")
    tasks = data.get("tasks", [])
    
    content = f"""# {feature} Tasks

"""
    
    for task in tasks:
        task_id = task.get('id', 'T?')
        description = task.get('description', '')
        status = task.get('status', 'planned')
        done_when = task.get('done_when', '')
        dependencies = task.get('dependencies', [])
        
        content += f"## {task_id}: {description}\n\n"
        content += f"**Status**: {status}\n\n"
        
        if dependencies:
            content += f"**Dependencies**: {', '.join(dependencies)}\n\n"
        
        content += f"**Done When**: {done_when}\n\n"
        content += "---\n\n"
    
    content += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    return content


def generate_from_template(template_type: str, data: Dict) -> str:
    """Generate content based on template type."""
    if template_type == "spec":
        return generate_spec_md(data)
    elif template_type == "design":
        return generate_design_md(data)
    elif template_type == "tasks":
        return generate_tasks_md(data)
    else:
        raise ValueError(f"Unknown template type: {template_type}")


def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: spec_generator.py <template_type> [--data <json_file>]"}))
        sys.exit(1)
    
    template_type = sys.argv[1]
    
    # Read data from stdin or file
    if len(sys.argv) > 3 and sys.argv[2] == "--data":
        with open(sys.argv[3], 'r') as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)
    
    try:
        content = generate_from_template(template_type, data)
        print(content)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
