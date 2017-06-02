#!/usr/bin/env python
import sys
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selenium.common.exceptions import NoSuchElementException
import json
import time
from color_parse_lib import parse_color_string
#from specifications_lib import get_specs
from datetime import date
from front_lib import get_summary
from front_lib import get_colors
from front_lib import get_options
from front_lib import get_pricing
from exceptor_lib import ex_click_tag
from no_survey import no_survey
from specifications_lib import get_specs

def scrape_options_ed(driver, year):

    attempts = 0
    max_attempts = 3
    success = False
    error = True
    url = driver.current_url
    for attempts in range(0,max_attempts):
      try:
        
        data = { "Summary"        : "Not available",
                 "Colors"         : "Not available",
                 "Options"        : "Not available",
                 "Price"          : "Not available",
                 "Specifications" : "Not available" }
        if( attempts > 0):
	  driver.get(url)
        no_survey(driver)
        print "Getting summary, colors and options ..."
        data["Summary"] = get_summary(driver)
        
        ex_click_tag(driver, '//*[@id="section-tabs"]/ul/li[2]')
        if (no_survey(driver)):
          continue
        data["Colors"] = get_colors(driver)
        if (no_survey(driver)):
          continue
        data["Options"] = get_options(driver)
        time.sleep(0.5)      
        if (no_survey(driver)):
          continue
        firstColor = driver.find_element_by_xpath('//*[@id="exterior_1"]/div[2]')
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(firstColor, 2, 2)
        action.click()
        action.perform()
        if (no_survey(driver)):
          continue 
        mileageTab = driver.find_element_by_xpath('//*[@id="section-tabs"]/ul/li[3]')
        mileageTab.click()
        if (no_survey(driver)):
          continue 
        mileageVal = (date.today().year - year) * 15000  
        ex_click_tag(driver, '//*[@id="cln_lbl"]')
        if (no_survey(driver)):
          continue
        mileageField = driver.find_element_by_id('mileage')
        mileageField.send_keys(str(mileageVal))
        if (no_survey(driver)):
          continue
        ex_click_tag(driver, '//*[@id="gp_submit"]/span')
        if (no_survey(driver)):
          continue
        noemailButton = driver.find_element_by_xpath(\
        '//*[@id="step-appraisal"]/div[2]/form/img')
        while not noemailButton.is_displayed():
          continue
        ex_click_tag(driver, '//*[@id="step-appraisal"]/div[2]/form/img')
        if (no_survey(driver)):
          continue
        print "Getting price ..."
        data["Price"] = get_pricing(driver, year)
        if (no_survey(driver)):
          continue
        driver.back()
        time.sleep(0.3)
        if (no_survey(driver)):
          continue 
        ex_click_tag(driver, '//*[@id="page-title"]/ul/li[6]/a')
        if (no_survey(driver)):
          continue 
        time.sleep(0.3)
        print "Getting specializations ..."
        data["specifications"] = get_specs(driver)
        success = True
      except:
        pass
      if(success):
        error = False
        return [data, error] 
        break
      attempts += 1
    return ["Not available", error]
