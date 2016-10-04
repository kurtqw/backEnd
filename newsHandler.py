# coding=utf-8
import tornado.web
import pymysql
import json
import configparser


class NewsHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kargs):
        parser = configparser.ConfigParser()
        parser.read('mysql.ini')
        host = parser['CONFIG']['HOST']
        username = parser['CONFIG']['USERNAME']
        password = parser['CONFIG']['PASSWORD']
        db = parser['CONFIG']['DB']

        self.conn = pymysql.connect(host, username, password, db,charset='utf8')
        self.cur = self.conn.cursor()
        self.select_stmt = 'select * from news order by pv desc'
        self.size = self.cur.execute(self.select_stmt)
        l = list(range(0, self.size, 9))
        self.index = list(zip(l, l[1:]))
        self.res = self.cur.fetchall()
        super(NewsHandler, self).__init__(application, request, **kargs)

    def get(self):
        page = int(self.get_argument("page", 1))
        try:
            head = self.index[page - 1][0]
            tail = self.index[page - 1][1]
            newsTuple = self.res[head:tail]
            data = []
            for t in newsTuple:
                news = {}
                news['id'] = t[0]
                news['url'] = t[1]
                news['title'] = t[2]
                news['visit_cnt'] = t[3]
                data.append(news)
            self.write(json.dumps({'status': 0, 'data': data}))
        except IndexError as e:
            self.write(json.dumps({'status': 1, 'data': 'page exceed limits'}))

        '''
        TODO 更新热点的pv数
        '''

# if __name__ == '__main__':
#    n = NewsHandler()
#    n.get()
