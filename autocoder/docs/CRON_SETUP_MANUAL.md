# Manual Cron Setup

If you prefer to set up cron manually instead of using the script:

## Step 1: Open Cron Editor
```bash
crontab -e
```

## Step 2: Add These Lines

Replace `/path/to/project` with your actual project directory:

```bash
# Autocoder: Overnight task execution (1:00 AM - 4:45 AM, every 15 minutes)
0,15,30,45 1 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 2 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 3 * * * cd /path/to/project && python -m openclaw.skills.autocoder
0,15,30,45 4 * * * cd /path/to/project && python -m openclaw.skills.autocoder
```

## Step 3: Save and Exit

- In `nano`: Press `Ctrl+O`, then `Enter`, then `Ctrl+X`
- In `vi`: Press `Esc`, then `:wq`, then `Enter`

## Step 4: Verify

```bash
crontab -l
```

You should see your autocoder jobs listed.

## Cron Schedule Explanation

```
0,15,30,45 1 * * * ...
│          │ │ │ │ │
│          │ │ │ │ └─ Day of week (0-6, 0=Sunday)
│          │ │ │ └─── Month (1-12)
│          │ │ └───── Day of month (1-31)
│          │ └─────── Hour (0-23)
│          └───────── Minute (0-59)
└──────────────────── Run at minutes 0, 15, 30, 45
```

So `0,15,30,45 1 * * *` means:
- Every 15 minutes (0, 15, 30, 45)
- During hour 1 (1:00 AM - 1:59 AM)
- Every day of month
- Every month
- Every day of week

## Example: Full Cron Setup

```bash
# Autocoder: Overnight task execution (1:00 AM - 4:45 AM, every 15 minutes)
0,15,30,45 1 * * * cd /home/user/my-project && python -m openclaw.skills.autocoder
0,15,30,45 2 * * * cd /home/user/my-project && python -m openclaw.skills.autocoder
0,15,30,45 3 * * * cd /home/user/my-project && python -m openclaw.skills.autocoder
0,15,30,45 4 * * * cd /home/user/my-project && python -m openclaw.skills.autocoder
```

## Troubleshooting

### Cron not running?
1. Check if cron daemon is running:
   ```bash
   sudo systemctl status cron
   ```

2. Start cron if not running:
   ```bash
   sudo systemctl start cron
   ```

3. Enable cron to start on boot:
   ```bash
   sudo systemctl enable cron
   ```

### Check cron logs
```bash
# On Linux
sudo tail -f /var/log/syslog | grep CRON

# On macOS
log stream --predicate 'process == "cron"'
```

### Test cron job manually
```bash
cd /path/to/project && python -m openclaw.skills.autocoder
```

### Verify cron is installed
```bash
which cron
crontab -l
```

## Alternative: Using at Command

If you prefer one-time scheduling instead of recurring cron:

```bash
# Schedule for tomorrow at 1:00 AM
echo "cd /path/to/project && python -m openclaw.skills.autocoder" | at 1:00 AM tomorrow
```

But cron is recommended for recurring overnight execution.

## Removing Cron Jobs

To remove autocoder cron jobs:

```bash
crontab -e
```

Delete the 4 autocoder lines, save, and exit.

Or remove all cron jobs:
```bash
crontab -r
```

## Monitoring Cron Execution

Check if cron jobs ran:

```bash
# Check NIGHTLY_LOG.md
tail -f NIGHTLY_LOG.md

# Check RUN_STATE.json
cat RUN_STATE.json

# Check for lock file (should not exist between runs)
ls -la .autocoder.lock
```

## Time Zone

Cron uses the system time zone. To verify:

```bash
date
timedatectl
```

If you need to run at a specific time zone, set TZ in cron:

```bash
TZ=America/New_York 0,15,30,45 1 * * * cd /path/to/project && python -m openclaw.skills.autocoder
```

## Next Steps

1. Set up cron using this guide
2. Create your first spec with spec-creation skill
3. Test manually with spec-coding skill
4. Let cron run overnight
5. Check results in the morning
