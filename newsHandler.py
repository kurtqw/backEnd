# coding=utf-8
import tornado.web
import pymysql
import json
import configparser
import json
import traceback


class NewsHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kargs):
        parser = configparser.ConfigParser()
        parser.read('mysql.ini')
        host = parser['CONFIG']['HOST']
        username = parser['CONFIG']['USERNAME']
        password = parser['CONFIG']['PASSWORD']
        db = parser['CONFIG']['DB']

        self.conn = pymysql.connect(host, username, password, db, charset='utf8')
        self.cur = self.conn.cursor()
        self.select_stmt = 'select * from news where type="news" order by visit_cnt desc'
        self.size = self.cur.execute(self.select_stmt)
        l = list(range(0, self.size, 9))
        self.index = list(zip(l, l[1:]))
        self.res = self.cur.fetchall()
        super(NewsHandler, self).__init__(application, request, **kargs)

    def set_default_headers(self):
        # 跨域
        # self.set_header('Access-Control-Allow-Origin', r'^(https?://(?:.+\.)?localhost(?::\d{1,5})?)$')
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        # self.set_header('Access-Control-Max-Age', 1000)
        # self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Credentials', "false")

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.set_header("Access-Control-Allow-Headers",
                        "Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By, If-Modified-Since, X-File-Name, Cache-Control")

    def check_origin(self, origin):
        self.set_header('Access-Control-Allow-Origin', "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        # self.set_header('Access-Control-Allow-Credentials', "true")

    def get(self):
        page = int(self.get_argument("page", 1))
        print('page:　')
        print(page)
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
            self.write(json.dumps({'status': 1, 'data': data}))
        except IndexError as e:
            self.write(json.dumps({'status': 0, 'data': 'page exceed limits'}))

    def post(self, *args, **kwargs):
        try:
            if isinstance(self.request.body, bytes):
                print(self.request.body)
                body = self.request.body.decode('utf-8')
                request_body = json.loads(body)
            else:
                request_body = json.loads(self.request.body)
            news_id = request_body['news_id']
            cnt_new = int(request_body['cnt'])
            status = self.cur.execute('select visit_cnt from news where news_id=%s', news_id)
            if status == 0:
                self.write(json.dumps({'status': 0, 'data': 'wrong news_id'}))
                return
            else:
                cnt_old = self.cur.fetchone()[0]
            cnt_new = cnt_new + cnt_old
            update_stmt = "update news set visit_cnt =%s where news_id=%s;"
            status = self.cur.execute(update_stmt, [str(cnt_new), news_id])
            if status == 0:
                self.write(json.dumps({'status': 0, 'data': 'update failed'}))
                return
            self.conn.commit()
            self.write(json.dumps({'status': 1}))
        except Exception as e:
            traceback.print_exc()
            self.write(json.dumps({'status': 0, 'data': 'decode json failed'}))


class JokeHanlder(tornado.web.RequestHandler):
    def __init__(self, application, request, **kargs):
        parser = configparser.ConfigParser()
        parser.read('mysql.ini')
        host = parser['CONFIG']['HOST']
        username = parser['CONFIG']['USERNAME']
        password = parser['CONFIG']['PASSWORD']
        db = parser['CONFIG']['DB']

        self.conn = pymysql.connect(host, username, password, db, charset='utf8')
        self.cur = self.conn.cursor()
        self.select_stmt = 'select content from joke order by rand()'
        super(JokeHanlder, self).__init__(application, request, **kargs)

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Credentials', "false")

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.set_header("Access-Control-Allow-Headers",
                        "Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By, If-Modified-Since, X-File-Name, Cache-Control")

    def check_origin(self, origin):
        self.set_header('Access-Control-Allow-Origin', "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')

    def get(self):
        """
        :return: 随机返回一个笑话
        """
        status = self.cur.execute(self.select_stmt)
        items = self.cur.fetchall()
        if len(items) == 0:
            self.write(json.dumps({'status': 0, 'data': 'Not enough jokes'}))
            return
        import random
        rand_index = random.randrange(0, len(items) - 1)
        print(items[rand_index][0])
        self.write(json.dumps({'status': 1, 'data': items[rand_index][0]}))


class TopicHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kargs):
        parser = configparser.ConfigParser()
        parser.read('mysql.ini')
        host = parser['CONFIG']['HOST']
        username = parser['CONFIG']['USERNAME']
        password = parser['CONFIG']['PASSWORD']
        db = parser['CONFIG']['DB']

        self.conn = pymysql.connect(host, username, password, db, charset='utf8')
        self.cur = self.conn.cursor()
        self.select_stmt = 'select url,title from news WHERE type="%s" order by rand() limit 10'
        self.topic_type = ['sport', 'movie', 'game', 'travel', 'music', 'library']
        super(TopicHandler, self).__init__(application, request, **kargs)

    def get(self):
        topic_type = self.get_argument("type")
        if topic_type not in self.topic_type:
            self.write(json.dumps({'status': 0, 'data': 'type not found'}))
            return
        select_stmt = self.select_stmt % topic_type
        print(select_stmt)
        self.cur.execute(select_stmt)
        items = self.cur.fetchall()
        data = [{'url': item[0], 'title': item[1]} for item in items]
        print(data)
        self.write(json.dumps({'status': 1, 'data': data}))

# if __name__ == '__main__':
#    n = NewsHandler()
#    n.get()
