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
file_url=open("result/urls.csv","w")
file_url.write("")
file_url=open("result/urls.csv","a")

file=open("result/everjobs.csv","w")
file.write("company_name;location;logo;title;Category;description;requirement;updated_at;contract_type;url\n")
file=open("result/everjobs.csv","a")
def init_driver():
    driver = webdriver.Firefox()
    return driver
def lookup(driver):
    try:
        driver.get("https://www.everjobs.com.kh/en/top/categories/")
        allCategories = []
        allCategoriesSelector= driver.find_elements_by_css_selector(".container > div > section > div > div > a")
        #get all category url
        #i=0 #remove here
        for selector in allCategoriesSelector:
            #if i<1: #remove here
            category_name=(selector.text).split("(")[0]
            print "Category Name ==>"+category_name
            allCategories.append(selector.get_attribute('href')+"::"+category_name)
            #i=i+1 #remove here
        #print "{}".format(allCategories)
        print "There are {} categories".format(len(allCategories))
        all_posts_url=[]
        #go each category url,get pagin,get post url
        #i=0
        for category in allCategories:
            #if i==0:
            print "go to category >> {}".format(category.split("::")[0])
            driver.get(category.split("::")[0])
            pagin=int(driver.find_element_by_css_selector("div:nth-child(1) > div > div > div > ul > li > form > .pagination-page-number > strong").text)
            print "There are {} pagin".format(pagin)
            #get url each pagination
            #pagin=1 #remove here
            for i in range(1,(pagin+1)):
                print "Go to >>>>>>>>>>>> {}?page={}".format(category.split("::")[0],str(i))
                driver.get(category.split("::")[0]+"?page="+str(i))
                temp_selectors = driver.find_elements_by_css_selector(".col-xs-12 > .panel.hidden-sm > div.panel-heading > p > strong > a")
                for selector in temp_selectors:
                    all_posts_url.append(selector.get_attribute('href')+"::"+category.split("::")[1])
            #i=i+1
        print "There are {} jobs".format(len(all_posts_url))
        i=0
        for job in all_posts_url:
            driver.get(job.split("::")[0])
            logo=""
            location=""
            company_name=""
            title=""
            category=(job.split("::")[1]).replace(";",',')
            description=""
            requirement=""
            updated_at=""
            contract_type=""
            if len(driver.find_elements_by_css_selector(".row > div > div:nth-child(1) > div:nth-child(1) > dl > dd:nth-child(6)"))>0:
                if driver.find_element_by_css_selector("#job-view > div.col-md-12.ca-wrapper > div.col-xs-12.white-box > div > div.col-md-8.col-xs-12 > div.row > div > div:nth-child(1) > div:nth-child(1) > dl > dt:nth-child(5)").text=="Contract Type:":
                    contract_type=driver.find_element_by_css_selector(".row > div > div:nth-child(1) > div:nth-child(1) > dl > dd:nth-child(6)").text
                elif driver.find_element_by_css_selector("#job-view > div.col-md-12.ca-wrapper > div.col-xs-12.white-box > div > div.col-md-8.col-xs-12 > div.row > div > div:nth-child(1) > div:nth-child(1) > dl > dt:nth-child(3)").text=="Contract Type:":
                    contract_type=driver.find_element_by_css_selector("#job-view > div.col-md-12.ca-wrapper > div.col-xs-12.white-box > div > div.col-md-8.col-xs-12 > div.row > div > div:nth-child(1) > div:nth-child(1) > dl > dd:nth-child(4)").text

            if len(driver.find_elements_by_css_selector(".job-header-thumb img"))>0:
                logo=driver.find_element_by_css_selector(".job-header-thumb img").get_attribute('src')
                logo=logo.split("?")[0]
            if len(driver.find_elements_by_css_selector(".row > div > div:nth-child(1) > div:nth-child(1) > dl > dd:nth-child(2)"))>0:
                location=driver.find_element_by_css_selector(".row > div > div:nth-child(1) > div:nth-child(1) > dl > dd:nth-child(2)").text
                location=location.split(":")[0]
                location=location.replace(';',',')
            if len(driver.find_elements_by_css_selector("#job-header > div:nth-child(1) > div > h4 > a"))>0:
                company_name=driver.find_element_by_css_selector("#job-header > div:nth-child(1) > div > h4 > a").text
                company_name=company_name.replace(';',',')
            if len(driver.find_elements_by_css_selector("#job-header > div:nth-child(1) > div > h3"))>0:
                title=driver.find_element_by_css_selector("#job-header > div:nth-child(1) > div > h3").text
                title=title.replace(';',',')
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
            print str(i)+" - {}".format(title.encode("utf-8"))
            data=company_name+";"+location+";"+logo+";"+title+";"+category+";"+description+";"+requirement+";"+updated_at+";"+contract_type+";"+job.split("::")[0]
            data=data.encode("utf-8")
            file_url.write((job.split("::")[0]).encode("utf-8")+"\n")
            file.write(data+"\n")
            i=i+1
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
