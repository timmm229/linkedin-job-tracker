# Email Scheduler Setup - Get Spreadsheet 4 Times Daily

## What This Does

Automatically checks for new LinkedIn jobs and emails you the spreadsheet at:
- **9:00 AM CST**
- **12:00 PM CST**
- **3:00 PM CST**
- **6:00 PM CST**

Each run will:
1. Check your email for new LinkedIn job alerts
2. Update the Excel spreadsheet with any new jobs
3. Email you the updated spreadsheet

## Prerequisites

You need:
1. ✅ Python installed (you already have this!)
2. ✅ Packages installed (you already did this!)
3. LinkedIn job alerts set up
4. Email app password

## Setup Instructions

### Step 1: Install Additional Package

```cmd
python -m pip install pytz
```

This is needed for Central Time Zone handling.

### Step 2: Set Environment Variables

In Command Prompt, set these **every time** before running, OR set them permanently (see below):

```cmd
set EMAIL_ADDRESS=your_email@gmail.com
set EMAIL_PASSWORD=your_16_char_app_password
set IMAP_SERVER=imap.gmail.com
set RECIPIENT_EMAIL=your_email@gmail.com
```

**Note:** `RECIPIENT_EMAIL` is where the spreadsheet gets sent. If not set, it sends to your `EMAIL_ADDRESS`.

### Step 3: Run the Scheduler

```cmd
cd C:\Users\timma\OneDrive\Desktop\emailcmds\files
python multi_time_scheduler.py
```

**Keep this window open!** The scheduler runs continuously.

---

## Setting Environment Variables PERMANENTLY (Recommended)

So you don't have to set them every time:

### Windows 10/11:

1. Press `Windows + R`
2. Type `sysdm.cpl` and press Enter
3. Click **"Advanced"** tab
4. Click **"Environment Variables"**
5. Under **"User variables"**, click **"New"**
6. Add each variable:
   - Variable name: `EMAIL_ADDRESS`
   - Variable value: `your_email@gmail.com`
7. Repeat for:
   - `EMAIL_PASSWORD`
   - `IMAP_SERVER`
   - `RECIPIENT_EMAIL`
8. Click **OK** on all windows
9. **Close and reopen Command Prompt** for changes to take effect

---

## How to Keep It Running

### Option 1: Leave Command Prompt Open
- Just minimize the window
- Don't close it
- Computer must stay on

### Option 2: Run as Background Service (Advanced)

Create a file called `run_scheduler.bat`:

```batch
@echo off
cd C:\Users\timma\OneDrive\Desktop\emailcmds\files
python multi_time_scheduler.py
pause
```

Then:
1. Right-click `run_scheduler.bat` → Create Shortcut
2. Press `Windows + R`, type `shell:startup`, press Enter
3. Move the shortcut there
4. It will start automatically when you log in

### Option 3: Windows Task Scheduler

1. Open **Task Scheduler**
2. Create Basic Task
3. Name: "LinkedIn Job Tracker"
4. Trigger: "When I log on"
5. Action: "Start a program"
   - Program: `python`
   - Arguments: `multi_time_scheduler.py`
   - Start in: `C:\Users\timma\OneDrive\Desktop\emailcmds\files`
6. Finish

---

## Test It First!

Before leaving it to run, test manually:

```cmd
# Test the email parser
python linkedin_email_parser.py

# Test the email sender
python email_sender.py

# Then start the scheduler
python multi_time_scheduler.py
```

---

## What You'll Receive

Every 3 hours (9 AM, 12 PM, 3 PM, 6 PM CST), you'll get an email:

**Subject:** LinkedIn Jobs Tracker - February 08, 2026 at 9:00 AM CST

**Attachment:** linkedin_jobs_tracker.xlsx

The spreadsheet will have:
- All jobs sorted by priority
- Priority 1 (Green) = Oracle ERP/EPM + Manager + PwC jobs at the top
- Priority 2 (Yellow) = Other Oracle positions
- Priority 3 (White) = General jobs

---

## Troubleshooting

### "pytz not found"
```cmd
python -m pip install pytz
```

### Email not sending
- Check you're using **app password**, not regular password
- For Gmail, make sure "Less secure app access" is NOT blocking it
- Try sending a test email: `python email_sender.py`

### Spreadsheet not attached
- Run `python linkedin_email_parser.py` first to create the file
- Check that `linkedin_jobs_tracker.xlsx` exists in the folder

### Wrong time zone
- The scheduler uses Central Time (CST)
- If you're in a different timezone, edit line 13 in `multi_time_scheduler.py`

---

## Files You Need

Make sure these are all in the same folder:
- ✅ `linkedin_email_parser.py`
- ✅ `email_sender.py`
- ✅ `multi_time_scheduler.py`

---

## Commands Quick Reference

```cmd
# Navigate to folder
cd C:\Users\timma\OneDrive\Desktop\emailcmds\files

# Set credentials (each session)
set EMAIL_ADDRESS=your@email.com
set EMAIL_PASSWORD=your_app_password
set IMAP_SERVER=imap.gmail.com

# Run scheduler
python multi_time_scheduler.py
```

---

## Stop the Scheduler

Press **Ctrl+C** in the Command Prompt window.

Or close the Command Prompt window entirely.

---

Good luck with your job search! 🎯
