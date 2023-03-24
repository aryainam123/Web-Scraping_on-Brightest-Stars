from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests
from selenium.webdriver.common.by import By



START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

browser = webdriver.Edge("C:\\Users\\DELL\\OneDrive\\Desktop\\msedgedriver.exe")
browser.get(START_URL)
time.sleep(10)
planets_data = []
headers = ["Proper name","Distance(ly)","Mass(M)","Radius(R)"]

def scrape():
    
    planet_data = []
    for i in range(0,97):
        soop = BeautifulSoup(browser.page_source,"html.parser")
        for th_tag in soop.find_all("th",attrs={"class","headerSort"}):
            td_tags = th_tag.find_all("td")
            temp_list = []
            for index,td_tag in enumerate(td_tags):
                if index==0:
                    temp_list.append(td_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(td_tag.contents[0])
                    except:
                        temp_list.append("")
            planet_data.append(temp_list)
        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()  
    with open("scrapper_2.csv","w")as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(headers)
        csv_writer.writerows(planet_data)
scrape()

new_planets_data = []
def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
      
        soup = BeautifulSoup(page.content, "html.parser")

        temp_list = []

        for tr_tag in soup.find_all("th", attrs={"class": "headerSort"}):
            td_tags = tr_tag.find_all("td")
          
            for td_tag in td_tags:
                try: 
                    temp_list.append(td_tag.find_all("td", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
                    
        new_planets_data.append(temp_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
        
for index, data in enumerate(planets_data):
    scrape_more_data(data[5])
    print(f"scraping at hyperlink {index+1} is completed.")
