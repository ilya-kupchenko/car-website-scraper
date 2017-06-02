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

from no_survey import no_survey

from exceptor_lib import ex_list_search   
from exceptor_lib import ex_list_length   
from exceptor_lib import ex_list_clicknum 
from exceptor_lib import ex_read_list     
from exceptor_lib import ex_click_tag     
from exceptor_lib import ex_read_fcol     
from exceptor_lib import ex_1re           
from exceptor_lib import ex_2re           
from exceptor_lib import ex_int_1re       
from exceptor_lib import ex_int_2re       
from exceptor_lib import ex_float_1re     
from exceptor_lib import ex_float_2re     
from exceptor_lib import ex_float_attr    
from exceptor_lib import ex_bool          
from exceptor_lib import ex_int_text_1re  
from exceptor_lib import ex_int_text_2re  
from exceptor_lib import ex_float_text_1re
from exceptor_lib import ex_float_text_2re
from exceptor_lib import ex_text_2re      
from exceptor_lib import ex_text_1re      
from exceptor_lib import ex_bool_text     
from exceptor_lib import ex_safe_text     

import time
import json


def get_units(driver, string, val_num = 1):

  parShort = "Not available"

  try:
    if (val_num == 1):

      stringCut = re.search("^\d{1,}[.]{0,1}\d{0,}[ ][A-Za-z.-]{1,}", string).group()
      parShort  = re.search("[A-Za-z.-]{1,}$", stringCut).group()

    elif (val_num == 2):

      stringCut = re.search("\d{1,}[.]{0,1}\d{0,}[ ][A-Za-z.-]{1,}$", string).group()
      parShort  = re.search("[A-Za-z.-]{1,}$", stringCut).group()
  except:
    pass
  
  return parShort

def get_highlights(driver):

  dataHighlights = { "fuel_economy_city": 0,
                     "fuel_economy_highway": 0,
                     "car_type": None,
                     "transmission_type": None,
                     "transmission_nspeeds": None,
                     "basic_warranty_years": 0,
                     "basic_warranty_miles": 0,
                     "bluetooth": False,
                     "heated_seats": False,
                     "engine_type": None,
                     "total_seating": 0,
                     "cylinders": 0,
                     "drive_train": None,
                     "consumer_rating": 0,
                     "navigation": False
                   }
  

 
  
  dataHighlights["fuel_economy_city"] = \
    ex_int_2re(driver, \
    '//*[@id="highlights-pod"]/div/div[2]/ul[1]/li[1]/em/a', \
    "\d{1,3}", "\d{1,3}[/]") 

  dataHighlights["fuel_economy_highway"] = \
    ex_int_2re(driver, \
    '//*[@id="highlights-pod"]/div/div[2]/ul[1]/li[1]/em/a', \
    "\d{1,3}", "[/]\d{1,3}") 

  dataHighlights["car_type"] =ex_safe_text(driver, \
    '//*[@id="highlights-pod"]/div/div[2]/ul[1]/li[2]/em')

  dataHighlights["transmission_nspeeds"] = ex_int_1re(driver,\
  '//*[@id="highlights-pod"]/div/div[2]/ul[1]/li[3]/em',"\d{1}")

  try:
    transText = driver.find_element_by_xpath( \
      '//*[@id="highlights-pod"]/div/div[2]/ul[1]/li[3]/em').text  
    if (re.search("Automatic", transText)):
      dataHighlights["transmission_type"] = "Automatic"
    elif (re.search("Manual", transText)):
      dataHighlights["transmission_type"] = "Manual"
    else:
      dataHighlights["transmission_type"] = "Not Available"
  except:
    dataHighlights["transmission_type"] = "Not Available"

  dataHighlights["basic_warranty_years"] = ex_int_2re(driver, \
    '//*[@id="highlights-pod"]/div/div[2]/ul[1]/li[4]/em', \
    "\d", "\d.Yr")

  dataHighlights["basic_warranty_miles"] = ex_text_2re(driver, \
      '//*[@id="highlights-pod"]/div/div[2]/ul[1]/li[4]/em',
      "\d{1,}", "\d{1,}.Mi")

  dataHighlights["bluetooth"] = ex_bool(driver, \
    '//*[@id="highlights-pod"]/div/div[2]/ul[1]/li[5]/em')

  dataHighlights["heated_seats"] = ex_bool(driver, \
    '//*[@id="highlights-pod"]/div/div[2]/ul[1]/li[6]/em')

  dataHighlights["engine_type"] = ex_safe_text(driver, \
    '//*[@id="highlights-pod"]/div/div[2]/ul[2]/li[1]/em')
  
  dataHighlights["total_seating"] = ex_int_1re(driver, \
    '//*[@id="highlights-pod"]/div/div[2]/ul[2]/li[2]/em',
    '\d')

  dataHighlights["cylinders"] = ex_int_1re(driver, \
  '//*[@id="highlights-pod"]/div/div[2]/ul[2]/li[3]/em', \
  "\d{1,2}")

  dataHighlights["drive_train"] = ex_safe_text(driver, \
    '//*[@id="highlights-pod"]/div/div[2]/ul[2]/li[4]/em')

  dataHighlights["consumer_rating"] = ex_float_attr(driver, \
    '//*[@id="highlights-pod"]/div/div[2]/ul[2]/li[5]/em/a/span',
    'title')
  dataHighlights["navigation"] = ex_bool(driver, \
    '//*[@id="highlights-pod"]/div/div[2]/ul[2]/li[6]/em')
 
  return dataHighlights

