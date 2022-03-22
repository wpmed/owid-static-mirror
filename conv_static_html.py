#!/usr/bin/python3
import os
import glob
#import copy
#import json
#import re
import string
import argparse
#from urllib.parse import urljoin, urldefrag, urlparse
#import requests
from bs4 import BeautifulSoup
#import youtube_dl
#from icu import UnicodeString, Locale
# from basicspider.sp_lib import *

SOURCE_DIR = '/srv/repos/owid-static/grapher/'
DEST_DIR = '/srv/www/html/grapher/'
SOURCE_HOST = 'ourworldindata.org'
DEST_HOST = 'owidm.wmcloud.org'

# for test
u1 = 'interventions-ntds-sdgs.html'
u2 = 'share-of-population-with-schizophrenia.html'
u3 = 'share-of-adults-defined-as-obese.html'
u4 = 'asthma-prevalence.html'

def main():
    file_list = get_grapher_page_list()
    for f in file_list:
        do_page(os.path.basename(f))
        pass

def get_grapher_page_list():
    file_list = glob.glob(SOURCE_DIR + '*.html')
    return file_list

def do_page(file_name):
    page = get_page(file_name)
    page = change_host(page)
    page = mod_scripts(page)
    head_lines = BeautifulSoup(get_head_lines(), 'html.parser')
    page.head.append(head_lines)
    bottom_lines = BeautifulSoup(get_bottom_lines(), 'html.parser')
    page.body.append(bottom_lines)
    output_converted_page(page, file_name)

def get_page(file_name):
    inp_file = SOURCE_DIR + file_name
    html = read_html_file(inp_file)
    page = BeautifulSoup(html, "html5lib")
    return page

def change_host(page):
    href_tags = page.find_all(href=True)
    content_tags = page.find_all(content=True)
    src_tags = page.find_all(src=True)
    for tag in href_tags:
        tag['href'] = tag['href'].replace(SOURCE_HOST, DEST_HOST)
    for tag in content_tags:
        tag['content'] = tag['content'].replace(SOURCE_HOST, DEST_HOST)
    #for tag in src_tags:
    #    tag['src'] = tag['src'].replace(SOURCE_HOST, DEST_HOST)
    # using owidm for vendor.js and owid.js causes image to hang
    return page

def mod_scripts(page):
    scripts = page.find_all('script')
    scripts[-1].string = scripts[-1].text.replace('window.Grapher.', '// window.Grapher.')
    scripts[-3]['src'] = 'https://owidm.wmcloud.org/assets/owid.js'
    scripts[-4]['src'] = 'https://owidm.wmcloud.org/assets/vendors.js'
    scripts[-5]['src'] = 'https://owidm.wmcloud.org/assets/commons-mods.js'
    #scripts[-3]['src'] = scripts[-3]['src'].replace(SOURCE_HOST, DEST_HOST)
    #scripts[-5]['src'] = scripts[-5]['src'].replace(SOURCE_HOST, DEST_HOST)
    return page

def read_html_file(input_file_path):
    with open(input_file_path, 'r') as f:
        text = f.read()
    return text

def output_converted_page(page, page_file_name):
    html_output = page.encode_contents(formatter='html')
    output_file_name = DEST_DIR + page_file_name
    write_conv_html_file(output_file_name, html_output)
    print(output_file_name)

def write_conv_html_file(output_file_name, html_output):
    output_dir = os.path.dirname(output_file_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_file_name, 'wb') as f:
        f.write(html_output)

def get_head_lines():
    head_lines = '''
    <link rel="stylesheet" href="/assets/map-mixer.css">
    '''
    return head_lines

def get_bottom_lines():
    bottom_lines = '<script src="https://' + DEST_HOST + '/assets/map-mixer.js"></script>'
    bottom_lines += '''
    <script>
    var jsonConfigCC;
    if (jsonConfigCC == undefined){
        jsonConfigCC = JSON.parse(JSON.stringify(jsonConfig));
        jsonConfig.subtitle = '';
        jsonConfig.note = '';
        jsonConfig.sourceDesc += ', OWID';
        if ('relatedQuestions' in jsonConfig)
            delete jsonConfig.relatedQuestions;
    }
    window.Grapher.renderSingleGrapherOnGrapherPage(jsonConfig)
    mixMaps(jsonConfigCC);
    </script>
    '''
    return bottom_lines

if __name__ == "__main__":
    # place holder for future args
    parser = argparse.ArgumentParser(description="Convert downloaded html. By default downloads asset files")
    parser.add_argument("-n", "--nodownload", help="don't download assets", action="store_true")
    args = parser.parse_args()
    #main(args)
    main()
