function mirrorMapsHeader(donateUrl){
    var logoElem = 'div .site-logo a'
    $(logoElem).innerHTML = 'Our World in<br/> Data Mirror'
    //var navList = $('ul.site-primary-links').children
    //var navLinks = Array.from(navList)
    //for (var link of navLinks)
    //    if (link.querySelector('a').pathname  == '/donate')
    //        link.querySelector('a').href = donateUrl;
    var topNav =  $('ul.site-primary-links');
    var html = '<li><a href="https://mdwiki.org/wiki/Main_Page" data-track-note="header-navigation">MD Wiki</a></li>';
    html += '<li><a href="/legal" data-track-note="header-navigation">Legal</a></li>';
    // html += '<li><a href="' + donateUrl + '" data-track-note="header-navigation">Donate</a></li>'; // remove donate 12/2/2022
    html += '</ul>';
    topNav.innerHTML = html;

    var topLogos = $('div.header-logos-wrapper');
    html = '<a href="https://www.oxfordmartin.ox.ac.uk/global-development" class="oxford-logo"><img src="/oms-logo.svg" alt="Oxford Martin School logo"></a>';
    html += '<a href="https://global-change-data-lab.org/" class="gcdl-logo"><img src="/gcdl-logo.svg" alt="Global Change Data Lab logo"></a></div>';
    topLogos.innerHTML = html;



    $('.site-navigation-bar').innerHTML = "MDWiki's OWID Graph Collection"

}

function mirrorMaps(jsonConfig){
    // console.log('in mirrorMaps')
    var infoBlurb = '<span class="tooltiptext">' + jsonConfig.subtitle
    try{
        noteLen = jsonConfig.note.length
    } catch (error) {
        noteLen = 0
    }
    if (noteLen > 0)
        infoBlurb += '<BR><BR>' + jsonConfig.note
    //infoBlurb += '<BR><BR>The formatting and style of this material has been altered by MDWiki for use within a Mediawiki and is not endorsed in any way by Our World in Data.'
    infoBlurb += '<BR><BR>MDWiki alternations to this content have not been endorsed by OWID.'
    infoBlurb += '</span>'

    var host = 'owidm.wmcloud.org'
    var mapUrl = 'https://' + host + '/grapher/' + jsonConfig.slug

    var infoImg = '<img src="/images/240px-Info_icon_002.svg.png" alt="Info" width="35" height="auto">'

    var logoElem = 'figure div .HeaderHTML .logo'

    //var logoElem ='figure div .HeaderHTML a.logo'
    //if (window != window.top)
    //    logoElem = 'figure div .HeaderHTML div.logo'
    $(logoElem).innerHTML = infoImg + infoBlurb

    $(logoElem).setAttribute('href', mapUrl)
    $(logoElem).nextElementSibling.setAttribute('href', mapUrl)

    $(logoElem).classList.add("tooltip");

    if ($('[data-track-note="chart-click-newtab"]') != null)
        $('[data-track-note="chart-click-newtab"]').setAttribute('href', mapUrl)

    // $('figure div .HeaderHTML a')
    // $('figure div .HeaderHTML a').nextElementSibling

    $('[data-track-note="chart-click-map"]').setAttribute( "onClick", "mirrorMaps(jsonConfigCC);" );
    $('[data-track-note="chart-click-chart"]').setAttribute( "onClick", "mirrorMaps(jsonConfigCC);" );
    // $('.GrapherComponent').setAttribute( "onClick", "grapherComponentClick();" );
}

function $(x) {return window.document.querySelector(x);}
// function $$(x) {return window.document.querySelectorAll(x);}

// these functions sill do not solve the icon problem when going from Source to Map

function grapherComponentClick(){
    console.log('in grapherComponentClick')
    var tooltip = mirrorMapsToolTip()
    var logoElem = 'figure div .HeaderHTML .logo'
    $(logoElem).classList.add("tooltip");
    $(logoElem).innerHTML = tooltip
  }

  function mirrorMapsToolTip(){
      var infoBlurb = '<span class="tooltiptext">' + jsonConfigCC.subtitle
      try{
          noteLen = jsonConfigCC.note.length
      } catch (error) {
          noteLen = 0
      }
      if (noteLen > 0)
          infoBlurb += '<BR><BR>' + jsonConfigCC.note
      infoBlurb += '</span>'
      var infoImg = '<img src="/images/240px-Info_icon_002.svg.png" alt="Info" width="35" height="auto">'

      return infoImg + infoBlurb
  }

