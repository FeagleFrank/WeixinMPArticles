import urllib.request
import http.cookiejar
import re
import json
import time
import pdfkit
import os
import threading


class MP:
    articles = []
    cookie_filename = 'cookie.txt'
    offset = 0

    def set_cookie(self, url):
        cookie = http.cookiejar.LWPCookieJar(self.cookie_filename)
        handler = urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(handler)
        request = urllib.request.Request(url)
        response = opener.open(request)
        print(response.read().decode())
        cookie.save(ignore_discard=True, ignore_expires=True)

    def get_all_link(self, url_link):
        cookie = http.cookiejar.LWPCookieJar(self.cookie_filename)
        cookie.load(self.cookie_filename, ignore_discard=True, ignore_expires=True)
        handler = urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(handler)

        while 1:
            print('offset:' + str(self.offset))
            url = re.sub("(?<=&offset=)(\d+)(?=&)", self.change_offset, url_link)
            request = urllib.request.Request(url)
            response = opener.open(request)
            data = json.loads(response.read().decode())
            articles = json.loads(data['general_msg_list'])['list']
            if not articles:
                break
            self.articles.extend(articles)
            self.offset += 10
            time.sleep(1)

        print('total: ' + str(len(self.articles)))

    def html_to_pdf(self):
        for article in self.articles:
            t = article['comm_msg_info']['datetime']
            time_local = time.localtime(t)
            dt = time.strftime("%Y%m%d", time_local)
            title = article['app_msg_ext_info']['title']
            url = article['app_msg_ext_info']['content_url']
            print(url)
            # from_url会丢失图片
            # pdfkit.from_url(url, dt + '-' + title + '.pdf')
            response = urllib.request.urlopen(url)
            data = response.read().decode()
            data = data.replace('data-src', 'src')

            t = threading.Thread(target=self.get_pdf, args=(data, dt + '-' + title + '.pdf'))
            t.start()
            time.sleep(2)

    def get_pdf(self, st, name):
        if os.path.exists(name):
            print('skip')
            return
        try:
            print(name)
            pdfkit.from_string(st, name)
        except:
            pass

    def change_offset(self, matched):
        return str(self.offset)


if __name__ == '__main__':
    url = 'https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=xxx==&uin=xxx&key=xxx&devicetype=xxx&version=xxx&lang=zh_CN&ascene=x&pass_ticket=xxx'
    url_link = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=xxx==&f=json&offset=10&count=10&is_ok=1&scene=124&uin=xxx&pass_ticket=xxx&wxtoken=&appmsg_token=xxx&x5=0&f=json'
    mp = MP()
    mp.set_cookie(url)
    mp.get_all_link(url_link)
    mp.html_to_pdf()

