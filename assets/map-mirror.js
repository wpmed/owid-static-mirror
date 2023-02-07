function mirrorMapsHeader() {
  var html = "MDWiki's OWID Graph Collection"
  var graphFrag = owidmGetGraphFrag()
  if (graphFrag != ''){
    html += '<div><button style="border-radius: 8px;" onclick="owidmCopyExtension()">Click to Compute and Copy Embed Tag</button><span>&nbsp;Then Paste on Page in Wiki Editor.</span><div>'
    html += '<div>Clipboard:&nbsp;<span id="owidmEmbedTag" style="font-size: .75em;"></span></div>'
  }
  $('.site-navigation-bar').innerHTML = html
  $('.site-navigation-bar').style.display = 'block'
}

function owidmCopyExtension() {
  var tagString
  var paramString = ''
  var paramParts = []

  var graphFrag = owidmGetGraphFrag()
  if (graphFrag == '')
    return

  tagString = '<ourworldindata'
  const parts = graphFrag.split('?')
  const page = parts[0]
  if (parts.length == 2)
    paramParts = parts[1].split('&')
    for (var i in paramParts)
      tagString += ' ' + paramParts[i]
  tagString += '>' + page + '</ourworldindata>'

  $('#owidmEmbedTag').innerHTML =  owidmEscapeTag(tagString)
  navigator.clipboard.writeText(tagString);
}

function owidmGetGraphFrag(){
  const urlParts = window.location.href.split('/')

  if (urlParts.length != 5)
    return ''
  else if (urlParts[3] != 'grapher')
    return ''
  else
    return urlParts[4]
}

function owidmEscapeTag(htmlStr) {
  return htmlStr.replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");

}

function mirrorMaps(jsonConfig) {
  // console.log('in mirrorMaps')
  var infoBlurb = '<span class="tooltiptext">' + jsonConfig.subtitle
  var noteLen = 0
  try {
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

  // adding onclick for table didn't really solve anything
  $('[data-track-note="chart-click-map"]').setAttribute("onClick", "mirrorMaps(jsonConfigCC);");
  $('[data-track-note="chart-click-chart"]').setAttribute("onClick", "mirrorMaps(jsonConfigCC);");
  $('[data-track-note="chart-click-table"]').setAttribute("onClick", "mirrorMaps(jsonConfigCC);");
  // $('.GrapherComponent').setAttribute( "onClick", "grapherComponentClick();" );
}

function $(x) { return window.document.querySelector(x); }
// function $$(x) {return window.document.querySelectorAll(x);}

// these functions sill do not solve the icon problem when going from Source to Map

function grapherComponentClick() {
  console.log('in grapherComponentClick')
  var tooltip = mirrorMapsToolTip()
  var logoElem = 'figure div .HeaderHTML .logo'
  $(logoElem).classList.add("tooltip");
  $(logoElem).innerHTML = tooltip
}

function mirrorMapsToolTip() {
  var infoBlurb = '<span class="tooltiptext">' + jsonConfigCC.subtitle
  try {
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

