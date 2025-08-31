from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import os
from datetime import datetime

print('Enter some skill you are not familiar with')
unfamiliar_skill = input('>')
print(f'Filtering out {unfamiliar_skill}')

# Save file into 'posts' folder
today_str = datetime.now().strftime("%Y-%m-%d")
EXCEL_FILE = os.path.join("posts", f"jobs_{today_str}.xlsx")

def find_jobs():
    html_text = requests.get(
        'https://m.timesjobs.com/mobile/jobs-search-result.html?txtKeywords=python&cboWorkExp1=-1&txtLocation='
    ).text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('div', class_='srp-listing clearfix')
    
    job_list = []
    for job in jobs:
        published_date = job.find('span', class_='posting-time').text
        if 'days' in published_date:
            company_name = job.find('span', class_='srp-comp-name').text.strip()
            skills = job.find('div', class_='srp-keyskills').text.strip()
            more_info = job.div.h3.a['href']
            
            if unfamiliar_skill not in skills:
                job_list.append({
                    "Company Name": company_name,
                    "Required Skills": skills,
                    "More Info": more_info,
                    "Published": published_date
                })
    
    if job_list:
        df = pd.DataFrame(job_list, columns=["Company Name", "Required Skills", "More Info", "Published"])
        
        if not os.path.isfile(EXCEL_FILE):
            # First run of the day -> create new Excel file
            df.to_excel(EXCEL_FILE, index=False)
        else:
            # If file exists > append without losing old data
            existing_df = pd.read_excel(EXCEL_FILE)
            combined = pd.concat([existing_df, df], ignore_index=True)
            combined.to_excel(EXCEL_FILE, index=False)
        
        print(f"Saved {len(job_list)} jobs to {EXCEL_FILE}")
    else:
        print("No new jobs found.")

if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
