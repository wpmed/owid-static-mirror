function mixMaps(jsonConfig){
    // console.log('in mixMaps')
    var infoBlurb = '<span class="tooltiptext">' + jsonConfig.subtitle
    try{
        noteLen = jsonConfig.note.length
    } catch (error) {
        noteLen = 0
    }
    if (noteLen > 0)
        infoBlurb += '<BR><BR>' + jsonConfig.note
    infoBlurb += '</span>'

    var host = 'owidm.wmcloud.org'
    var mapUrl = 'https://' + host + '/grapher/' + jsonConfig.slug

    var infoImg = '<img src="/images/240px-Info_icon_002.svg.png" alt="Info" width="35" height="auto">'

    var logo_elem = 'figure div .HeaderHTML .logo'

    //var logo_elem ='figure div .HeaderHTML a.logo'
    //if (window != window.top)
    //    logo_elem = 'figure div .HeaderHTML div.logo'
    $(logo_elem).innerHTML = infoImg + infoBlurb

    $(logo_elem).setAttribute('href', mapUrl)
    $(logo_elem).nextElementSibling.setAttribute('href', mapUrl)

    $(logo_elem).classList.add("tooltip");

    if ($('[data-track-note="chart-click-newtab"]') != null)
        $('[data-track-note="chart-click-newtab"]').setAttribute('href', mapUrl)

    // $('figure div .HeaderHTML a')
    // $('figure div .HeaderHTML a').nextElementSibling

    $('[data-track-note="chart-click-map"]').setAttribute( "onClick", "mixMaps(jsonConfigCC);" );
    $('[data-track-note="chart-click-chart"]').setAttribute( "onClick", "mixMaps(jsonConfigCC);" );
    // $('.GrapherComponent').setAttribute( "onClick", "grapherComponentClick();" );
}

function $(x) {return window.document.querySelector(x);}

// these functions sill do not solve the icon problem when going from Source to Map

function grapherComponentClick(){
    console.log('in grapherComponentClick')
    var tooltip = mixMapsToolTip()
    var logo_elem = 'figure div .HeaderHTML .logo'
    $(logo_elem).classList.add("tooltip");
    $(logo_elem).innerHTML = tooltip
  }

  function mixMapsToolTip(){
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

