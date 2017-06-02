#!/usr/bin/env python
import sys
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException        
from scropt2b import scrape_options
import time
import json

data = []

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def no_thanks_survey():
  try:
    zipCodeField = driver.find_element_by_id('selectedZipCode')
    zipCodeField.send_keys("90007")
    zipCodeField.send_keys(Keys.RETURN)
  except:
    pass
  while (True):
    try:
      driver.find_element_by_xpath('//*[@id="sign-in-header"]').click()
      #print "\nCURRENT URL: %s\n" % driver.current_url
      break
    except:
      driver.get(driver.current_url)
      driver.implicitly_wait(1) 

def traverse_style_page():
  data_style_arr_json = "Not available"
  try:
    styleOptions =  driver.find_elements_by_xpath(\
      '//*[@id="Styles-list-container"]/div/div/'+\
      'div/div[1]/div[@class="style-name section-title"]')
    nStyles = len(styleOptions)
    data_style_arr_json = []
    s = 0
  #print ",\"styles\":["
    while (s < nStyles):
      try:
        styleOptions =  driver.find_elements_by_xpath(\
          '//*[@id="Styles-list-container"]/div/div'+\
          '/div/div[1]/div[@class="style-name section-title"]')
        styleOption = styleOptions[s]
        driver.execute_script("return arguments[0].scrollIntoView();", styleOption)
        styleLink = styleOption.find_element_by_xpath('./following-sibling::a[1]')
        trimName = styleOption.text
        #print "{\"style\":\"%s\"}" % styleOption.text
        #print "{\"link\":\"%s\"}"  % styleLink.text
        data_style_arr_json
        styleLink.click()
        no_thanks_survey() 
        data_options_arr = scrape_options(driver)
        driver.back()
        data_style_arr_json.append({"trim_name":trimName, "equipment":data_options_arr})
        driver.implicitly_wait(0.5)
        no_thanks_survey()
        #if (s < nStyles - 1):
          #print ","
      except:
        pass
      s += 1
  except:
    pass
  #print "]"
  return data_style_arr_json

def traverse_category_page():
  data_cat_arr_json = "Not available"
  try:
    categoryOptions =  driver.find_elements_by_xpath('//*[@id="Content"]/div[7]/section/div[1]/div/div/a')
    nCategories = len(categoryOptions)
    c = 0
    data_cat_arr_json = []
    #print ",\"categories\":["
    while (c < nCategories):
      try:
        categoryOptions =  driver.find_elements_by_xpath('//*[@id="Content"]/div[7]/section/div[1]/div/div/a')
        categoryOption = categoryOptions[c]
        driver.execute_script("return arguments[0].scrollIntoView();", categoryOption)
        data_cat_arr_json.append({"category":categoryOption.text, "trims":None})
        #print "{\"category\":\"%s\"" % categoryOption.text
        categoryOption.click()
        no_thanks_survey()
        data_styles_json = traverse_style_page()
        data_cat_arr_json[c]["trims"] = data_styles_json
        driver.back()
        driver.implicitly_wait(1)
        #print "}"
        #if (c < nCategories - 1):
          #print ","
      except:
        pass
      c += 1
    #print "]"
  except:
    pass
  return data_cat_arr_json

def selectedYearMake(yearMake, callId):
  if (callId == 1):
    yearArr = ["2000", "2005", "2010"]
    for yearEl in yearArr:
      if (yearMake == yearEl):
        return True
  elif (callId == 2):
    makeArr = ["Acura", "Audi", "BMW", "Chevrolet"]
    for makeEl in makeArr:
      if (yearMake == makeEl):
        return True
  return False 


driver = webdriver.Chrome(executable_path="/home/ilya/Downloads/chromedriver")
driver.get("http://www.kbb.com/used-cars/")
no_thanks_survey()

data_gl = []

