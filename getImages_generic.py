# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:05:06 2019

@author: Simon
"""

import json
import itertools
import logging
import uuid
from urllib.request import urlopen, Request
import csv
import base64
import os
import sys

from bs4 import BeautifulSoup



def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('[%(asctime)s %(levelname)s %(module)s]: %(message)s'))
    logger.addHandler(handler)
    return logger

logger = configure_logging()

REQUEST_HEADER = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}


def get_soup(url, header):
    response = urlopen(Request(url, headers=header))
    return BeautifulSoup(response, 'html.parser')

def get_query_url(query):
    return "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch" % query

def extract_images_from_soup(soup):
    image_elements = soup.find_all("div", {"class": "rg_meta"})
    metadata_dicts = (json.loads(e.text) for e in image_elements)
    link_type_records = ((d["ou"], d["ity"]) for d in metadata_dicts)
    return link_type_records

def extract_images(query, num_images):
    url = get_query_url(query)
    logger.info("Souping")
    soup = get_soup(url, REQUEST_HEADER)
    logger.info("Extracting image urls")
    link_type_records = extract_images_from_soup(soup)
    return itertools.islice(link_type_records, num_images)


def get_raw_image(url):
    req = Request(url, headers=REQUEST_HEADER)
    resp = urlopen(req)
    return resp.read()

def save_image(raw_image, image_type, save_directory):
    file_name = uuid.uuid4().hex
    save_path = save_directory+"/"+file_name+".jpg" #os.path.join(save_directory, file_name)
    with open(save_path, 'wb') as image_file:
        image_file.write(raw_image)

def download_images_to_dir(images, save_directory, num_images):
    for i, (url, image_type) in enumerate(images):
        print(i)
        try:
            logger.info("Making request (%d/%d): %s", i, num_images, url)
            raw_image = get_raw_image(url)
            save_image(raw_image, image_type, save_directory)
        except Exception as e:
            logger.exception(e)
            
def images_to_b64(images, save_directory, num_images):
    urls=list()
    for i, (url, image_type) in enumerate(images):
        urls.append(url)
        recent_url=urls[i]
        print(recent_url)
        if recent_url[-3:]=='jpg' or recent_url[-4:]=='jpeg':
            try:
                logger.info("Making request (%d/%d): %s", i, num_images, recent_url)
                raw_image = get_raw_image(recent_url)
                img_size=sys.getsizeof(raw_image)
                
                if img_size < 250000:
                
                    image = base64.b64encode(raw_image)
                    
                    image_string=str(image)
                    image_string=image_string[2:-1]
                    image_string="data:image/jpeg;base64,"+image_string
                    
                    image_name=str(i)+".txt"
                    f=open(save_directory + "/" + image_name,"w")
                    
                    f.write(image_string)
                    f.close()
                
            except Exception as e:
                logger.exception(e)


def run(query, save_directory, num_images=10):
    query = '+'.join(query.split())
    logger.info("Extracting image links")
    images = extract_images(query, num_images)
    logger.info("Downloading images")
    images_to_b64(images, save_directory, num_images)
    logger.info("Finished")



csv_name='locations'

with open(csv_name+'.csv', 'r', encoding='utf-8-sig') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        id=row[0]
        type=row[1]
        title=row[2]
        subtitle=row[3]
        description=row[4]
        latitude=row[5]
        longitude=row[6]
        
        search_query="cityname "+title        
        search_query=search_query.replace("ä","ae")
        search_query=search_query.replace("Ä","Ae")
        search_query=search_query.replace("ö","oe")
        search_query=search_query.replace("Ö","Oe")
        search_query=search_query.replace("ü","ue")
        search_query=search_query.replace("Ü","Ue")
        search_query=search_query.replace("é","e")
        search_query=search_query.replace("ù","u")
        search_query=search_query.replace("ß","ss")
        
        img_path="img/"+id
        img_folder="C:/Users/.../img/" + id
        
        if not os.path.isdir(img_path):
            os.mkdir(img_path)
            run(search_query, img_folder, 3)
        else:
            if not os.listdir(img_path):
                print(id) 
                #run(search_query, img_folder, 20)
        
        
csvFile.close()