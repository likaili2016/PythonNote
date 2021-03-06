# coding= utf-8

"""获取博客的排名并自动邮件通知"""

from bs4 import BeautifulSoup
from time import sleep
import requests
import logging
import thread


def get_nums(blogs_des):
    """
    get page ranks from string
    : param blogs_des:
    :return:
    """
    split_str = blogs_des.split('-')[1].strip()
    return split_str


class BlogRankMonitor(object):
    """
    博客园积分排名监控工具
    """
    def __init__(self, id):
          self.gap_seconds = 60 * 30  # 间隔时间为30min
          self.url_fmt = 'http://www.cnblogs.com/%s/mvc/blog/sidecolumn.aspx?blogApp=%s'
          self.id = id
          self.score = 0
          self.rank = 0
          self.his_score = 0
          self.his_rank = 0

    def get_blog_ranks(self):
        """
        解析页面获取博客积分和排名
        :return:
        """
        url = self.url_fmt % (self.id, self.id)
        res = requests.get(url)
        soup = BeautifulSoup(res.text)
        lis = soup.find_all('div')

        for item in lis:
            if 'sidebar_scorerank' == item.get('id'):
                li_lists = item.find_all('li')

                for li_item in li_lists:
                    if u'积分' in li_item.text:
                        self.score = get_nums(li_item.text)
                    elif u'排名' in li_item.text:
                        self.rank = get_nums(li_item.text)
                    else:
                        print 'Error'
            continue

    def monitor_score_rank(self):
        """
        监控博客积分及排名的变化
        :return:
        """
        while True:
            self.get_blog_ranks()
            if self.score != self.score or self.rank != self.his_rank:
                # 发送邮件
                mail_title = '[e-notice]:blog-rank-changes'
                mail_body = "[%s]time-(score,rank):old-(%s,%s),now-(%s,%s)" \
                            % (
                               self.id,
                               self.his_score, self.his_rank,
                               self.score, self.rank
                            )





