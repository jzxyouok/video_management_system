#coding=utf-8
import urllib2
from lxml import etree
import time
import math
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def multiConnect(request):
    try:
        response = urllib2.urlopen(request)
        return response
    except:
        print "网络异常，正在重新尝试连接..."
        multiConnect(request)

start_time = time.clock()

#爬取视频广告的分类
url = "http://k.cnad.com"
request = urllib2.Request(url)
response = urllib2.urlopen(request)
html = response.read()
tree = etree.HTML(html , parser=etree.HTMLParser(encoding='utf-8'))

category_list_temp = tree.xpath(u'//div[@class="left180"]/div')
category_list = category_list_temp[0].xpath(u'div/ul/li/a')

category_item_dict = []
for category_item in category_list:
    # print category_item.get('title')
    # print url + category_item.get('href')
    category_item_dictitem = { "title" : category_item.get('title'), "href" : url + category_item.get('href')}
    category_item_dict.append(category_item_dictitem)
print category_item_dict

production_box_item_list_total = []
for category_item in category_item_dict:
    # 爬取某一类别的视频广告的页面数量
    production_box_item_list = []
    page_index = 1
    url = category_item['href'] + "&page=" + str(page_index)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    html = response.read()
    tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
    page_box_list = tree.xpath(u'//div[@class="page_box"]/div/a')
    page_count = page_box_list[-2].text
    print "当前分类是：" + category_item['title'] + ";"
    print "当前分类视频资源页面数共计：" + page_count + "页"

    # 爬取视频广告的具体信息
    for page_index in range(int(page_count)):
        url = category_item['href'] + "&page=" + str(page_index + 1)
        request = urllib2.Request(url)
        # response = multiConnect(request)
        try:
            response = urllib2.urlopen(request)
        except:
            print "网络异常，正在重新尝试连接..."
            response = urllib2.urlopen(request)
        html = response.read()
        tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
        # 注释掉的这两行xpath解析的是k.cnad.com这个路径下的页面，它存在分类栏这个结构
        # production_box_list_temp = tree.xpath(u'//div[@class="tab_con"]')
        # production_box_list = production_box_list_temp[0].xpath(u'div[@class="tab_con_list"]/div')
        production_box_list = tree.xpath(u'//div[@class="main_box"]/div[@class="production_box"]')
        production_index = 1
        for production_box in production_box_list:
            # print "*****************当前是第", page_index * 24 + production_index, "个视频资源，信息如下*****************"
            # print "视频名称", production_box[1][0].text.lstrip()
            # print "品牌名称：", production_box[2][0].text
            # print "语种：", production_box[3][0].text
            # print "国家或地区：", production_box[3][1].text
            # print "广告年份：", production_box[4][0].text
            # print "广告类型：", production_box[4][1].text
            # video_cover_image_link = production_box[0][0][0].get('src')
            # if video_cover_image_link[0:4] == "http":
            #     print "广告视频封面图片链接:", production_box[0][0][0].get('src')
            # else:
            #     print "广告视频封面图片链接:", "http://k.cnad.com" + production_box[0][0][0].get('src')
            # print "广告视频资源链接：", "http://k.cnad.com" + production_box[0][0].get('href')
            # print "**************************分割线***************************************"
            production_box_item = {
                                    "视频名称" : production_box[1][0].text.lstrip(),
                                    "品牌名称" : production_box[2][0].text,
                                    "语种" : production_box[3][0].text,
                                    "国家或地区" : production_box[3][1].text,
                                    "广告年份" : production_box[4][0].text,
                                    "广告类型" : production_box[4][1].text,
                                    "广告视频封面图片链接" : "??",
                                    "广告视频资源链接" : production_box[0][0].get('href')
                                    }
            # print production_box_item
            # print json.dumps(production_box_item , ensure_ascii=False , indent=2)
            production_box_item_list.append(production_box_item)
            production_index += 1

    production_box_item_list_object = {
                                        "所属分类" :category_item.get('title') ,
                                        "视频资源集合" : production_box_item_list
                                        }
    production_box_item_list_total.append(production_box_item_list_object)

# print production_box_item_list_total
d = json.dumps(production_box_item_list_total , ensure_ascii=False , indent=2)
with open("C:\\Users\\oliverfan\\Desktop\\111.txt", "w") as f:
    json.dump(d, f)

end_time = time.clock()
time_duration = end_time - start_time

print "Spider爬取工作完成。"
print "共耗时："  + str(int(time_duration/60)) + " 分 " + str(int(math.ceil(time_duration%60))) + "秒"