#!/usr/bin/env python3
"""
Multi-Time Scheduler for LinkedIn Job Tracker
Runs at 9 AM, 12 PM, 3 PM, and 6 PM CST daily
- Checks email for new LinkedIn job alerts
- Updates spreadsheet
- Emails you the updated spreadsheet
"""
import schedule
import time
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path
import pytz

# Get the directory where THIS script is located
SCRIPT_DIR = Path(__file__).parent.absolute()

# Central Standard Time
CST = pytz.timezone('America/Chicago')

def run_parser_and_email():
    """Run the parser, then email the results"""
    current_time = datetime.now(CST).strftime('%I:%M %p CST')
    
    print(f"\n{'='*70}")
    print(f"LinkedIn Job Tracker - Running at {current_time}")
    print(f"{'='*70}\n")
    
    # Step 1: Parse emails and update spreadsheet
    print("Step 1: Checking email for new LinkedIn job alerts...")
    try:
        parser_path = SCRIPT_DIR / 'linkedin_email_parser.py'
        
        result = subprocess.run(
            [sys.executable, str(parser_path)],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(SCRIPT_DIR)  # Run in the script directory
        )
        
        print(result.stdout)
        
        if result.returncode != 0:
            print(f"ERROR: Parser failed with code {result.returncode}")
            print(result.stderr)
            return
            
    except subprocess.TimeoutExpired:
        print("ERROR: Parser timed out after 5 minutes")
        return
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return
    
    # Step 2: Email the spreadsheet
    print("\nStep 2: Emailing spreadsheet to you...")
    try:
        email_sender_path = SCRIPT_DIR / 'email_sender.py'
        
        result = subprocess.run(
            [sys.executable, str(email_sender_path)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(SCRIPT_DIR)  # Run in the script directory
        )
        
        print(result.stdout)
        
        if result.returncode != 0:
            print(f"ERROR: Email sender failed with code {result.returncode}")
            print(result.stderr)
        else:
            print(f"\n✓ Complete! Spreadsheet emailed at {current_time}")
            
    except subprocess.TimeoutExpired:
        print("ERROR: Email sender timed out")
    except Exception as e:
        print(f"ERROR: {str(e)}")

def main():
    """Main scheduler loop"""
    
    print(f"Script directory: {SCRIPT_DIR}\n")
    
    # Schedule for 9 AM, 12 PM, 3 PM, and 6 PM CST
    schedule.every().day.at("09:00").do(run_parser_and_email)
    schedule.every().day.at("12:00").do(run_parser_and_email)
    schedule.every().day.at("15:00").do(run_parser_and_email)  # 3 PM in 24-hour format
    schedule.every().day.at("18:00").do(run_parser_and_email)  # 6 PM in 24-hour format
    
    print(f"LinkedIn Job Tracker - Multi-Time Scheduler")
    print(f"{'='*70}")
    print(f"Scheduled to run at:")
    print(f"  • 9:00 AM CST")
    print(f"  • 12:00 PM CST")
    print(f"  • 3:00 PM CST")
    print(f"  • 6:00 PM CST")
    print(f"\nEach run will:")
    print(f"  1. Check your email for new LinkedIn job alerts")
    print(f"  2. Update the spreadsheet with new jobs")
    print(f"  3. Email you the updated spreadsheet")
    print(f"\nPress Ctrl+C to stop")
    print(f"{'='*70}\n")
    
    # Show current time and next run
    now = datetime.now(CST)
    print(f"Current time: {now.strftime('%I:%M %p CST on %A, %B %d, %Y')}")
    
    # Check if we should run immediately (if it's close to a scheduled time)
    current_hour = now.hour
    current_minute = now.minute
    
    # If within 5 minutes of a scheduled time, run now
    scheduled_hours = [9, 12, 15, 18]
    if current_hour in scheduled_hours and current_minute < 5:
        print(f"\nRunning immediately (scheduled time)...")
        run_parser_and_email()
    else:
        print(f"\nWaiting for next scheduled run...")
    
    # Main loop
    while True:
        schedule.run_pending()
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user")
        sys.exit(0)
