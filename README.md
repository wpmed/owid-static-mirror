# owid-static-mirror
Scripts to create a mirror of OurWorldInData
https://owidm.wmcloud.org/

## Test Page
https://mdwiki.org/wiki/WikiProjectMed:OWID

## Install/Setup

### apt packages
- apt install rsync
- apt install python3-pip
- nginx required

### python packages
- python3-bs4

## Environment
- Live /srv/www/html
- Stageing /srv/www-staging/html
- Devel /srv/www-devel/html

A new download is first tested on Devel, then converted again to Staging, then Staging is moved to Live.

## Assets
- From a given owid-static release
- Contents of assets unmodified
- commons-mods.js
- This has all ourworldindata.org urls replaced with owidm.wmcloud.org
- The following two files that patch the output of static
- map-mirror.css
- map-mirror.js

## Pages
- legal.html

## Conversion Scripts

### conv_static_html.py
- Converts grapher pages to modify sections and add assets

## Refresh Graphs
-

## nginx config
- sites enabled:
### /etc/nginx/sites-available/default modified:
server {
        listen 80 default_server;
        listen [::]:80 default_server;
        root /srv/www/html;
        server_name _;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ $uri.html =404;
                #sub_filter '<figure data-grapher-src="https://ourworldindata.org/' '<figure data-grapher-src="https://$host/';
                #sub_filter 'href="https://ourworldindata.org/'  'href="https://$host/';
                #sub_filter 'ourworldindata.org/' 'owidm.wmcloud.org/';
                #sub_filter_once off;
        }
}


root /srv/www/html;
server_name _;
location / {
    # First attempt to serve request as file, then
    # as directory, then fall back to displaying a 404.
    try_files $uri $uri/ $uri.html =404;

- ? nginx.conf added ssl:
        ##
        # SSL Settings
        ##

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
        ssl_prefer_server_ciphers on;
### /etc/nginx/sites-available/owidm modified:
server {
        listen 80;
        root /srv/www/html;

        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;

        # server_name _;
        server_name owidm.wmcloud.org;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ $uri.html =404;
                #sub_filter '<figure data-grapher-src="https://ourworldindata.org/' '<figure data-grapher-src="https://$host/';
                #sub_filter 'href="https://ourworldindata.org/'  'href="https://$host/';
                #sub_filter 'ourworldindata.org/' 'owidm.wmcloud.org/';
                #sub_filter_once off;
        }
}


### /etc/nginx/sites-available/owidm-devel modified:
server {
        listen 80;
        root /srv/www-devel/html;

        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;

        server_name owidm-devel.wmcloud.org;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ $uri.html =404;
                #sub_filter '<figure data-grapher-src="https://ourworldindata.org/' '<figure data-grapher-src="https://$host/';
                #sub_filter 'href="https://ourworldindata.org/'  'href="https://$host/';
                #sub_filter 'ourworldindata.org/' 'owidm.wmcloud.org/';
                #sub_filter_once off;
        }
}
