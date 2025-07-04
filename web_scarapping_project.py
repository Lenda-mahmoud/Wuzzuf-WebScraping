# -*- coding: utf-8 -*-
"""Web_Scarapping_Project.ipynb

"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

all_data=[]
key_words=["machine learning" , "data analysis" , "business intelligence" , "data scientist"]

for keyword in key_words:
    print(f"Scraping jobs for {keyword}")
    for page in range(0,6):
        print(f"  Processing page {page+1}")
        url=f"https://wuzzuf.net/search/jobs/?a=hpb&q={keyword.replace(' ' , '%20')}&start={page}"
        response=requests.get(url)

        soup=BeautifulSoup(response.content,"lxml")

        titles=soup.find_all("h2" , {"class":"css-m604qf"})
        title_list=[title.a.text for title in titles]

        links=[title.a['href'] for title in titles]

        occupations=soup.find_all('div' , {'class':'css-1lh32fc'})
        occupation_list=[occ.text for occ in occupations]

        companies=soup.find_all('a' , {'class':'css-17s97q8'})
        company_list=[comp.text.replace(' -' , '') for comp in companies]

        specs=soup.find_all("div" , {'class':"css-y4udm8"})
        specs_list=[spec.text for spec in specs]

        locations=soup.find_all('span' , {'class':'css-5wys0k'})
        location_list=[loc.text for loc in locations]

        for i in range(len(title_list)):
            try:
                all_data.append({
                    "Keyword":keyword,
                    "Title":title_list[i],
                    "Link":links[i],
                    "Occupation":occupation_list[i] if i < len(occupation_list) else "",
                    "Company": company_list[i] if i < len(company_list) else "",
                    "Specs": specs_list[i] if i < len(specs_list) else "",
                    "Location": location_list[i] if i < len(location_list) else ""
                })
            except:
                continue

data_frame=pd.DataFrame(all_data)
data_frame.to_csv("wuzzuf_Tech_jobs_.csv" , index=False)
print("Data has been saved to wuzzuf_jobs_all_keywords.csv")

