#!/usr/bin/env python3
"""
Nightly Heartbeat Writer for Coding Agent
Runs once per night via cron. Checks active projects and writes coding-agent's HEARTBEAT.md.
"""

import json
from pathlib import Path
from datetime import datetime

# Paths
# Script is at: .openclaw/workspace/skills/autocoder/scripts/nightly_heartbeat_writer.py
# We need to go up to .openclaw root
SCRIPT_DIR = Path(__file__).parent.resolve()  # scripts/
AUTOCODER_DIR = SCRIPT_DIR.parent  # autocoder/
SKILLS_DIR = AUTOCODER_DIR.parent  # skills/
WORKSPACE_DIR = SKILLS_DIR.parent  # workspace/
OPENCLAW_ROOT = WORKSPACE_DIR.parent  # .openclaw/

ACTIVE_PROJECTS_FILE = WORKSPACE_DIR / "skills" / "active-projects" / "active_projects.json"
CODING_AGENT_HEARTBEAT = WORKSPACE_DIR / "subagents" / "coding-agent" / "HEARTBEAT.md"
SOFTWARE_PROJECTS_DIR = WORKSPACE_DIR / "software-projects"

def get_active_projects():
    """Read active projects from active-projects skill."""
    if not ACTIVE_PROJECTS_FILE.exists():
        print(f"❌ Active projects file not found: {ACTIVE_PROJECTS_FILE}")
        return []
    
    try:
        data = json.loads(ACTIVE_PROJECTS_FILE.read_text())
        return data.get("active_projects", [])
    except Exception as e:
        print(f"❌ Error reading active projects: {e}")
        return []

def check_project_has_pending_tasks(project_name):
    """Check if project has pending tasks in tasks.md."""
    tasks_file = SOFTWARE_PROJECTS_DIR / project_name / "tasks.md"
    
    if not tasks_file.exists():
        return False
    
    try:
        content = tasks_file.read_text()
        # Look for planned, in-progress, or failed tasks
        return any(status in content for status in [
            "**Status:** planned",
            "**Status:** in-progress", 
            "**Status:** failed"
        ])
    except Exception as e:
        print(f"❌ Error reading {project_name}/tasks.md: {e}")
        return False

def write_heartbeat(projects_with_work):
    """Write HEARTBEAT.md for coding-agent."""
    timestamp = datetime.now().isoformat()
    
    if not projects_with_work:
        content = f"""# HEARTBEAT.md

No active coding tasks.

Reply: HEARTBEAT_OK

---
{timestamp}
"""
    else:
        project_list = ", ".join(projects_with_work)
        content = f"""# HEARTBEAT.md

Active projects: {project_list}

Use spec-coding skill to execute ONE task from ONE project.

If no pending tasks, reply: HEARTBEAT_OK

---
{timestamp}
"""
    
    CODING_AGENT_HEARTBEAT.write_text(content)
    print(f"✓ Wrote HEARTBEAT.md for coding-agent")
    print(f"  Projects with work: {len(projects_with_work)}")
    if projects_with_work:
        for p in projects_with_work:
            print(f"    - {p}")

def main():
    """Main execution."""
    print("=" * 60)
    print("Nightly Heartbeat Writer")
    print("=" * 60)
    
    # Get active projects
    active_projects = get_active_projects()
    print(f"\n📋 Active projects: {len(active_projects)}")
    
    if not active_projects:
        print("   No active projects found")
        write_heartbeat([])
        return
    
    # Check each project for pending work
    projects_with_work = []
    for project in active_projects:
        print(f"\n🔍 Checking {project}...")
        
        project_dir = SOFTWARE_PROJECTS_DIR / project
        if not project_dir.exists():
            print(f"   ⚠️  Project directory not found: {project_dir}")
            continue
        
        if check_project_has_pending_tasks(project):
            print(f"   ✓ Has pending tasks")
            projects_with_work.append(project)
        else:
            print(f"   ○ No pending tasks")
    
    # Write heartbeat
    print(f"\n📝 Writing HEARTBEAT.md...")
    write_heartbeat(projects_with_work)
    
    print("\n" + "=" * 60)
    print("✓ Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