def get_colors(driver):

    dataColors = []
    dataExteriorColors = { "Exterior_Colors"   : [] }
    dataInteriorColors = { "Interior_Colors"   : [] }
  
    try:
      colorsTitle = driver.find_element_by_xpath('//*[@id="colors-pod"]/div/div[1]/h2') 
      try:
        colorExteriorTags = driver.find_elements_by_xpath('//*[@id="bean-container"]/span/span[3]')
        nExteriorColors = len(colorExteriorTags)  

        if (nExteriorColors > 0):
            
            for colorTag in colorExteriorTags:
              exterMetallic = False
              try:
                colorKey = re.sub('[^A-Za-z ]','',colorTag.text)
                colorKey = re.sub('[ ]', '_', colorKey)
                try:
                  if(re.search("Metallic", colorTag.text)):
                    exterMetallic = True
                except:
                  pass
                if(colorKey != ''):
                  dataExteriorColors["Exterior_Colors"].append({ colorKey: \
                  {"Color_Name": colorTag.text, "Metallic": exterMetallic }})
              except:
                pass
            dataColors.append(dataExteriorColors)
        else:
            dataExteriorColors["Exterior_Colors"] =  "Not available"
            dataColors.append(dataExteriorColors) 
      except:
        dataExteriorColors["Exterior_Colors"] =  "Not available"
        dataColors.append(dataExteriorColors) 

      try:
        colorInteriorTags = driver.find_elements_by_xpath( \
              '//*[@id="interior_colors"]/span/span[3]')
        nInteriorColors = len(colorInteriorTags)  

        if (nInteriorColors > 0):

            for colorTag in colorInteriorTags:
              try:

                colorKey = re.sub('[^A-Za-z ]', '', colorTag.text)
                colorKey = re.sub('[ ]', '_', colorKey)

                interColorName = re.search("[A-Za-z ]{1,}", \
                re.search("[A-Za-z ()]{1,}[,]", \
                colorTag.text).group()).group()
 
                interColorMaterial = re.search( \
                "[A-Za-z][A-Za-z ]{1,}[A-Za-z]", \
                re.search("[,].[A-Za-z ]{1,}", \
                colorTag.text).group()).group()
 
                dataInteriorColors["Interior_Colors"].append({ \
                colorKey: { "color_name":interColorName, \
                "interior_material":interColorMaterial }})
              except:
                pass
            dataColors.append(dataInteriorColors) 
        else:
            dataInteriorColors["Interior_Colors"] = "Not Available"
            dataColors.append(dataInteriorColors)
      except:
        dataInteriorColors["Interior_Colors"] = "Not Available"
        dataColors.append(dataInteriorColors)
    except:
      dataColors = "Not available"

    return dataColors

