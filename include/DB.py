#!/usr/bin/env python
<<<<<<< HEAD
try:
    import pymysql
except ImportError:
    print("[!_!]ERROR INFO: You have to install pymysql module.")
=======
# coding = utf-8

try:
    import pymysql
except ImportError:
    print("[!_!]ERROR INFO: You have to install MySQLdb module.")
>>>>>>> e866df66cee25f71b9bc9910ae65becef7fcfed4
    exit()

HOST = "localhost"
PORT = 3306
USER = "rename"
PASS = "/*F0rCh1ldN@m3*/"
DATABASE = "rename"


class DBOP(object):
    """
    MySQL operation class for logging command logs and searching logs
    """
    def __init__(self):
        try:
            self.db = pymysql.connect(HOST, USER, PASS, DATABASE, PORT, charset='utf8')
        except pymysql.OperationalError as e:
            print(e)
            exit()
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

<<<<<<< HEAD
=======
    def record_decade(self, did, decade):
        try:
            decade_sql = 'INSERT INTO rn_decade(did, decade) VALUES(%s, %s)'
            self.cursor.execute(decade_sql, [did, decade])
            self.db.commit()
        except pymysql.IntegrityError:
            pass

    def record_person(self, poet_list):
        person_sql = 'INSERT INTO rn_person(did, name, uri) VALUES(%s, %s, %s)'
        self.cursor.executemany(person_sql, poet_list)
        self.db.commit()

    def get_person(self):
        person_sql = 'SELECT pid, uri FROM rn_person'
        self.cursor.execute(person_sql)
        poet_set = self.cursor.fetchall()
        return poet_set

    def record_poem(self, works_list):
        poem_sql = 'INSERT INTO rn_poem(pid, title, uri) VALUES(%s, %s, %s)'
        self.cursor.executemany(poem_sql, works_list)
        self.db.commit()

    def get_works(self, offset):
        works_sql = 'SELECT wid, uri FROM rn_poem LIMIT %s, 10000'
        self.cursor.execute(works_sql, [offset * 10000])
        poem_set = self.cursor.fetchall()
        return poem_set

    def record_content(self, wid, content):
        poem_sql = 'INSERT INTO rn_content(wid, content) VALUES(%s, %s)'
        self.cursor.execute(poem_sql, [wid, content])
        self.db.commit()

    def get_content(self, offset):
        content_sql = 'SELECT wid, content FROM rn_content LIMIT %s, 5000'
        self.cursor.execute(content_sql, [offset * 5000])
        poem_set = self.cursor.fetchall()
        return poem_set

    def record_word(self, wid, word):
        word_sql = 'INSERT INTO rn_word(wid, word) VALUES(%s, %s)'
        self.cursor.execute(word_sql, [wid, word])
        self.db.commit()

>>>>>>> e866df66cee25f71b9bc9910ae65becef7fcfed4
    def get_wuxing_name(self, wuxing_list):
        wuxing_sql = 'SELECT word FROM rn_wuxing WHERE 1 and 1'
        for word in wuxing_list:
            wuxing_sql += ' OR type="%s"' % word
<<<<<<< HEAD
        name_sql = 'SELECT DISTINCT word FROM rn_word ' \
=======
        name_sql = 'SELECT wid, word FROM rn_word_unique ' \
>>>>>>> e866df66cee25f71b9bc9910ae65becef7fcfed4
                   'WHERE SUBSTR(word, 1, 1) IN (%s) AND SUBSTR(word, 2, 1) IN (%s)' % (wuxing_sql, wuxing_sql)
        self.cursor.execute(name_sql)
        name_set = self.cursor.fetchall()
        return name_set

<<<<<<< HEAD
    def match_name_word(self, name):
        name_word_sql = 'SELECT COUNT(1) FROM rn_name_word WHERE word="%s" OR word="%s"' % (name[0], name[1])
        self.cursor.execute(name_word_sql)
        match_count = self.cursor.fetchone()
        return True if match_count[0] == 2 else False

    def get_name_source(self, name):
        source_sql = 'SELECT decade, poet, poem, content FROM rn_poem_content WHERE wid IN ' \
                     '(SELECT wid FROM rn_word WHERE word = %s)'
        self.cursor.execute(source_sql, (name))
        source = self.cursor.fetchall()
        return source[0]


=======
    def get_name_source(self, wid):
        source_sql = 'SELECT decade, poet, poem, content FROM rn_poem_content WHERE wid=%s'
        self.cursor.execute(source_sql, (wid))
        source = self.cursor.fetchall()
        return source[0]

>>>>>>> e866df66cee25f71b9bc9910ae65becef7fcfed4
if __name__ == "__main__":
    pass
