class Table:
    def __init__(self, conn, spider_name, create_stmt, insert_stmt, cache_size=None, is_created=False):
        self.create_stmt = create_stmt
        self.insert_stmt = insert_stmt
        self.conn = conn
        self.spider_name = spider_name
        self.cache_size = cache_size
        self.cache = []
        self.cur = self.conn.cursor()
        if not is_created:
            self.cur.execute(self.create_stmt)
        self.conn.commit()

    def insert(self, *args):
        if self.cache_size == 0:
            self.cur.execute(self.insert_stmt, args)
            self.conn.commit()
        else:
            self.cache.append(args)
            if len(self.cache) > self.cache_size:
                self.flush()

    def insertmany(self, arr):
        self.cur.executemany(self.insert_stmt, arr)
        self.conn.commit()

    def flush(self):
        self.insertmany(self.cache)
        self.cache = []


class NewsTable(Table):
    def __init__(self, conn, spider_name, cache_size=None, is_created=False):
        self.table_name = 'news'
        create_stmt = 'create table if not exists ' + self.table_name + \
                      ' (`news_id` INT NOT NULL AUTO_INCREMENT,' \
                      '`url` VARCHAR(250)  NOT NULL,' \
                      '`title` VARCHAR(250) NOT NULL, ' \
                      '`type` VARCHAR(100) NOT NULL, ' \
                      ' `visit_cnt`INT DEFAULT 0,' \
                      '  PRIMARY KEY (news_id));'
        insert_stmt = 'insert ignore into ' + self.table_name + \
                      ' values(NULL,%s,%s,%s,0);'
        Table.__init__(self, conn, spider_name, create_stmt, insert_stmt, cache_size, is_created)


class JokeTable(Table):
    def __init__(self, conn, spider_name, cache_size=None, is_created=False):
        self.table_name = 'joke'
        create_stmt = "create table if not exists " + self.table_name + " (`joke_id` INT  NOT NULL AUTO_INCREMENT,  `content` TEXT NOT NULL,  `pop_cnt` INT  NOT NULL DEFAULT 0,  PRIMARY KEY (joke_id));"
        insert_stmt = 'insert ignore into ' + self.table_name + ' values(NULL,%s,0);'
        Table.__init__(self, conn, spider_name, create_stmt, insert_stmt, cache_size, is_created)