def get_specifications(driver):

  dataSpecifications = []
  dataExteriorMeasurements = {"exterior_measurements": []}
  dataInteriorMeasurements = {"interior_measurements": []}
  dataFuel                 = {"fuel": []}
  dataWeightsCapacities    = {"weights_and_capacities": []}
  dataDrivetrain           = {"drive_train": []}
  dataEnginePerformance    = {"engine_performance":[]}
  dataSuspension           = {"suspension": []}
  dataWarranty             = {"warranty": []}

  try:
    specificationsHeaders = driver.find_elements_by_xpath( \
      '//*[@id="specification-pod"]/div/div[2]/h3')
    specificationsTables  = driver.find_elements_by_xpath( \
      '//*[@id="specification-pod"]/div/div[2]/table')

    for header, table in zip(specificationsHeaders, specificationsTables):
    
      if (header.text == 'Exterior Measurements'):
        try:
          exteriorMeasurementsTag = driver.find_element_by_xpath( \
          '//*[@id="specification-pod"]/div/div[2]/h3'+\
          '[contains(text(),"Exterior Measurements")]')

          if (exteriorMeasurementsTag):
            measurementsTags = table.find_elements_by_xpath( \
              './tbody/tr/td/label')
            valuesTags = table.find_elements_by_xpath( \
              './tbody/tr/td/span')
            nMeasurments = len(measurementsTags)

            if(nMeasurments > 0):
              for measurementTag, valueTag  in zip(measurementsTags, valuesTags):
                try:
                  measurementKey = re.sub('[^A-Za-z ]', '', measurementTag.text)
                  measurementKey = re.sub('[ ]', '_', measurementKey)
                  dataExteriorMeasurements["exterior_measurements"].append({ \
                    measurementKey: {"measure_name": measurementTag.text, \
                    "measure_value_feet": int(re.search("^\d{1,2}", valueTag.text).group()), \
                    "measure_value_inches": float(re.search("\d{1,2}[.]{0,1}\d{0,1}", \
                    re.search("ft[.][ ]\d{1,2}[.]{0,1}\d{0,1}[ ]in", \
                    valueTag.text).group()).group()),
                    "measure_value_total_inches": float(re.search("\d{1,2}[.]{0,1}[\d]{0,1}", \
                    re.search("[(]\d{1,3}[.]{0,1}[\d]{0,1}[ ]in[.][)]$", \
                    valueTag.text).group()).group()) }})
                except:
                  pass
              dataSpecifications.append(dataExteriorMeasurements)
        except:
              dataSpecifications.append({'exterior_measurements': 'Not available'})

      elif (header.text == 'Interior Measurements'):
        try:
          interiorMeasurementsTag = driver.find_element_by_xpath( \
            '//*[@id="specification-pod"]/div/div[2]/h3[contains(text(),"Interior Measurements")]')

          if (interiorMeasurementsTag):
            measurementsTags = table.find_elements_by_xpath( \
              './tbody/tr/td/label')
            valuesTags = table.find_elements_by_xpath( \
              './tbody/tr/td/span')
            nMeasurments = len(measurementsTags)

            if(nMeasurments > 0):
              for measurementTag, valueTag  in zip(measurementsTags, valuesTags):
                try:
                  measurementKey = re.sub('[^A-Za-z ]', '', measurementTag.text)
                  measurementKey = re.sub('[ ]', '_', measurementKey)
                  dataInteriorMeasurements["interior_measurements"].append({ \
                    measurementKey:{"measure_name": measurementTag.text, \
                    "measure_value_inches": float(re.search("^\d{1,3}[.]{0,1}[\d]{0,1}", \
                    valueTag.text).group())
                    }})
                except:
                  pass
              dataSpecifications.append(dataInteriorMeasurements)
        except:
          dataSpecifications.append({"interior_measurements" : "Not available"})

      elif (header.text == 'Fuel'):
        try:
          interiorMeasurementsTag = driver.find_element_by_xpath( \
            '//*[@id="specification-pod"]/div/div[2]/h3[contains(text(),"Fuel")]')

          if (interiorMeasurementsTag):
            measurementsTags = table.find_elements_by_xpath( \
              './tbody/tr/td/label')
            valuesTags = table.find_elements_by_xpath( \
              './tbody/tr/td/span')
            nMeasurments = len(measurementsTags)

            if(nMeasurments > 0):
              for measurementTag, valueTag  in zip(measurementsTags, valuesTags):
                try:
                  measurementKey = re.sub('[^A-Za-z ]', '', measurementTag.text)
                  measurementKey = re.sub('[ ]', '_', measurementKey)
                  if (measurementTag.text == 'ENGINE TYPE'):
                    dataFuel["fuel"].append({ \
                      measurementKey : {
                      "specification_name": measurementTag.text, \
                      "specification_value": valueTag.text }})
                  if (measurementTag.text == 'FUEL TANK CAPACITY'):
                    
                    dataFuel["fuel"].append({ \
                      measurementKey : {
                      "specification_name": measurementTag.text, \
                      "specification_value": float(re.search("^\d{1,3}[.]{0,1}[\d]{0,1}", \
                      valueTag.text).group()),
                      "units": get_units(driver, valueTag.text)}})
                  if (measurementTag.text == 'EPA MILEAGE EST. (CTY/HWY)'):
                    dataFuel["fuel"].append({ \
                      measurementKey : {
                      "specification_name": 'EPA MILEAGE EST. CTY', \
                      "specification_value": int(re.search("^\d{1,3}", \
                      valueTag.text).group()),
                      "units": get_units(driver, valueTag.text, 2) } })
                    dataFuel["fuel"].append({ \
                      measurementKey : {
                      "specification_name": 'EPA MILEAGE EST. HWY', \
                      "specification_value": int(re.search("[/]\d{1,3}", \
                      valueTag.text).group().replace('/','')),
                      "units": get_units(driver, valueTag.text, 2) }})
                  if (measurementTag.text == 'FUEL TYPE'):
                    dataFuel["fuel"].append({ \
                      measurementKey : {
                      "specification_name": measurementTag.text, \
                      "specification_value": valueTag.text }})
                  if (measurementTag.text == 'RANGE IN MILES (CTY/HWY)'):
                    dataFuel["fuel"].append({ \
                      measurementKey : {
                      "specification_name": 'RANGE IN MILES CTY', \
                      "specification_value": float(re.search("^\d{1,3}", \
                      valueTag.text).group()),
                      "units": get_units(driver, valueTag.text, 2) }})
                    dataFuel["fuel"].append({ \
                      measurementKey : {
                      "specification_name": 'RANGE IN MILES HWY', \
                      "specification_value": float(re.search("[/]\d{1,3}", \
                      valueTag.text).group().replace('/','')),
                      "units": get_units(driver, valueTag.text, 2) }})  
                except:
                  pass 

              dataSpecifications.append(dataFuel)
        except:
          dataSpecifications.append({"fuel": "Not available"})
          dataSpecifications.append(dataFuel)

      elif (header.text == 'Weights and Capacities'):
        try:
          interiorMeasurementsTag = driver.find_element_by_xpath( \
            '//*[@id="specification-pod"]/div/div[2]/h3[contains(text(),"Weights and Capacities")]')

          if (interiorMeasurementsTag):
            measurementsTags = table.find_elements_by_xpath( \
              './tbody/tr/td/label')
            valuesTags = table.find_elements_by_xpath( \
              './tbody/tr/td/span')
            nMeasurments = len(measurementsTags)

            if(nMeasurments > 0):
              for measurementTag, valueTag  in zip(measurementsTags, valuesTags):
                try:
                  measurementKey = re.sub('[^A-Za-z ]', '', measurementTag.text)
                  measurementKey = re.sub('[ ]', '_', measurementKey)   
                  if (measurementTag.text == 'MAXIMUM TOWING CAPACITY**' or \
                     measurementTag.text == 'GROSS WEIGHT' or \
                     measurementTag.text == 'CURB WEIGHT' or \
                     measurementTag.text == 'MAXIMUM PAYLOAD**'  ):
                       dataWeightsCapacities["weights_and_capacities"].append({ \
                       measurementKey: {
                      "specification_name": measurementTag.text, \
                      "specification_value": int(re.search('\d{1,}', valueTag.text).group()),
                      "units": get_units(driver, valueTag.text) }})
                  elif ( measurementTag.text == 'ANGLE OF DEPARTURE' or \
                        measurementTag.text == 'MAXIMUM CARGO CAPACITY' or \
                        measurementTag.text == 'DRAG COEFFICIENT' or \
                        measurementTag.text == 'ANGLE OF APPROACH' or \
                        measurementTag.text == 'CARGO CAPACITY, ALL SEATS IN PLACE'):
                          dataWeightsCapacities["weights_and_capacities"].append({ \
                         measurementKey: {
                         "specification_name": measurementTag.text, \
                         "specification_value": float(re.search('\d{1,}[.]{1,}\d{1,}', \
                                                valueTag.text).group()),
                         "units": get_units(driver, valueTag.text) }})
                except:
                  pass
              dataSpecifications.append(dataWeightsCapacities)
        except:
          dataSpecifications.append({"weights_and_capacities": "Not available"})

      elif (header.text == 'DriveTrain'):
        try:
          interiorMeasurementsTag = driver.find_element_by_xpath( \
            '//*[@id="specification-pod"]/div/div[2]/h3[contains(text(),"DriveTrain")]')

          if (interiorMeasurementsTag):
            measurementsTags = table.find_elements_by_xpath( \
              './tbody/tr/td/label')
            valuesTags = table.find_elements_by_xpath( \
              './tbody/tr/td/span')
            nMeasurments = len(measurementsTags)

            if(nMeasurments > 0):
              for measurementTag, valueTag  in zip(measurementsTags, valuesTags):
                try:
                  measurementKey = re.sub('[^A-Za-z ]', '', measurementTag.text)
                  measurementKey = re.sub('[ ]', '_', measurementKey)
                  dataDrivetrain["drive_train"].append({ \
                    measurementKey : {
                    "specification_name": measurementTag.text, \
                    "specification_value": valueTag.text }})
                except:
                  pass
              dataSpecifications.append(dataDrivetrain)
        except:
          dataSpecifications.append({"drive_train" : "Not available"})

      elif (header.text == 'Engine & Performance'):
        try:
          interiorMeasurementsTag = driver.find_element_by_xpath( \
            '//*[@id="specification-pod"]/div/div[2]/h3[contains(text(),"Engine & Performance")]')

          if (interiorMeasurementsTag):
            measurementsTags = table.find_elements_by_xpath( \
              './tbody/tr/td/label')
            valuesTags = table.find_elements_by_xpath( \
              './tbody/tr/td/span')
            nMeasurments = len(measurementsTags)

            if(nMeasurments > 0):
              for measurementTag, valueTag  in zip(measurementsTags, valuesTags):
                try:
                  measurementKey = re.sub('[^A-Za-z ]', '', measurementTag.text)
                  measurementKey = re.sub('[ ]', '_', measurementKey)
                  if(measurementTag.text == 'CYLINDERS' or \
                     measurementTag.text == 'VALVES' ):
                     dataEnginePerformance["engine_performance"].append({ \
                       measurementKey : {
                       "specification_name":  measurementTag.text, \
                       "specification_value": int(re.search('\d{1,}', \
                        valueTag.text).group()) }})
                  if(measurementTag.text == 'TURNING CIRCLE'):
                    dataEnginePerformance["engine_performance"].append({ \
                       measurementKey : {
                       "specification_name":  measurementTag.text, \
                       "specification_value": int(re.search('\d{1,}', valueTag.text).group()), \
                       "units": get_units(driver, valueTag.text) }})
                  if(measurementTag.text == 'HORSEPOWER'):
                      dataEnginePerformance["engine_performance"].append({ \
                       measurementKey : {
                       "specification_name":  measurementTag.text, \
                       "specification_value": int(re.search('\d{1,}', valueTag.text).group()), \
                       "units": get_units(driver, valueTag.text) }})
                  if(measurementTag.text == 'TORQUE'):
                      dataEnginePerformance["engine_performance"].append({ \
                       measurementKey : {
                       "specification_name":  measurementTag.text, \
                       "specification_value": int(re.search('\d{1,}', valueTag.text).group()), \
                       "units": get_units(driver, valueTag.text) }})
                  if(measurementTag.text == 'VALVE TIMING' or \
                     measurementTag.text == 'CAM TYPE'  ):
                      dataEnginePerformance["engine_performance"].append({ \
                       measurementKey : {
                       "specification_name":  measurementTag.text, \
                       "specification_value": valueTag.text }})
                except:
                  pass

              dataSpecifications.append(dataEnginePerformance)
        except:
          dataSpecifications.append({"engine_performance":"Not available"})


      elif (header.text == 'Suspension'):
        try:
          interiorMeasurementsTag = driver.find_element_by_xpath( \
            '//*[@id="specification-pod"]/div/div[2]/h3'+\
            '[contains(text(),"Engine & Performance")]')

          if (interiorMeasurementsTag):
            measurementsTags = table.find_elements_by_xpath( \
              './tbody/tr/td/ul/li/span')
            nMeasurments = len(measurementsTags)

            if(nMeasurments > 0):
              for measurementTag  in measurementsTags:
                measurementKey = re.sub('[^A-Za-z ]', '', measurementTag.text)
                measurementKey = re.sub('[ ]', '_', measurementKey)
                try:
                  dataSuspension["suspension"].append({ \
                      measurementKey: {
                      "suspension_type":  measurementTag.text}})
                except:
                  pass
              dataSpecifications.append(dataSuspension)
        except:
           dataSpecifications.append({"suspension": "Not available"})

      elif (header.text == 'Warranty'):
        try:
          interiorMeasurementsTag = driver.find_element_by_xpath( \
            '//*[@id="specification-pod"]/div/div[2]/h3[contains(text(),"Warranty")]')

          if (interiorMeasurementsTag):
            measurementsTags = table.find_elements_by_xpath( \
              './tbody/tr/td/label')
            valuesTags = table.find_elements_by_xpath( \
              './tbody/tr/td/span')
            nMeasurments = len(measurementsTags)

            if(nMeasurments > 0):
              for measurementTag, valueTag  in zip(measurementsTags, valuesTags):
                try:
                  measurementKey = re.sub('[^A-Za-z ]', '', measurementTag.text)
                  measurementKey = re.sub('[ ]', '_', measurementKey)
                  dataWarranty["warranty"].append({ \
                   measurementKey: {
                   
                   "specification_name":  measurementTag.text.lower().replace(" ", "_") + "_years", \
                   "specification_value": int(re.search("\d", re.search('\d{1} yr', \
                     valueTag.text).group()).group()) }})
                  dataWarranty["warranty"].append({ \
                   measurementKey : {
                   "specification_name":  measurementTag.text.lower().replace(" ", "_") + "_miles", \
                   "specification_value": int(re.search("\d{1,}", re.search('[/][ ]\d{1,}', \
                     valueTag.text).group()).group()) } })
                except:
                  pass


              dataSpecifications.append(dataWarranty)
        except:
          dataSpecifications.append({"warranity":"Not avalable"})
  except:
    dataSpecifications = "Not available"
  
  return dataSpecifications

