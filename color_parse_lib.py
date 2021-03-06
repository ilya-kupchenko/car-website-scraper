#!/usr/bin/env python

import re
import webcolors

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
    return closest_name

def parse_color_string(styleString):

  error = True

  rnumex = r"rgb[(][0-9]{1,3}"
  gnumex = r"[,][ ][0-9]{1,3}[,]"
  bnumex = r"[0-9]{1,3}[)][;]$"
  num    = r"[0-9]{1,3}"

  try:
    matchLineRed = re.search(rnumex, styleString)
    matchLineGreen = re.search(gnumex, styleString)
    matchLineBlue = re.search(bnumex, styleString)
    numb =  re.search(num, matchLineBlue.group()).group()
    numr =  re.search(num, matchLineRed.group()).group()
    numg =  re.search(num, matchLineGreen.group()).group()
    requested_colour = (int(numr), int(numg), int(numb))
    closest_name = get_colour_name(requested_colour)
  except:
    return [error, '']

  error = False
  return [error, closest_name]
