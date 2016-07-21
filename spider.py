#coding=utf-8
import urllib2
from lxml import etree

#爬取某一类别的视频广告的页面数量
page_index = 1
url = "http://k.cnad.com/view/video_production_list.aspx?category_id=23&page=" + str(page_index)
request = urllib2.Request(url)
response = urllib2.urlopen(request)
html = response.read()
tree = etree.HTML(html , parser=etree.HTMLParser(encoding='utf-8'))
page_box_list = tree.xpath(u'//div[@class="page_box"]/div/a')
page_count = page_box_list[3].text
print "当前分类是：消费电子与通讯；"
print "当前分类视频资源页面数共计：" + page_count + "页"

# 爬取视频广告的具体信息
page_index = 1
for page_index in range( int(page_count) ):
	url = "http://k.cnad.com/view/video_production_list.aspx?category_id=23&page=" + str(page_index + 1)
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	html = response.read()
	tree = etree.HTML(html , parser=etree.HTMLParser(encoding='utf-8'))
	# 注释掉的这两行xpath解析的是k.cnad.com这个路径下的页面，它存在分类栏这个结构
	# production_box_list_temp = tree.xpath(u'//div[@class="tab_con"]')
	# production_box_list = production_box_list_temp[0].xpath(u'div[@class="tab_con_list"]/div')
	production_box_list = tree.xpath(u'//div[@class="main_box"]/div[@class="production_box"]')
	index = 1
	for production_box in production_box_list:
		print "*****************当前是第" , page_index * 24 + index , "个视频资源，信息如下*****************"
		print "视频名称" , production_box[1][0].text.lstrip()
		print "品牌名称：" , production_box[2][0].text
		print "语种：" , production_box[3][0].text
		print "国家或地区：", production_box[3][1].text
		print "广告年份：", production_box[4][0].text
		print "广告类型：", production_box[4][1].text
		video_cover_image_link = production_box[0][0][0].get('src')
		if video_cover_image_link[0:4] == "http":
			print "广告视频封面图片链接:", production_box[0][0][0].get('src')
		else:
			print "广告视频封面图片链接:" , "http://k.cnad.com"+production_box[0][0][0].get('src')
		print "广告视频资源链接：" , "http://k.cnad.com"+production_box[0][0].get('href')
		print "**************************分割线***************************************"
		index += 1


#爬取视频广告的分类
# lis_temp = tree.xpath(u'//div[@class="left180"]/div')
# lis = lis_temp[0].xpath(u'div/ul/li/a')
#
# for li in lis:
# 	print li.get('title')