yearOptions = driver.find_elements_by_xpath('//form[1]/div/div[1]/div[1]/select/option')
nYears = len(yearOptions)
i = 1
ii = 1
data_gl.append({"years":[]})
while (ii < nYears):
  no_thanks_survey()
  yearOptions = driver.find_elements_by_xpath('//form[1]/div/div[1]/div[1]/select/option')
  yearOption = yearOptions[ii]
  yearText = yearOption.text
  yearOption.click()
  time.sleep(0.6)
  print "\nYEAR: %s  i: %s  ii: %s\n" % (yearText, i, ii)
  if (selectedYearMake(yearText, 1)):
    data_gl[0]["years"].append({"year":int(yearText), "makes":[]})
    driver.implicitly_wait(1)
    makeOptions = driver.find_elements_by_xpath('//form[1]/div/div[1]/div[2]/select/option')
    nMakes = len(makeOptions)
    j = 1
    jj = 1
    while (jj <nMakes):
        time.sleep(0.6)
        no_thanks_survey()
        yearOptions = driver.find_elements_by_xpath('//form[1]/div/div[1]/div[1]/select/option')
        yearOption = yearOptions[ii]
        yearOption.click()
        time.sleep(0.6)
        no_thanks_survey()
        makeOptions = driver.find_elements_by_xpath('//form[1]/div/div[1]/div[2]/select/option')
        makeOption = makeOptions[jj]
        makeText = makeOption.text
        makeOption.click()
        print "\nSELECTEDYEAR: %s\t MAKE: %s  i: %s  ii: %s   j:%s  jj:%s\n" % (yearText, makeText, i, ii, j, jj)
        if (selectedYearMake(makeText, 2)):
          print "\nSELECTEDYEAR: %s\t SELECTEDMAKE: %s  i: %s  ii: %s   j:%s  jj:%s\n" % (yearText, makeText, i, ii, j, jj)
          driver.implicitly_wait(1)
          data_gl[0]["years"][i-1]["makes"].append({"make":makeText, "models":[]})
          modelOptions = driver.find_elements_by_xpath('//form[1]/div/div[1]/div[3]/select/option')
          nModels = len(modelOptions)
          k = 2
          while (k < nModels-1):
            success = False
            att = 0
            while (not success and att < 10):
              try:
                att += 1
                no_thanks_survey()
                yearOptions =  driver.find_elements_by_xpath(\
                '//form[1]/div/div[1]/div[1]/select/option')
                yearOption = yearOptions[ii]
                yearOption.click()
                time.sleep(0.6)
                driver.implicitly_wait(1)
                makeOptions =  driver.find_elements_by_xpath(\
                '//form[1]/div/div[1]/div[2]/select/option')
                makeOption = makeOptions[jj]
                makeOption.click()
                time.sleep(0.6)
                no_thanks_survey()
                modelOptions = driver.find_elements_by_xpath(\
                '//form[1]/div/div[1]/div[3]/select/option')
                modelOption = modelOptions[k]
                modelText = modelOption.text
                modelOption.click()
                no_thanks_survey()
                time.sleep(0.6)
                nextUsedButton =  driver.find_element_by_id('ymm-submit')
                nextUsedButton.click()
                driver.implicitly_wait(1)
                no_thanks_survey()
                if (check_exists_by_xpath(\
                '//*[@id="Styles-list-container"]/div/'+\
                'div/div[2]/div[1]/div[@class="style-name'+\
                ' section-title"]')): 
                  try:
                    data_trim = traverse_style_page()
                  except:
                    data_trim = "Not available"
                  data_gl[0]["years"][i-1]["makes"][j-1]["models"].append({"model":modelText, "styles":[data_trim]})
                  driver.get("http://www.kbb.com/used-cars/")
                  time.sleep(0.6)
                  k += 1
                  continue
                elif (check_exists_by_xpath('//*[@id="Content"]'+\
                '/div[7]/section/div[1]/div[1]/div[@class="mod-category-inner"]/a')):
                  try:
                    data_cat = traverse_category_page()
                  except:
                    data_cat = "Not available"
                  data_gl[0]["years"][i-1]["makes"][j-1]["models"].append({"model":modelText, "styles":[data_cat]})
                  driver.get("http://www.kbb.com/used-cars/")
                  k += 1
                  continue
                elif (check_exists_by_xpath('//*[@id="Options-container"]')):
                  try:
                    data_opt = scrape_options(driver)
                  except:
                    data_opt = "Not available"
                  data_gl[0]["years"][i-1]["makes"][j-1]["models"].append({"model":modelText, "styles":[data_opt]})
                  driver.get("http://www.kbb.com/used-cars/")
                  k += 1
                  continue
                driver.back()
                success = True
                time.sleep(0.3)
              except:
                pass
              if (success):
                break
              time.sleep(3)
            k += 1
          j += 1
        jj += 1
    i += 1
  ii += 1

print '\n\n\n\n\nINDENT:', json.dumps(data_gl, sort_keys=True, indent=1)