def get_equipment(driver):

  try:

    dataEquipment = {"equipment": []}

    equipMainHeaders = driver.find_elements_by_xpath('//div[contains(@class, "feature-spec box")]/h3[1]')
    equipMainHeadersLength = len(equipMainHeaders)

    i = 1

    while i < equipMainHeadersLength:

      try:

        equipMainHeader = equipMainHeaders[i]
        equipMainHeaderText = equipMainHeader.text
        equipMainHeaderKey = \
        equipMainHeaderText.lower().replace(' ', '_').replace('features', 'equipment')

        equipInterior = {equipMainHeaderKey: []}

        if (equipMainHeaderText != "Safety Features"): 

          equipSubContainerHeaders = driver.find_elements_by_xpath( \
            '//div[contains(@class, "feature-spec box")]/h3' + \
            '[contains(text(), "' + equipMainHeaderText + '")]/parent::*/h4')
          equipSubContainerTables  = driver.find_elements_by_xpath( \
            '//div[contains(@class, "feature-spec box")]/h3' + \
            '[contains(text(), "' + equipMainHeaderText + '")]/parent::*/table')
          
          equipSubContainersLength = len(equipSubContainerTables)

          j = 0

          while j < equipSubContainersLength:
            try:

              subHeaderString = equipSubContainerHeaders[j].text.lower().replace(' ', '_') 
              equipInteriorSub = {subHeaderString: []}

              tableContentsTags = driver.find_elements_by_xpath( \
                  '//div[contains(@class, "feature-spec box")]/h3' +\
                  '[contains(text(), "' + equipMainHeaderText + '")]/parent::*/table[' + \
                  str(j+1) + ']/tbody/tr/td/ul/li/span')
              tableContentsLength = len(tableContentsTags)
              k = 0

              if( driver.find_elements_by_xpath( \
                '//div[contains(@class, "feature-spec box")]/h3' +\
                '[contains(text(), "' + equipMainHeaderText + '")]/parent::*/table[' + \
                str(j+1) + ']/tbody/tr/td/ul/li/span') ):

                while k < tableContentsLength:
                  try:
                    tableTagText = tableContentsTags[k].text
                    equipInteriorSub[subHeaderString].append({"equipment_item":tableTagText})
                    k += 1
                  except:
                    pass       
              equipInterior[equipMainHeaderKey].append(equipInteriorSub)
            except:
              pass
            j += 1
          dataEquipment["equipment"].append(equipInterior)

        else:
          try:
            equipSubContainerTable  = driver.find_element_by_xpath( \
              '//div[contains(@class, "feature-spec box")]/h3' + \
              '[contains(text(), "' + equipMainHeaderText + '")]/parent::*/table')
            equipMainHeaderKey = \
              equipMainHeaderText.lower().replace(' ', '_').replace('features', 'equipment')
            equipInterior = {equipMainHeaderKey: []}

            if( driver.find_elements_by_xpath( \
                '//div[contains(@class, "feature-spec box")]/h3' +\
                '[contains(text(), "' + equipMainHeaderText + \
                '")]/parent::*/table/tbody/tr/td/ul/li/span') ):

              tableContentsTags = driver.find_elements_by_xpath( \
                '//div[contains(@class, "feature-spec box")]/h3' +\
                '[contains(text(), "' + equipMainHeaderText + \
                '")]/parent::*/table/tbody/tr/td/ul/li/span')

              tableContentsLength = len(tableContentsTags)
              k = 0

              while k < tableContentsLength:
                try:

                  tableTagText = tableContentsTags[k].text
                  equipInterior[equipMainHeaderKey].append({"equipment_item":tableTagText})
                  k += 1
                except:
                  pass
              
              dataEquipment["equipment"].append(equipInterior)
          except: 
            pass
      except:
        pass   
      i += 1

    return dataEquipment
  except:
    dataEquipment["equipment"] = "Not available"

def get_specs(driver):
  try:
    dataFeatures = { "Highlights": "Not available",
                   "Features":   {"Colors" : [],
                                  "Specifications" : [],
                                  "Equipment" : []} }
  
    dataFeatures["Highlights"]                         = get_highlights(driver)
    dataFeatures["Features"]["Colors"]                 = get_colors(driver)
    dataFeatures["Features"]["Specifications"]  = get_specifications(driver)
    dataFeatures["Features"]["Equipment"]       = get_equipment(driver)
    return dataFeatures
  except:
    return "Not available"
