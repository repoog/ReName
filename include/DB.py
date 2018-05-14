#!/usr/bin/env python
try:
    import pymysql
except ImportError:
    print("[!_!]ERROR INFO: You have to install pymysql module.")
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

    def get_wuxing_name(self, wuxing_list):
        wuxing_sql = 'SELECT word FROM rn_wuxing WHERE 1 = 2'
        for word in wuxing_list:
            wuxing_sql += ' OR type="%s"' % word
        name_sql = 'SELECT a.wid, a.word FROM rn_word_unique a ' \
                   'WHERE EXISTS (SELECT b.word FROM (%s) b  WHERE SUBSTR(a.word, 1, 1) = b.word) ' \
                   'AND EXISTS (SELECT b.word FROM (%s) b  WHERE SUBSTR(a.word, 2, 1) = b.word)' % \
                   (wuxing_sql, wuxing_sql)
        self.cursor.execute(name_sql)
        name_set = self.cursor.fetchall()
        return name_set

    def match_name_word(self, name):
        name_word_sql = 'SELECT COUNT(1) FROM rn_name_word WHERE word IN ("%s", "%s")' % (name[0], name[1])
        self.cursor.execute(name_word_sql)
        match_count = self.cursor.fetchone()
        return True if match_count[0] == 2 else False

    def get_name_source(self, wid):
        source_sql = 'SELECT decade, poet, poem, content FROM rn_poem_content WHERE wid=%s'
        self.cursor.execute(source_sql, (wid))
        source = self.cursor.fetchall()
        return source[0]


if __name__ == "__main__":
    pass
