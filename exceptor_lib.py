import sys
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import random
from no_survey import no_survey

def ex_list_search(driver, xpath, string):
  error = True
  renewed = 0 
  rcount = 0
  tmax = [1, 3, 10, 30]
  rmax = len(tmax) - 1
  while (rcount < rmax):
    no_survey(driver)
    tcount = 0
    while (tcount <= tmax[rcount]):
      try:
        listElements = driver.find_elements_by_xpath(xpath)
        listElementsLength = len(listElements)
        if(listElementsLength > 1):
          for element in listElements:
            if(element.text == string):
              element.click()
              error = False
              return error
          return error
      except:
        pass
      if (tcount < tmax[rcount]):
        tcount += 1
        time.sleep(1)
      else:
        tcount += 1
    driver.get(driver.current_url)
    rcount += 1
    renewed = 1       
                
  return error


def ex_list_length(driver, xpath):

  error = True
  rcount = 0
  tmax = [1, 3, 10, 30]
  rmax = len(tmax) - 1

  while (rcount < rmax):
    tcount = 0
    while (tcount <= tmax[rcount]):
      try:
        listElements = driver.find_elements_by_xpath(xpath)
        listElementsLength = len(listElements)
        if(listElementsLength > 1):
          error = False
          return [error, listElementsLength]
      except:
        pass
      if (tcount < tmax[rcount]):
        tcount += 1
        time.sleep(1)
      else:
        tcount += 1
    driver.get(driver.current_url)
    rcount += 1

  return [error, 0]

def ex_list_clicknum(driver, xpath, el_id):

  error = True
  renewed = 0
  reply = ''
  rcount = 0
  tmax = [1, 3, 10, 30]
  rmax = len(tmax) - 1

  while (rcount < rmax):
    tcount = 0
    while (tcount <= tmax[rcount]):
      try:
        listElements = driver.find_elements_by_xpath(xpath)
        listElementsLength = len(listElements)
        if(listElementsLength > 1):
            listElements[el_id].click()
            error = False
            reply = listElements[el_id].text
            return [error, reply]
      except:
        pass
      if (tcount < tmax[rcount]):
        tcount += 1
        time.sleep(1)
      else:
        tcount += 1
    driver.get(driver.current_url)
    rcount += 1

  return [error, reply]

def ex_read_list(driver, xpath, num_els):

  error = True
  reply = []
  rcount = 0
  tmax = [3, 5, 10, 30]
  rmax = len(tmax) - 1

  while (rcount < rmax):
    tcount = 0

    while (tcount <= tmax[rcount]):
      try:
        listElements = driver.find_elements_by_xpath(xpath)
        listElementsLength = len(listElements)
        if (listElementsLength == num_els):

          reply = []
          filled_counter = 0
          for i in range(-1, listElementsLength - 1):

            if (listElements[i].text != ''):
              reply.append(listElements[i].text)
              filled_counter += 1
            else:
              reply.append("Not available") 
          if(filled_counter == num_els):
            error = False
            return [error, reply]
            
      except:
        pass
      if (tcount < tmax[rcount]):
        tcount += 1
        time.sleep(1)
      else:
        tcount += 1
    driver.get(driver.current_url)
    rcount += 1

  if(filled_counter > 0):
    error = False
    return [error, reply]

  return [error, reply]


def ex_click_tag(driver, xpath):

  error = 1
  renewed = 0
  rcount = 0
  tmax = [1, 3, 10, 30]
  rmax = len(tmax) - 1

  while (rcount < rmax):
    tcount = 0
    time.sleep(random.random() * 2 + 1)  
    while (tcount <= tmax[rcount]):
      try:
        target = driver.find_element_by_xpath(xpath)
        target.click()
        error = 0
        return error
      except:
        pass
      if (tcount < tmax[rcount]):
        tcount += 1
        time.sleep(1)
      else:
        tcount += 1
    driver.get(driver.current_url)
    rcount += 1
    renewed = 1

  return [error, renewed]


