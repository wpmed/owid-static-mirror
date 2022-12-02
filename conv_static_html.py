#!/usr/bin/python3
from fileinput import filename
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

SOURCE_DIR = '/srv/repos/owid-static/'
SOURCE_DATE = 'November 30, 2022'
SOURCE_HOST = 'ourworldindata.org'

DEST_DIR = '/srv/www/html/'
DEST_HOST = 'owidm.wmcloud.org'
DEST_DIR = '/srv/www-devel/html/'
DEST_HOST = 'owidm-devel.wmcloud.org'

WPMED_DONATE_URL = 'https://www.paypal.com/us/fundraiser/charity/1757736'

SPECIAL_PAGES  = ['identifyadmin.html',
                    '404.html',
                    'donate.html',
                    'feedback.html',
                    'thank-you.html',
                    'search.html',
                    'index.html']

# for test
u1 = 'interventions-ntds-sdgs.html'
u2 = 'share-of-population-with-schizophrenia.html'
u3 = 'share-of-adults-defined-as-obese.html'
u4 = 'asthma-prevalence.html'
u5 = 'new-covid-cases-per-million.html'

m1 = 'co2-gdp-decoupling.html'
m2 = 'diet-compositions.html'

def main():
    do_special_pages()
    do_main_pages()
    do_grapher_pages()

def do_special_pages():
    for file_name in SPECIAL_PAGES:
        if file_name != 'identifyadmin.html':
            do_special_page(file_name)

def do_special_page(file_name):
    print('Starting ' + file_name)
    page = get_page(file_name)
    page = remove_block("section", "homepage-coverage", page)
    page = remove_block("div", "see-all", page)
    page = remove_block("section", "homepage-subscribe", page)
    page = remove_block("section", "homepage-projects", page)
    page = change_host(page)
    page = mod_scripts(page)
    head_lines = BeautifulSoup(get_head_lines(), 'html.parser')
    page.head.append(head_lines)
    page = rem_banner(page)
    page = do_footer(page)
    bottom_lines = BeautifulSoup(get_main_bottom_lines(), 'html.parser')
    page.body.append(bottom_lines)
    output_converted_page(page, file_name)

def do_main_pages():
    file_list = get_page_list()
    for f in file_list:
        file_name = os.path.basename(f)
        if file_name not in SPECIAL_PAGES:
            try:
                do_main_page(file_name)
            except:
                print('***************************')

def do_main_page(file_name):
    print('Starting Main Page ' + file_name)
    page = get_page(file_name)
    page = change_host(page)
    page = mod_scripts(page)
    head_lines = BeautifulSoup(get_head_lines(), 'html.parser')
    page.head.append(head_lines)
    page = rem_banner(page)
    page = do_footer(page)
    bottom_lines = BeautifulSoup(get_main_bottom_lines(), 'html.parser')
    page.body.append(bottom_lines)
    output_converted_page(page, file_name)

def do_grapher_pages():
    file_list = get_page_list(dir='grapher/')
    for f in file_list:
        do_grapher_page(os.path.basename(f))

def do_grapher_page(file_name):
    print('Starting Grapher Page ' + file_name)
    page = get_page(file_name, dir='grapher/')
    # page = do_header(page) # this gets rewritten in js
    page = change_host(page)
    page = mod_scripts(page)
    head_lines = BeautifulSoup(get_head_lines(), 'html.parser')
    page.head.append(head_lines)
    page = rem_banner(page)
    page = do_footer(page)
    bottom_lines = BeautifulSoup(get_grapher_bottom_lines(), 'html.parser')
    page.body.append(bottom_lines)
    output_converted_page(page, file_name, dir='grapher/')

def get_page_list(dir=''):
    file_list = glob.glob(SOURCE_DIR + dir + '*.html')
    return file_list

def get_page(file_name, dir=''):
    inp_file = SOURCE_DIR + dir + file_name
    html = read_html_file(inp_file)
    page = BeautifulSoup(html, "html5lib")
    return page

def change_host(page):
    href_tags = page.find_all(href=True)
    content_tags = page.find_all(content=True)
    src_tags = page.find_all(src=True)
    figure_tags = page.find_all('figure')
    for tag in href_tags:
        tag['href'] = tag['href'].replace(SOURCE_HOST, DEST_HOST)
    for tag in content_tags:
        tag['content'] = tag['content'].replace(SOURCE_HOST, DEST_HOST)

    for tag in src_tags:
        if tag.name != 'script':
            tag['src'] = tag['src'].replace(SOURCE_HOST, DEST_HOST)
    for tag in figure_tags:
        if  tag.get('data-grapher-src'):
            tag['data-grapher-src'] = tag['data-grapher-src'].replace(SOURCE_HOST, DEST_HOST)

    return page

