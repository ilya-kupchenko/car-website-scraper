#!/usr/bin/env python
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

def no_survey(driver):
  time.sleep(random.random() * 0.2 + 0.2)  
  tcount = 0
  reloaded = False
  while (True):
    if (tcount < 10):
      tcount += 1
      time.sleep(random.random() * 0.2 + 0.1)  
      try:
        driver.find_element_by_xpath('//*[@id="make_item"]/span[1]').click()
        time.sleep(0.01)
        driver.find_element_by_xpath('//*[@id="make_item"]/span[1]').click()
        break
      except:
        continue
    else:
      tcount = 0
      driver.get(driver.current_url)
  return reloaded 
