#!/usr/bin/env python
# coding = utf-8

try:
    import MySQLdb
except ImportError:
    print "[!_!]ERROR INFO: You have to install MySQLdb module."
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
        self.db = MySQLdb.connect(HOST, USER, PASS, DATABASE, PORT, charset='utf8')
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def record_decade(self, did, decade):
        try:
            decade_sql = 'INSERT INTO rn_decade(did, decade) VALUES(%s, %s)'
            self.cursor.execute(decade_sql, [did, decade])
            self.db.commit()
        except MySQLdb.IntegrityError:
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

    def get_wuxing_name(self, wuxing_list):
        wuxing_sql = 'SELECT word FROM rn_wuxing WHERE 1 and 1'
        for word in wuxing_list:
            wuxing_sql += ' OR type="%s"' % (word.encode('utf-8'))
        name_sql = 'SELECT wid, word FROM rn_word_unique ' \
                   'WHERE SUBSTR(word, 1, 1) IN (%s) AND SUBSTR(word, 2, 1) IN (%s)' % (wuxing_sql, wuxing_sql)
        self.cursor.execute(name_sql)
        name_set = self.cursor.fetchall()
        return name_set

    def get_name_source(self, wid):
        source_sql = 'SELECT decade, poet, poem, content FROM rn_poem_content WHERE wid=%s'
        self.cursor.execute(source_sql, (wid))
        source = self.cursor.fetchall()
        return source[0]

if __name__ == "__main__":
    pass
