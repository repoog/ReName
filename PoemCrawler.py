try:
    import threadpool
except ImportError:
    print("[!_!]ERROR INFO: You have to install threadpool module.")
    exit()

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("[!_!]ERROR INFO: You have to install bs4 module.")
    exit()

import requests
from threading import *

from include.DB import DBOP


class POEM_CRAWLER(object):
    def __init__(self):
        self.host = "http://www.shicimingju.com"
        self.db_obj = DBOP()
        self.store_lock = Semaphore()

    def decade_poet(self):
        page_html = requests.get(self.host + "/category/all")
        page_html = page_html.content
        parse_file = BeautifulSoup(page_html, 'lxml')
        decade_list = parse_file.select('div.www-main-container > div:nth-of-type(1) > a')
        decade_list = decade_list[1:]

        thread_list = []
        did = 1
        # Couldn't use enumerate because of overwriting by threading package
        for decade in decade_list:
            t = Thread(target=self.__store_poet, args=(did, decade.get_text(), decade.get('href'),))
            t.start()
            thread_list.append(t)
            did += 1

        for thread in thread_list:
            thread.join()

    def __store_poet(self, did, decade, decade_uri):
        self.store_lock.acquire()
        self.db_obj.record_decade(did, decade)

        page = 1
        while 1:
            poet_list = self.__poet_crawler(did, decade_uri + '__' + str(page))
            if poet_list:
                self.db_obj.record_person(poet_list)
            else:
                break
            page += 1
        self.store_lock.release()

    def __poet_crawler(self, did, decade_uri):
        page_html = requests.get(self.host + decade_uri)
        page_html = page_html.content
        parse_file = BeautifulSoup(page_html, 'lxml')
        person_list = parse_file.select('h3 > a')

        if not person_list:
            return None

        poet_list = []
        for person in person_list:
            poet_list.append([did, person.get_text(), person['href']])

        return poet_list

    def poet_works(self):
        # Get all poet id and his/her works uri
        count = 0
        while 1:
            poet_tuple = self.db_obj.get_person(count)
            if not poet_tuple:
                break
            thread_list = []
            for poet in poet_tuple:
                t = Thread(target=self.__store_works, args=(poet[0], poet[1],))
                t.start()
                thread_list.append(t)
            for thread in thread_list:
                thread.join()
            count += 1

    def __store_works(self, pid, poet_uri):
        self.store_lock.acquire()
        page = 1
        while 1:
            works_list = self.__works_crawler(pid, poet_uri.replace('.', '_' + str(page) + '.'))
            if works_list:
                self.db_obj.record_poem(works_list)
            else:
                break
            page += 1
        self.store_lock.release()

    def __works_crawler(self, pid, uri):
        try:
            page_html = requests.get(self.host + uri, timeout=10)
        except requests.exceptions.ConnectionError:
            print(pid, uri)
            return None
        except requests.exceptions.ReadTimeout:
            print(pid, uri)
            return None
        page_html = page_html.content
        parse_file = BeautifulSoup(page_html, 'lxml')
        poem_list = parse_file.select('h3 > a')
        if not poem_list:
            return None

        works_list = []
        for poem in poem_list:
            works_list.append([pid, poem.get_text().strip(), poem['href']])

        return works_list

    def poem_content(self):
        # Get all poet id and his/her works uri
        count = 0
        while 1:
            poem_tuple = self.db_obj.get_works(count)
            if not poem_tuple:
                break
            thread_list = []
            for poem in poem_tuple:
                t = Thread(target=self.__content_crawler, args=(poem[0], poem[1],))
                t.start()
                thread_list.append(t)
            for thread in thread_list:
                thread.join()
            count += 1

    def __content_crawler(self, wid, poem_uri):
        self.store_lock.acquire()
        try:
            page_html = requests.get(self.host + poem_uri, timeout=10)
            page_html = page_html.content
            parse_file = BeautifulSoup(page_html, 'lxml')
            content = parse_file.select('.shici-content')
        except ConnectionError as e:
            print("ConnectionError: %s, %s" % (wid, poem_uri))
        except TimeoutError as e:
            print("TimeoutError: %s, %s" % (wid, poem_uri))
        else:
            try:
                self.db_obj.record_content(wid, content[0].get_text().strip())
            except IndexError as e:
                print("IndexError: %s, %s" % (wid, poem_uri))
        self.store_lock.release()


if __name__ == '__main__':
    # Record decade and person information with crawler uri
    poem_obj = POEM_CRAWLER()
    # Crawling decade and poet information
    # poem_obj.decade_poet()
    # # Crawling each poem title and uri of poet
    # poem_obj.poet_works()
    # # Crawling each poem content of poem
    poem_obj.poem_content()
