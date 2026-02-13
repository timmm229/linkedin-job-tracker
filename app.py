"""
LinkedIn Job Tracker - Web Application
Cloud-based job tracker with LinkedIn API integration
"""

from flask import Flask, render_template, jsonify
import os
import requests
from datetime import datetime
import json
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# LinkedIn API Configuration
LINKEDIN_ACCESS_TOKEN = os.environ.get('LINKEDIN_ACCESS_TOKEN', '')
LINKEDIN_API_BASE = "https://api.linkedin.com/v2"

# Job storage (in production, use a database)
jobs_data = {
    'jobs': [],
    'last_updated': None
}

# Priority keywords
HIGH_PRIORITY_KEYWORDS = [
    'oracle erp', 'oracle epm', 'technical sales', 'fusion', 'netsuite',
    'manager', 'senior manager', 'pwc', 'pricewaterhousecoopers'
]

MEDIUM_PRIORITY_KEYWORDS = [
    'oracle cloud', 'oracle application', 'oracle consultant', 
    'oracle developer', 'oracle hcm', 'oracle scm'
]

def calculate_priority(job_data):
    """Calculate job priority based on keywords"""
    title = job_data.get('title', '').lower()
    company = job_data.get('company', '').lower()
    combined = f"{title} {company}"
    
    for keyword in HIGH_PRIORITY_KEYWORDS:
        if keyword in combined:
            return 1
    
    for keyword in MEDIUM_PRIORITY_KEYWORDS:
        if keyword in combined:
            return 2
    
    return 3

def fetch_linkedin_jobs():
    """Fetch jobs from LinkedIn API"""
    if not LINKEDIN_ACCESS_TOKEN:
        print("No LinkedIn access token found")
        return []
    
    headers = {
        'Authorization': f'Bearer {LINKEDIN_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    # Search keywords
    search_keywords = [
        'Oracle ERP',
        'Oracle EPM', 
        'Oracle technical sales',
        'PwC Oracle manager',
        'Oracle Fusion',
        'Oracle Cloud'
    ]
    
    all_jobs = []
    
    for keyword in search_keywords:
        try:
            params = {
                'keywords': keyword,
                'count': 25,
                'start': 0,
                'locationFallback': 'us:0'  # United States
            }
            
            response = requests.get(
                f"{LINKEDIN_API_BASE}/jobSearch",
                headers=headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('elements', [])
                
                for job in jobs:
                    job_data = {
                        'id': job.get('jobPostingId', ''),
                        'title': job.get('title', 'N/A'),
                        'company': job.get('companyDetails', {}).get('name', 'N/A'),
                        'location': job.get('formattedLocation', 'N/A'),
                        'url': f"https://www.linkedin.com/jobs/view/{job.get('jobPostingId', '')}",
                        'posted_date': job.get('listedAt', ''),
                        'description': job.get('description', {}).get('text', '')[:200],
                        'priority': 0
                    }
                    
                    job_data['priority'] = calculate_priority(job_data)
                    all_jobs.append(job_data)
                    
                print(f"Fetched {len(jobs)} jobs for '{keyword}'")
            else:
                print(f"API error for '{keyword}': {response.status_code}")
                
        except Exception as e:
            print(f"Error fetching '{keyword}': {str(e)}")
    
    # Remove duplicates by job ID
    seen_ids = set()
    unique_jobs = []
    for job in all_jobs:
        if job['id'] not in seen_ids:
            seen_ids.add(job['id'])
            unique_jobs.append(job)
    
    # Sort by priority
    unique_jobs.sort(key=lambda x: x['priority'])
    
    return unique_jobs

def update_jobs():
    """Update jobs from LinkedIn API"""
    print(f"Updating jobs at {datetime.now()}")
    jobs = fetch_linkedin_jobs()
    
    jobs_data['jobs'] = jobs
    jobs_data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S CST')
    
    print(f"Updated with {len(jobs)} jobs")

@app.route('/')
def index():
    """Main page showing all jobs"""
    return render_template('index.html', 
                         jobs=jobs_data['jobs'],
                         last_updated=jobs_data['last_updated'],
                         total_jobs=len(jobs_data['jobs']))

@app.route('/api/jobs')
def api_jobs():
    """API endpoint returning jobs as JSON"""
    return jsonify(jobs_data)

@app.route('/api/refresh')
def api_refresh():
    """Manually refresh jobs"""
    update_jobs()
    return jsonify({
        'status': 'success',
        'jobs_count': len(jobs_data['jobs']),
        'updated_at': jobs_data['last_updated']
    })

@app.route('/priority/<int:level>')
def priority_jobs(level):
    """Filter jobs by priority level"""
    filtered = [job for job in jobs_data['jobs'] if job['priority'] == level]
    return render_template('index.html',
                         jobs=filtered,
                         last_updated=jobs_data['last_updated'],
                         total_jobs=len(filtered),
                         filter_level=level)

if __name__ == '__main__':
    # Initial job fetch
    print("Starting LinkedIn Job Tracker...")
    update_jobs()
    
    # Schedule daily updates at 9 AM, 12 PM, 3 PM CST
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_jobs, 'cron', hour='9,12,15', timezone='America/Chicago')
    scheduler.start()
    
    # Run Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
