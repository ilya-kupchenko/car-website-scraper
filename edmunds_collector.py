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
from exceptor_lib import ex_list_search
from exceptor_lib import ex_list_length
from exceptor_lib import ex_list_clicknum
from front_scraper import scrape_options_ed

import json

data = []

opt = webdriver.ChromeOptions()
opt.add_extension("/home/ilya/Downloads/Block-image_v1.1.crx")
opt.add_extension("/home/ilya/Downloads/AdBlock-Pro_v3.8.crx")
opt.add_extension("/home/ilya/Downloads/AdBlock_v2.56.crx")
driver = webdriver.Chrome(chrome_options=opt, executable_path="/home/ilya/Downloads/chromedriver")

data_global = {"years" : []}

list_of_years = ["2005", "2010", "2014"]

list_of_makes = [ "Acura", "Audi", "BMW", "Chevrolet", "Ford"]

xpath_year_select  = '//*[@id="cpo-vin-block-pod"]/div/div/div/' + \
  'div[2]/form/div[1]/select/option'
xpath_make_select  = '//*[@id="cpo-vin-block-pod"]/div/div/div/' + \
      'div[2]/form/div[2]/select/option'
xpath_model_select = '//*[@id="cpo-vin-block-pod"]/div/div/div/' + \
        'div[2]/form/div[3]/select/option' 
xpath_trim_select = '//*[@id="cpo-vin-block-pod"]/div/div/div/' + \
        'div[2]/form/div[4]/select/option' 

counter_year = 0

for year in list_of_years:
  errstat_year = ex_list_search(driver, xpath_year_select, year)

  if (not errstat_year):
    data_global["years"].append( { "year": 
                                          { "year_value"  : int(year),
                                            "makes"      : []}} )
    counter_make = 0

    for make in list_of_makes:
      atts = 0
      while(atts < 3):
        errstat_year = ex_list_search(driver, xpath_year_select, year)
        errstat_make = ex_list_search(driver, xpath_make_select, make)
        if(not errstat_year and not errstat_make):
          break
        atts += 1
      if (atts == 2 and ( errstat_year or errstat_make)):
        break
      if (not (errstat_make or errstat_year)):
        data_global["years"][counter_year]["year"]["makes"].\
          append({ "make": { "make_name" : make, \
                             "models"    : []  }})
        [errstat_model_llength, model_llength] = ex_list_length(driver, \
        xpath_model_select)
        counter_model = 0

        for count_model in range(1, model_llength):

          atts = 0
          while(atts < 3):
            errstat_year = ex_list_search(driver, xpath_year_select, year)
            errstat_make = ex_list_search(driver, xpath_make_select, make)
            [errstat_model, model] = \
            ex_list_clicknum(driver, xpath_model_select, count_model)
            atts += 1
            if(not errstat_year and not errstat_make and not errstat_model):
              break
          if (atts == 2 and (errstat_year or errstat_make or errstat_model)):
            continue

          if (not (errstat_model or errstat_year or errstat_make)):
            data_global["years"][counter_year]["year"]["makes"]\
              [counter_make]["make"]["models"].append(\
              {"model":{"model_name" : model, "trims":[]}})
            [errstat_trim_llength, trim_llength] = ex_list_length(driver, \
            xpath_trim_select)

            counter_trim = 0
                         
            for count_trim in range(1, trim_llength):

              atts = 0
              while(atts < 3):
                errstat_year = ex_list_search(driver, xpath_year_select, year)
                errstat_make = ex_list_search(driver, xpath_make_select, make)
                errstat_model, name_model = \
                ex_list_clicknum(driver, xpath_model_select, count_model)
                [errstat_trim, trim] =\
                ex_list_clicknum(driver, xpath_trim_select, count_trim)
                nextUsedButton =  driver.find_element_by_xpath(\
                          '//*[@id="cpo-vin-block-pod"]' +
                          '/div/div/div/div[2]/form/div[5]/button/span')
                nextUsedButton.click()
                
                print "Working on: %s, %s, %s, %s ..." % (year, make, model, trim)

                [data_trim_tmp, errstat_options] = \
                  scrape_options_ed(driver, int(year)) 

                driver.get("http://www.edmunds.com/appraisal/")

                if( not errstat_year and not errstat_make \
                    and not errstat_model and not errstat_trim):
                   break
                atts += 1

              if (   atts == 2 and (errstat_year \
                  or errstat_make or errstat_model \
                  or errstat_trim or errstat_options)):
                print "Failed to collect data for %s, %s, %s, %s !" \
                      % (year, make, model, trim)
                continue

              data_global["years"][counter_year]["year"]["makes"]\
                [counter_make]["make"]["models"][counter_model]["model"]\
                ["trims"].append({"trim":{"trim_name" : trim, "trim_features":[]}})
              

              data_global["years"][counter_year]["year"]["makes"]\
                [counter_make]["make"]["models"][counter_model]\
                ["model"]["trims"][counter_trim]["trim"]["trim_features"] = data_trim_tmp
              
              counter_trim += 1

            counter_model += 1
          
        counter_make += 1

    counter_year += 1
    
print '', json.dumps(data_global, sort_keys=True, indent=1)
