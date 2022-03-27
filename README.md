# owid-static-mirror
Scripts to create a mirror of OurWorldInData

## Install/Setup

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

## Assets
- From a give owid-static release
- Contents of assets unmodified
- commons-mods.js
- This has all ourworldindata.org urls replaced with owidm.wmcloud.org
- The following two files that patch the output of static
- map-mixer.css
- map-mixer.js

## Conversion Scripts

### conv_static_html.py
- Converts grapher pages to modify sections and add assets
