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
from color_parse_lib import parse_color_string
from datetime import date
from exceptor_lib import ex_read_list
from exceptor_lib import ex_read_fcol


def get_summary(driver):

  dataSummary = {  "Engine"        : "Not available",
                   "Drive_type"    : "Not available", 
                   "Transmission"  : "Not available",
                   "Cylinders"     : "Not available",
                   "Engine_volume" : "Not available", 
                   "URL"           : driver.current_url }
  try:
    [errstat_readl, tmpSummary] = ex_read_list(driver, '//*[@id="style-detail"]/ul/li', 3)
    if (not errstat_readl and len(tmpSummary)==3):
      dataSummary = { "Engine"        : tmpSummary[0], \
                      "Drive_type"    : tmpSummary[1], \
                      "Transmission"  : tmpSummary[2], \
                      "Cylinders"     : "Not available",
                      "Engine_volume" : "Not available", 
                       "URL"          : driver.current_url\
                    }
      try:
        dataSummary["Cylinders"] = int(re.search('\d{1,2}', re.search('[^.]\d{1,2}[^.]', \
        tmpSummary[0]).group()).group())
        dataSummary["Engine_volume"] = float(re.search('\d{1,2}[.]{1}\d{1}', \
        tmpSummary[0]).group())
      except:
        pass
  except:
    pass
  return dataSummary


def get_colors(driver):

  try:
    dataColors = { "URL"    : driver.current_url, \
                   "Color List" : [] }

    [errstat_fcol, colorNames, colorIDs] = ex_read_fcol(driver,\
      '//*[@id="exterior_colors"]/label/span/div[@class="primary"]',\
      '//*[@id="exterior_colors"]/input', \
      'style', \
      'value')

    if (not errstat_fcol): 
      #print "no error in ex_read_col"
      for cname, cid in zip(colorNames, colorIDs):
        #print "appending"
        #print "hi4"
        [errstat_prs, colorHTML] = parse_color_string(cname)
        if (not errstat_prs and colorHTML != ''):
          #print "hi5"
          dataColors["Color List"].append({colorHTML:{ "color_id": cid,  \
            "color_name":colorHTML}})
    else:
      dataColors["Color List"] = "Not available"
    return dataColors
  except:
    dataColors = { "URL"    : driver.current_url, \
     "Color List" : "Not available" }
    return dataColors


def get_options(driver):
  try:
    dataOptions = {"URL": driver.current_url,
                   "Options List":[]}
    optionsListLabels = driver.find_elements_by_xpath('//*[@id="option_checkbox_list"]/li/label')
    if (len(optionsListLabels) != 0):
      optionsListInputs = driver.find_elements_by_xpath('//*[@id="option_checkbox_list"]/li/input')
      i = 0
      for optionFlag in optionsListLabels:
        try:
          optionName = optionFlag.text
          optionID = optionsListInputs[i].get_attribute("value")
          dataOptions["Options List"].append({optionName:{ "option_id": optionID,
                                          "option_name": optionName }})
        except:
          pass
        i += 1
    else:
      dataOptions["Options List"] = "Not available"
    return dataOptions
  except:
    dataOptions = {"URL": driver.current_url,
                   "Options List":"Not available"}
    return dataOptions


def get_pricing(driver, year):
  dataPricing = "Not available"
  try:
    mileageValAv = (date.today().year - year) * 15000
    mileageValLo = (date.today().year - year) * 10000
    mileageValHi = (date.today().year - year) * 20000

  
    priceTradeinTag = driver.find_element_by_xpath( \
      '//*[@id="tmv-appraiser-results"]/ul[1]/li[8]/ul/li[2]')
    driver.execute_script("return arguments[0].scrollIntoView();", priceTradeinTag)
    pricePrivateTag = driver.find_element_by_xpath( \
      '//*[@id="tmv-appraiser-results"]/ul[1]/li[8]/ul/li[3]')
    driver.execute_script("return arguments[0].scrollIntoView();", pricePrivateTag)
    priceDealerTag  = driver.find_element_by_xpath( \
      '//*[@id="tmv-appraiser-results"]/ul[1]/li[8]/ul/li[4]')
    mileageAdjTag   = driver.find_element_by_xpath( \
      '//*[@id="tmv-appraiser-results"]/ul[1]/li[6]/ul/li[4]')
    driver.execute_script("return arguments[0].scrollIntoView();", mileageAdjTag)
  
    priceTradeinVal = int(re.sub('[^0-9]', '', priceTradeinTag.text))
    pricePrivateVal = int(re.sub('[^0-9]', '', pricePrivateTag.text))
    priceDealerVal  = int(re.sub('[^0-9]', '', priceDealerTag.text))
    mileageAdjVal   = int(re.sub('[^0-9]', '', mileageAdjTag.text)) / (mileageValAv / 1000)
  
    dataPricing = { "price_adjustment_per_1000_miles": mileageAdjVal,
                    "currency": "USD",
                    "average_usage": { "mean_mileage":   mileageValAv,
                                       "trade-in_price": priceTradeinVal,
                                       "private_price":  pricePrivateVal,
                                       "dealer_price":   priceDealerVal
                                     },
                    "low_usage":     { "mean_mileage":   mileageValLo,
                                       "trade_in_price": priceTradeinVal + 
                                                         (mileageValAv - mileageValLo)/1000 * mileageAdjVal,
                                       "private_price":  pricePrivateVal +
                                                         (mileageValAv - mileageValLo)/1000 * mileageAdjVal,
                                       "dealer_price":   priceDealerVal + 
                                                         (mileageValAv - mileageValLo)/1000 * mileageAdjVal
                                     },
                    "high_usage":    { "mean_mileage":   mileageValHi,
                                       "trade_in_price": priceTradeinVal +
                                                         (mileageValAv - mileageValHi)/1000 * mileageAdjVal,
                                       "private_price":  pricePrivateVal +
                                                         (mileageValAv - mileageValHi)/1000 * mileageAdjVal,
                                       "dealer_price":   priceDealerVal +
                                                         (mileageValAv - mileageValHi)/1000 * mileageAdjVal
                                     }
                   }

  except:
    pass
  
  return dataPricing

