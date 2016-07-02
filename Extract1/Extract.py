# Python selenium 
# intermarchedrive
# Create By amok Team
# Created on: 07-02-2016
#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
job_list=[]
#fs = open("result/everjobs.csv", "r+")
#fs=open("result/everjobs.csv","r+")
file=open("result/everjobs.csv","w")
file.write("company_name;location;logo;title;description;requirement;updated_at;url\n")
file=open("result/everjobs.csv","a")
def init_driver():
    driver = webdriver.Firefox()
    return driver
def lookup(driver):
    try:
        driver.get("https://www.everjobs.com.kh/en/top/jobs/")
        allCategories = []
        allCategoriesSelector= driver.find_elements_by_css_selector(".container > div > section > div > div > a")
        #get all category url
       # i=0 #remove here
        for selector in allCategoriesSelector:
            #if i<1: #remove here
            allCategories.append(selector.get_attribute('href'))
            #i=i+1 #remove here
        #print "{}".format(allCategories)
        print "There are {} categories".format(len(allCategories))
        all_posts_url=[]
        #go each category url,get pagin,get post url
        for category in allCategories:
            print "go to category >> {}".format(category)
            driver.get(category)
            pagin=int(driver.find_element_by_css_selector("div:nth-child(1) > div > div > div > ul > li > form > .pagination-page-number > strong").text)
            print "There are {} pagin".format(pagin)
            #get url each pagination
            #pagin=1 #remove here
            for i in range(1,(pagin+1)):
                print "Go to >>>>>>>>>>>> {}/?page={}".format(category,str(i))
                driver.get(category+"/?page="+str(i))
                temp_selectors = driver.find_elements_by_css_selector(".col-xs-12 > .panel.hidden-sm > div.panel-heading > p > strong > a")
                for selector in temp_selectors:
                    all_posts_url.append(selector.get_attribute('href'))
   
        print "There are {} jobs".format(len(all_posts_url))
        for job in all_posts_url:
            driver.get(job)
            logo=""
            location=""
            company_name=""
            title=""
            description=""
            requirement=""
            updated_at=""
            if len(driver.find_elements_by_css_selector(".job-header-thumb img"))>0:
                logo=driver.find_element_by_css_selector(".job-header-thumb img").get_attribute('src')
                logo=logo.split("?")[0]
            if len(driver.find_elements_by_css_selector(".row > div > div:nth-child(1) > div:nth-child(1) > dl > dd:nth-child(2)"))>0:
                location=driver.find_element_by_css_selector(".row > div > div:nth-child(1) > div:nth-child(1) > dl > dd:nth-child(2)").text
                location=location.split(":")[0]
            if len(driver.find_elements_by_css_selector("#job-header > div:nth-child(1) > div > h4 > a"))>0:
                company_name=driver.find_element_by_css_selector("#job-header > div:nth-child(1) > div > h4 > a").text
            if len(driver.find_elements_by_css_selector("#job-header > div:nth-child(1) > div > h3"))>0:
                title=driver.find_element_by_css_selector("#job-header > div:nth-child(1) > div > h3").text
            if len(driver.find_elements_by_css_selector(".row > div > div:nth-child(3) > div > div.dl-horizontal"))>0:
                description=driver.find_element_by_css_selector(".row > div > div:nth-child(3) > div > div.dl-horizontal").text
                description=description.replace('\n',"<br/>").replace(';',',')
            if len(driver.find_elements_by_css_selector(".row > div > div:nth-child(4) > div > div.dl-horizontal"))>0:
                requirement=driver.find_element_by_css_selector(".row > div > div:nth-child(4) > div > div.dl-horizontal").text
                requirement=requirement.replace('\n',"<br/>").replace(';',',')
            # if len(driver.find_elements_by_css_selector(".row > div > div:nth-child(5) > div > div.dl-horizontal > p"))>0:
            #     about_company=driver.find_element_by_css_selector(".row > div > div:nth-child(5) > div > div.dl-horizontal > p").text
            if len(driver.find_elements_by_css_selector("#job-date > strong"))>0:
                updated_at=driver.find_element_by_css_selector("#job-date > strong").text
            print "{};".format(title.encode("utf-8"))
            data=company_name+";"+location+";"+logo+";"+title+";"+description+";"+requirement+";"+updated_at+";"+job
            data=data.encode("utf-8")
            file.write(data+"\n")
        file.close()
        #fs.close()
        driver.close()
        print "Process Finished Successfully"
    except TimeoutException:
        print("error ")
if __name__ == "__main__":
    driver = init_driver()
    lookup(driver)
    time.sleep(5)
    driver.quit()