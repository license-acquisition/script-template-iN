# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 00:16:40 2015

@author: eto
"""

import requests, re
from bs4 import BeautifulSoup as soupify

def main():
    soup = soupify(requests.get('http://www.lni.wa.gov/Safety/Topics/AtoZ/Asbestos/contractorlist.asp').content)
    trs = soup.find_all('tr')
    info = {}
    num = 0
    for tr in trs:
        pair = {}
        row = tr.text.replace('\n', '  ').replace('\t', '  ').replace('\r', '  ')
        pair[num] = [x.strip() for x in row.split('  ') if x != '']
        info[num] = pair
        num += 1
    return info

def zipcode(data):
    try:
        data = data.replace(u'\xa0','')
        regex = re.findall('^[A-Za-z].+, .{2} ([0-9]{5})', data)
    except:
        pass
    return regex
    
def address1(data):
    data = data.lower()
    try:
        regex = re.findall('.*[0-9]*nd *.', data)
    except: pass
    try:
        regex = re.findall('.*[0-9]*st *.', data)
    except: pass
    try:
        regex = re.findall('.*[0-9]*rd *.', data)
    except: pass
    return regex

# make these a class
class RegexParser(object):
    def address1(self):
        self = self.lower()
        try:
            regex = re.findall('.*[0-9]*nd .*', self)
        except: pass
        try:
            regex = re.findall('.*[0-9]*st .*', self)
        except: pass
        try:
            regex = re.findall('.*[0-9]*rd .*', self)
        except: pass
        return regex
        
    def zipcode(self):
        try:
            self.replace(u'\xa0','')
            regex = re.findall('^[A-Za-z].+, .{2} ([0-9]{5})', self)
        except:
            pass
        return regex