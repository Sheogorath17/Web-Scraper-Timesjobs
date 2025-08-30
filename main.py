from bs4 import BeautifulSoup
import requests
import time


print('Enter some skill you are not familiar with')
unfamiliar_skill = input ('>')
print(f'Filtering out {unfamiliar_skill}')

def find_jobs():
        html_text = requests.get('https://m.timesjobs.com/mobile/jobs-search-result.html?txtKeywords=python&cboWorkExp1=-1&txtLocation=').text
        soup = BeautifulSoup(html_text, 'lxml')
        jobs = soup.find_all('div', class_ = 'srp-listing clearfix')
        for index, job in enumerate(jobs):
            published_date = job.find('span', class_ = 'posting-time').text
            if 'days' in published_date:
                company_name = job.find('span', class_ = 'srp-comp-name').text
                skills = job.find('div', class_ = 'srp-keyskills').text
                more_info =job.div.h3.a['href']
                if unfamiliar_skill not in skills:
                    with open(f'posts/{index}.txt', 'w') as f:
                         
                        f.write(f"Company Name: {company_name.strip()} \n")
                        f.write(f"Required Skills: {skills.strip()} \n")
                        f.write(f'More Info: {more_info}')
                    print(f'File saved: {index}')
                        
                    print(f'File saved: {index}')


if __name__== '__main__':
     while True:
          find_jobs()
          time_wait = 10
          print(f'Waiting {time_wait} minutes...')
          time.sleep(time_wait * 60)