################################################################################
#
#	dump.com (BY TEHCRUCIBLE) - v0.01
#
################################################################################

TITLE = "dump.com"
PREFIX = "/video/dump"
ART = "art-default.jpg"
ICON = "icon-default.png"
ICON_LIST = "icon-list.png"
ICON_NEXT = "icon-next.png"
BASE_URL = "http://www.dump.com"

################################################################################
# Set global variables

def Start():

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON_COVER)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON_COVER)
	VideoClipObject.art = R(ART)

	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
	HTTP.Headers['Referer'] = 'http://g2g.fm/'

################################################################################
# Latest videos

@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu():

	oc = ObjectContainer()
	page_data = HTML.ElementFromURL(BASE_URL)

	for each in page_data.xpath("//div/a[@class='b']"):
		oc.add(VideoClipObject(
			url = BASE_URL + each.xpath("./@href")[0],
			originally_available_at = Datetime.ParseDate(each.xpath("./span[@class='video_date']/text()")[0]),
			title = each.xpath("./span[@class='video_title']/text()")[0],
			thumb = each.xpath("./img/@data-original")[0],
			)
		)

	oc.add(DirectoryObject(
		key = Callback(Archives),
		title = "Browse Archives",
		thumb = ICON_NEXT
		)
	)

	return oc

################################################################################
# Displays archives

@route(PREFIX + "/archives")
def Archives():

	oc = ObjectContainer()
	page_data = HTML.ElementFromURL(BASE_URL + "/archives/")

	for each in page_data.xpath("//a[@class='b']"):
		oc.add(DirectoryObject(
			key = Callback(Browse, url = BASE_URL + each.xpath("./@href")[0]),
			title = each.xpath("./text()")[0],
			thumb = ICON_LIST
			)
		)

	return oc

################################################################################
# Displays archives

@route(PREFIX + "/browse")
def Browse(url):

	oc = ObjectContainer()
	page_data = HTML.ElementFromURL(url)

	for each in page_data.xpath("//div/a[@class='b']"):
		oc.add(VideoClipObject(
			url = BASE_URL + each.xpath("./@href")[0],
			originally_available_at = Datetime.ParseDate(each.xpath("./span[@class='video_date']/text()")[0]),
			title = each.xpath("./span[@class='video_title']/text()")[0],
			thumb = each.xpath("./img/@data-original")[0],
			)
		)

	oc.add(DirectoryObject(
		key = Callback(Archives),
		title = "Browse Archives",
		thumb = ICON_NEXT
		)
	)

	return oc
