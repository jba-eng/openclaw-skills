#!/bin/bash
# Autocoder Cron Setup Script
# This script adds the autocoder cron jobs to your system cron

# Configuration
PROJECT_PATH="/path/to/project"  # CHANGE THIS to your project path
SKILL_COMMAND="python -m openclaw.skills.autocoder"

# Validate project path
if [ ! -d "$PROJECT_PATH" ]; then
    echo "Error: Project path does not exist: $PROJECT_PATH"
    echo "Please edit this script and set PROJECT_PATH to your project directory"
    exit 1
fi

# Create temporary cron file
TEMP_CRON=$(mktemp)

# Get current cron jobs
crontab -l > "$TEMP_CRON" 2>/dev/null || true

# Check if autocoder jobs already exist
if grep -q "openclaw.skills.autocoder" "$TEMP_CRON"; then
    echo "Autocoder cron jobs already exist. Skipping..."
    rm "$TEMP_CRON"
    exit 0
fi

# Add autocoder cron jobs (every 15 minutes from 1:00 AM to 4:45 AM)
cat >> "$TEMP_CRON" << 'EOF'

# Autocoder: Overnight task execution (1:00 AM - 4:45 AM, every 15 minutes)
0,15,30,45 1 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 2 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 3 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 4 * * * cd /path/to/project && python -m openclaw.skills.autocoder
EOF

# Replace placeholder with actual project path
sed -i "s|/path/to/project|$PROJECT_PATH|g" "$TEMP_CRON"

# Install new cron jobs
crontab "$TEMP_CRON"

# Clean up
rm "$TEMP_CRON"

echo "✓ Autocoder cron jobs installed successfully"
echo ""
echo "Schedule:"
echo "  - 1:00 AM, 1:15 AM, 1:30 AM, 1:45 AM"
echo "  - 2:00 AM, 2:15 AM, 2:30 AM, 2:45 AM"
echo "  - 3:00 AM, 3:15 AM, 3:30 AM, 3:45 AM"
echo "  - 4:00 AM, 4:15 AM, 4:30 AM, 4:45 AM"
echo ""
echo "Total: 16 runs per night (one task per run)"
echo ""
echo "Verify with: crontab -l"
