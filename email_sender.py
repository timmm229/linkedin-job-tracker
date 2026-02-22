#!/usr/bin/env python3
"""
Email Spreadsheet Sender
Sends the LinkedIn jobs tracker spreadsheet via email
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from datetime import datetime

# Email Configuration
SENDER_EMAIL = os.environ.get('EMAIL_ADDRESS', '')
SENDER_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', SENDER_EMAIL)  # Defaults to same email

EXCEL_FILE = "linkedin_jobs_tracker.xlsx"

def send_spreadsheet_email():
    """Send the Excel file via email"""
    
    if not os.path.exists(EXCEL_FILE):
        print(f"Error: {EXCEL_FILE} not found. Run the parser first.")
        return False
    
    # Determine SMTP server based on email provider
    if 'gmail' in SENDER_EMAIL.lower():
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
    elif 'outlook' in SENDER_EMAIL.lower() or 'hotmail' in SENDER_EMAIL.lower():
        smtp_server = 'smtp-mail.outlook.com'
        smtp_port = 587
    elif 'yahoo' in SENDER_EMAIL.lower():
        smtp_server = 'smtp.mail.yahoo.com'
        smtp_port = 587
    else:
        smtp_server = 'smtp.gmail.com'  # Default to Gmail
        smtp_port = 587
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f'LinkedIn Jobs Tracker - {datetime.now().strftime("%B %d, %Y at %I:%M %p CST")}'
        
        # Email body
        body = f"""
Hello!

Here's your latest LinkedIn Jobs Tracker spreadsheet with Oracle-related positions.

Generated: {datetime.now().strftime("%A, %B %d, %Y at %I:%M %p CST")}

Priority levels:
• Priority 1 (Green) - Oracle ERP/EPM/Technical Sales + Manager/Senior Manager + PwC
• Priority 2 (Yellow) - Other Oracle Cloud/Applications positions
• Priority 3 (White) - General Oracle positions

The highest priority jobs are at the top of the spreadsheet.

Best of luck with your job search!

---
This is an automated email from your LinkedIn Job Tracker.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach Excel file
        with open(EXCEL_FILE, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {EXCEL_FILE}'
        )
        
        msg.attach(part)
        
        # Send email
        print(f"Connecting to {smtp_server}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        print(f"Sending email to {RECIPIENT_EMAIL}...")
        server.send_message(msg)
        server.quit()
        
        print(f"✓ Email sent successfully at {datetime.now().strftime('%I:%M %p CST')}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

if __name__ == "__main__":
    print(f"LinkedIn Job Tracker - Email Sender")
    print(f"{'='*70}")
    
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("ERROR: Email credentials not set")
        print("\nSet these environment variables:")
        print("  EMAIL_ADDRESS - Your email address")
        print("  EMAIL_PASSWORD - Your app password")
        print("  RECIPIENT_EMAIL - Where to send (optional, defaults to sender)")
    else:
        send_spreadsheet_email()
