# owid-static-mirror
Scripts to create a mirror of OurWorldInData
https://owidm.wmcloud.org/

## Test Page
https://mdwiki.org/wiki/WikiProjectMed:OWID

## Install/Setup

### apt packages
- apt install rsync
- apt install python3-pip

### python packages
- python3-bs4

### nginx
- package required
- /etc/nginx/sites-available/default modified:

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