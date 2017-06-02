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



def scrap_container_section(mcIndex, chIndex, cNameLNS, hNameLNS, containerHeaderOptions, sectionName, driver, data):
  containerHeaderFeature = containerHeaderOptions.find_element_by_xpath('./ancestor::div[@class="expand options-group-container"]/div/div/span[@class="options-title" and text()="' + sectionName + '"]')

  featureOptions = containerHeaderFeature.find_elements_by_xpath('./parent::div/following-sibling::div[contains(@class,"options-list-data") and preceding-sibling::div[@class="options-list-header"][1]/span[text()="' + sectionName + '"]]')
  driver.execute_script("return arguments[0].scrollIntoView();", featureOptions[0])
  sectionNameLNS = sectionName.lower()
  sectionNameLNS = re.sub("[ ]", "_", sectionNameLNS)
  t = 0
  nFeatures = len(featureOptions)

  for feature in   featureOptions:
    featureName =  feature.find_element_by_xpath('./span[2]/label/strong')
    featureNameText =  re.sub('[^A-Za-z0-9 /-:(),.;]', '', featureName.text)
    featureRadio = feature.find_element_by_xpath('./span[1]/input')
    featureID =    feature.find_element_by_xpath('./span[2]/label').get_attribute("for")
    if (featureRadio.is_selected()):
      data[mcIndex][cNameLNS][chIndex][hNameLNS].append({'option_name':featureNameText, 'option_id': int(re.sub("[^0-9]", "", featureID)), 'default':True})
    else:
      data[mcIndex][cNameLNS][chIndex][hNameLNS].append({'option_name':featureNameText, 'option_id': int(re.sub("[^0-9]", "", featureID)), 'default':False})
    t += 1



def scrap_color_section(mcIndex, dr, optionsColor, sectionName, data):
  colorFeature = optionsColor.find_element_by_xpath('./ancestor::div[@class="expand options-group-container"]/div/div/span[@class="options-title" and text()="' + sectionName + '"]')

  featureOptions = colorFeature.find_elements_by_xpath('./ancestor::div[@class="options-list-header"]/following-sibling::div/div[contains(@class,"options-list-data")]')
  dr.execute_script("return arguments[0].scrollIntoView();", featureOptions[0])
  sectionNameLNS = sectionName.lower()
  sectionNameLNS = re.sub("[ ]", "_", sectionNameLNS)
  #print "\"" + sectionNameLNS + "s\":"
  col = 0
  nFeatures = len(featureOptions)

  #if (nFeatures > 1):
    #print "["

  for feature in   featureOptions:
    featureName =  feature.find_element_by_xpath('./span[2]/label/strong')
    featureNameText =  re.sub('[^A-Za-z0-9 /-:(),.;]', '', featureName.text)
    featureRadio = feature.find_element_by_xpath('./span[1]/input')
    featureID =    feature.find_element_by_xpath('./span[2]/label').get_attribute("for")
    data[mcIndex]["colors"][0]["exterior_color"].append({'option_name':featureNameText, 'option_id': int(re.sub("[^0-9]", "", featureID)), 'default':False})
    #if (col < nFeatures - 1):
      #print ","
    col += 1

  #if (nFeatures > 1):
    #print "]"


def scrape_options(driver):
  data = []
  mainContainerHeaders = driver.find_elements_by_xpath('//*[@id="Options-container"]/div/div[1]/span/strong[text() != "Color"]')
  nMainContainerHeaders = len(mainContainerHeaders)
  mch = 0
  for container in mainContainerHeaders:
    container.click()
    containerName = container.text
    containerNameLNS = containerName.lower()
    containerNameLNS = re.sub("[ ]", "_", containerNameLNS)
    data.append({containerNameLNS:[]}) 
  
    containerHeaders = container.find_elements_by_xpath('./ancestor::div[@class="expand options-group-container"]/div[@class="mod-content expanded-content options-list"]/div[@class="options-list-header"]/span')
   
    nContainerHeaders = len(containerHeaders)
    ch = 0
    for header in containerHeaders:
      headerName = header.text
      headerNameLNS = headerName.lower()
      headerNameLNS = re.sub("[ ]", "_", headerNameLNS)
      data[mch][containerNameLNS].append({headerNameLNS:[]})
      scrap_container_section(mch, ch, containerNameLNS, headerNameLNS, container, header.text, driver, data)
      ch += 1
    mch += 1


  optionsColor =  driver.find_element_by_xpath('//*[@id="Options-container"]/div/div[1]/span/strong[text()="Color"]')
  driver.execute_script("return arguments[0].scrollIntoView();", optionsColor)
  optionsColor.click()
  #print "\"color\"i:"
  data.append({"colors":[]})
  data[mch]["colors"].append({"exterior_color":[]})
  scrap_color_section(mch, driver, optionsColor, 'Exterior Color', data)
  return data
#print 'INDENT:', json.dumps(data, sort_keys=True, indent=2)
