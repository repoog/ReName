try:
    import jieba
except ImportError:
    print("ERROR: You should install jieba module.")
    exit()

from threading import *
from include.DB import DBOP

db_obj = DBOP()
store_lock = Semaphore()


def record_word(poem):
    store_lock.acquire()
    word_list = jieba.lcut_for_search(poem[1])
    for word in word_list:
        if len(word) == 2:
            db_obj.record_word(poem[0], word)
    store_lock.release()


def cut_poem():
    count = 0
    while 1:
        poem_tuple = db_obj.get_content(count)
        if not poem_tuple:
            break
        thread_list = []
        for poem in poem_tuple:
            t = Thread(target=record_word, args=(poem,))
            t.start()
            thread_list.append(t)
        for thread in thread_list:
            thread.join()
        count += 1


if __name__ == '__main__':
    cut_poem()