def ex_read_fcol(driver, nxpath, ixpath, nattr, iattr):
  
  
  error = True
  reply = []
  rcount = 0
  tmax = [1, 3, 10, 30]
  rmax = len(tmax) - 1
  fill_counter = 0

  while (rcount < rmax):
    tcount = 0
    time.sleep(random.random() * 0.5 + 0.5)  
    while (tcount <= tmax[rcount]):
  #    try:
        #print "j0"
        listElementsN = driver.find_elements_by_xpath(nxpath)
        listElementsI = driver.find_elements_by_xpath(ixpath)
        listElementsLengthN = len(listElementsN)
        listElementsLengthI = len(listElementsI)
        #print "I-length: %s" % listElementsLengthI
        #print "N-length: %s" % listElementsLengthN

        if ( listElementsLengthI  > 0 and \
             listElementsLengthI == listElementsLengthN ):
          #print "j2"
          replyi = []
          replyn = []
          for elementi, elementn in zip(listElementsI, listElementsN):
              #print "Nattr : %s" %(elementi.get_attribute(iattr))
              #print "Iattr : %s" %(elementn.get_attribute(nattr))
              replyi.append(elementi.get_attribute(iattr))
              replyn.append(elementn.get_attribute(nattr))
          error = False
          #print  replyi
          #print  replyn
          return [error, replyn, replyi]

        if (tcount < tmax[rcount]):
          tcount += 1
          time.sleep(1)
        else:
          tcount += 1

    driver.get(driver.current_url)
    ex_click_tag(driver, '//*[@id="section-tabs"]/ul/li[2]')
    rcount += 1

  return [error, replyn, replyi]

def ex_1re(driver, xpath, regexp):
  value = "Not available"
  try:
    el = driver.find_element_by_xpath(xpath)
    return re.search(regexp, el.text).group()
  except:
    return value

def ex_2re(driver, xpath, regexp2, regexp1):
  value = "Not available"
  try:
    el = driver.find_element_by_xpath(xpath)
    return re.search(regexp2, re.search(regexp1, el.text).group()).group()
  except:
    return value

def ex_int_1re(driver, xpath, regexp):
  value = "Not available"
  try:
    el = driver.find_element_by_xpath(xpath)
    return int(re.search(regexp, el.text).group())
  except:
    return value

def ex_int_2re(driver, xpath, regexp2, regexp1):
  value = "Not available"
  try:
    el = driver.find_element_by_xpath(xpath)
    return int(re.search(regexp2, re.search(regexp1, el.text).group()).group())
  except:
    return value

def ex_float_1re(driver, xpath, regexp):
  value = "Not available"
  try:
    el = driver.find_element_by_xpath(xpath)
    return float(re.search(regexp, el.text).group())
  except:
    return value

def ex_float_2re(driver, xpath, regexp2, regexp1):
  value = "Not available"
  try:
    el = driver.find_element_by_xpath(xpath)
    return float(re.search(regexp2, re.search(regexp1, el.text).group()).group())
  except:
    return value

def ex_float_attr(driver, xpath, attr):
  value = "Not available"
  try:
    return float(driver.find_element_by_xpath(xpath).get_attribute(attr))
  except:
    return value

def ex_bool(driver, xpath):
  value = "Not available"
  try:
    text = driver.find_element_by_xpath(xpath).text
    if(text == "Yes"):
      return True
    elif(text == "No"):
      return False
  except:
    return value

def ex_int_text_1re(driver, text, regexp):
  value = "Not available"
  try:
    return int(re.search(regexp, text).group())
  except:
    return value

def ex_int_text_2re(driver, text, regexp2, regexp1):
  value = "Not available"
  try:
    return int(re.search(regexp2, re.search(regexp1, text).group()).group())
  except:
    return value

def ex_float_text_1re(driver, text, regexp):
  value = "Not available"
  try:
    return float(re.search(regexp, text).group())
  except:
    return value

def ex_float_text_2re(driver, text, regexp2, regexp1):
  value = "Not available"
  try:
    return float(re.search(regexp2, re.search(regexp1, text).group()).group())
  except:
    return value

def ex_text_2re(driver, text, regexp2, regexp1):
  value = "Not available"
  try:
    return re.search(regexp2, re.search(regexp1, text).group()).group()
  except:
    return value

def ex_text_1re(driver, text, regexp):
  value = "Not available"
  try:
    return re.search(regexp, text).group()
  except:
    return value

def ex_bool_text(driver, text):
  value = "Not available"
  try:
    if(text == "Yes"):
      return True
    elif(text == "No"):
      return False
  except:
    return value

def ex_safe_text(driver, xpath):
  value = "Not available"
  try:
    return driver.find_element_by_xpath(xpath).text
  except:
    return value