def rem_banner(page):
    banners = page.select('div.alert-banner div.content')
    if len(banners) == 0:
        return page
    new_banner_html = 'This material was copied from Our World in Data on ' + SOURCE_DATE + '. For current data please visit <a href="https://ourworldindata.org/">Our World in Data</a>'
    new_banner = BeautifulSoup(new_banner_html, "html5lib")
    banners[0].string = ''
    banners[0].append(new_banner)
    #if banner:
    #    banner[0].string = new_banner
    #    banner.append(new_banner_link)
    return page


def do_header(page): # not used
    logo = page.find("div", class_="site-logo")
    new_logo_a = BeautifulSoup('<a href="/">Our World in<br/> Data Mirror</a>', "html5lib")
    logo.a.replace_with(new_logo_a)
    other_logos = page.find("div", class_="header-logos-wrapper")
    #other_logos.decompose()
    return page

def do_footer(page):
    donation = page.find("section", class_="donate-footer")
    # turn off donation section 12/2/2022
    if donation:
        donation.p.string = 'Our World in Data Mirror and MDWiki are free and accessible for everyone.'
        donation.a['href'] = WPMED_DONATE_URL
        donation.a['target'] = '_blank'
        donation.decompose() # clear it
    footer = page.find("footer", class_="site-footer")
    block = footer.find("div", class_="owid-row")
    rm_rows = block.select('div .owid-col--lg-1')
    #legal = footer.select('div .owid-row div .legal')
    #rows = footer.select('div .owid-row div .owid-col .owid-col--lg-1')
    for row in rm_rows:
        row.decompose()
    legal_link = footer.find_all('a')[1]
    legal_link['href'] = '/legal'
    #rows.append(legal)
    page = remove_block("div", "site-tools", page)
    return page

def mod_scripts(page):
    scripts = page.find_all('script')
    scripts[-1].string = scripts[-1].text.replace('window.Grapher.', '// window.Grapher.')
    scripts[-3]['src'] = '/assets/owid.js'
    scripts[-4]['src'] = '/assets/vendors.js'
    scripts[-5]['src'] = '/assets/commons-mods.js'
    #scripts[-3]['src'] = scripts[-3]['src'].replace(SOURCE_HOST, DEST_HOST)
    #scripts[-5]['src'] = scripts[-5]['src'].replace(SOURCE_HOST, DEST_HOST)
    return page

def remove_block(tag, tag_class, page):
    block = page.find(tag, class_=tag_class)
    if block:
        block.decompose()
    return page

def read_html_file(input_file_path):
    with open(input_file_path, 'r') as f:
        text = f.read()
    return text

def output_converted_page(page, page_file_name, dir=''):
    html_output = page.encode_contents(formatter='html')
    output_file_name = DEST_DIR + dir + page_file_name
    write_conv_html_file(output_file_name, html_output)
    # print(output_file_name)

def write_conv_html_file(output_file_name, html_output):
    output_dir = os.path.dirname(output_file_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_file_name, 'wb') as f:
        f.write(html_output)

def get_head_lines():
    head_lines = '''
    <link rel="stylesheet" href="/assets/map-mirror.css">
    '''
    return head_lines

def get_main_bottom_lines():
    bottom_lines = '<script src="/assets/map-mirror.js"></script>'
    bottom_lines += '<script>\n'
    bottom_lines += 'var wpmedDonateUrl = "' + WPMED_DONATE_URL + '";\n'
    bottom_lines += '''
    mirrorMapsHeader(wpmedDonateUrl);
    </script>
    '''
    return bottom_lines

def get_grapher_bottom_lines():
    bottom_lines = '<script src="/assets/map-mirror.js"></script>'
    bottom_lines += '<script>\n'
    bottom_lines += 'var wpmedDonateUrl = "' + WPMED_DONATE_URL + '";\n'
    bottom_lines += '''
    var jsonConfigCC;
    if (jsonConfigCC == undefined){
        jsonConfigCC = JSON.parse(JSON.stringify(jsonConfig));
        jsonConfig.subtitle = '';
        jsonConfig.note = '';
        jsonConfig.sourceDesc += ', OWID';
        if ('relatedQuestions' in jsonConfig)
            delete jsonConfig.relatedQuestions;
    }
    mirrorMapsHeader(wpmedDonateUrl);
    window.Grapher.renderSingleGrapherOnGrapherPage(jsonConfig);
    mirrorMaps(jsonConfigCC);
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
