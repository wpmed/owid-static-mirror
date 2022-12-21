#!/usr/bin/python3
from fileinput import filename
import os
import time
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
SOURCE_DATE = '2022-11-30'
SOURCE_HOST = 'ourworldindata.org'

# Live - urls are owidm
DEST_DIR = '/srv/www/html/'
DEST_HOST = 'owidm.wmcloud.org'

# Staging - urls are owidm
DEST_DIR = '/srv/www-staging/html/'
DEST_HOST = 'owidm.wmcloud.org'

# Devel - urls are owidm-devel. this is the default
DEST_DIR = '/srv/www-devel/html/'
DEST_HOST = 'owidm-devel.wmcloud.org'

WPMED_DONATE_URL = 'https://www.paypal.com/us/fundraiser/charity/1757736'

SPECIAL_PAGES  = ['identifyadmin.html',
                    '404.html',
                    'about.html',
                    'charts.html',
                    'donate.html',
                    'donations-faq.html',
                    'faqs.html',
                    'feedback.html',
                    'funding.html',
                    'legal.html',
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

def main(args):
    global DEST_DIR
    global DEST_HOST
    global SOURCE_DATE

    SOURCE_DATE = get_owid_date()

    if args.staging: # do staging instead of devel
        DEST_DIR = '/srv/www-staging/html/'
        DEST_HOST = 'owidm.wmcloud.org'

    # do_special_pages()
    do_index_page()
    do_main_pages()
    do_grapher_pages()

def do_index_page(): # chart.html is used as index page
    file_name = 'charts.html'
    print('Starting ' + file_name)
    page = get_page(file_name)

    page.find("section", {"id": "explorers-section"}).decompose()


    #page = remove_block("section", "homepage-coverage", page)
    #page = remove_block("div", "see-all", page)
    #page = remove_block("section", "homepage-subscribe", page)
    #page = remove_block("section", "homepage-projects", page)
    page = change_host(page)
    page = mod_scripts(page)
    head_lines = BeautifulSoup(get_head_lines(), 'html.parser')
    page.head.append(head_lines)
    page = rem_banner(page)
    page = do_footer(page)
    bottom_lines = BeautifulSoup(get_main_bottom_lines(), 'html.parser')
    page.body.append(bottom_lines)
    output_converted_page(page, file_name)
    output_converted_page(page, 'index.html') # put in both charts and index

def do_special_pages():
    # 12/18/2022 don't do any of the special pages
    return
    # obsolete
    for file_name in SPECIAL_PAGES:
        if file_name != 'identifyadmin.html':
            do_special_page(file_name)

def do_special_page(file_name): # not used
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
    # new_banner_html = 'This material was copied from <a href="https://ourworldindata.org/">Our World in Data</a> on ' + SOURCE_DATE + '.'
    new_banner_html += '<BR>The formatting and style of this material has been altered by MDWiki for use within a Mediawiki and is not endorsed in any way by Our World in Data.'
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

# revise so only div .legal remains
# decompose it and then read lines
def do_footer(page):
    legal = page.find("div", class_="legal")
    legal.clear()
    legal.append(BeautifulSoup(get_legal_lines(), 'html.parser'))

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
    #legal_link = footer.find_all('a')[1]
    #legal_link['href'] = '/legal'
    #rows.append(legal)
    page = remove_block("div", "site-tools", page)
    return page

def mod_scripts(page):
    scripts = page.find_all('script')
    scripts[-1].string = scripts[-1].text.replace('window.Grapher.', '// window.Grapher.')
    scripts[-3]['src'] = '/assets-' + SOURCE_DATE + '/owid.js'
    scripts[-4]['src'] = '/assets-' + SOURCE_DATE + '/vendors.js'
    scripts[-5]['src'] = '/assets-' + SOURCE_DATE + '/commons-mods.js'
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
        //if ('sourceDesc' in jsonConfig)
        //    jsonConfig.sourceDesc += ', OWID without any endorsement';
        //else
        //    jsonConfig.sourceDesc = 'OWID without any endorsement';
        if ('relatedQuestions' in jsonConfig)
            delete jsonConfig.relatedQuestions;
    }
    mirrorMapsHeader();
    window.Grapher.renderSingleGrapherOnGrapherPage(jsonConfig);
    mirrorMaps(jsonConfigCC);
    </script>
    '''
    return bottom_lines

def get_legal_lines():
    legal_lines = '''
    <p>This site is licensed CC BY, the same as OurWorldinData from which it copies graphs and supporting material. It is completely independent of OurWorldinData and is not endorsed by it.</p>
    <p>The purpose of this site is threefold, to host graphs on WMF infrastructure, to provide a means of selecting graphs to embed in a MediaWiki site, and to make formatting and stylistic chnages to graphs that make them more compatible with inclusion on such a site.
     Use this site to embed graphs in a MediaWiki server. Use OWID for everything else.</p>
    <p>Where possible and reasonable the following changes have been made to OWID source material:</p>
    <ol>
    <li>All links to ourworldindata.org have been changed to the host on which you are reading this.</li>
    <li>Colors have been changed to avoid confusion with the OWID brand.</li>
    <li>Pages that relate specifically to the OWID organization and its partners have not been included.</li>
    <li>OWID and third party logos have been removed.</li>
    <li>The 'explorer' style visualizations have not been included.</li>
    <li>No changes have been made to the actual Graphs and Maps of Data.</li>
    <li>Some Graph and Map metadata has been moved to an info popup icon.</li>
    <li>This site is only synced with OurWorldinData periodically so data may be less current.</li>
    <li>Graphs that disappear from OWID are intended to remain on this site as they may already be in use.</li>
    <li>robots.txt files have been deployed to discourage indexing of this site.</li>
    </ol>
    '''
    return legal_lines

def get_owid_date():
    repo_date = os.path.getctime(SOURCE_DIR + '.git')
    return time.strftime('%Y-%m-%d', time.localtime(repo_date))

if __name__ == "__main__":
    # place holder for future args
    parser = argparse.ArgumentParser(description="Convert downloaded html.")
    parser.add_argument("-s", "--staging", help="Convert to Staging instead of Devel", action="store_true")
    parser.add_argument("-t", "--test", help="For testing don't run main", action="store_true")
    args = parser.parse_args()
    if not args.test:
        main(args)
    #main()
