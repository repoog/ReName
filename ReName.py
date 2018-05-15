try:
    from bs4 import BeautifulSoup
except ImportError:
    print("[!_!]ERROR INFO: You have to install bs4 module.")
    exit()

try:
    import requests
except ImportError:
    print("[!_!]ERROR INFO: You have to install requests module.")
    exit()

try:
    import ngender
except ImportError:
    print("[!_!]ERROR INFO: You have to install ngender module.")
    exit()

import argparse
import sys
import signal
from random import randint
from lib.DB import DBOP
from lib.boxcalendar import *

SCORE_LINE = 95


def compute_wuxing(year, month, day, hour):
    horoscope = lunarday(year, month, day)
    day_stem = horoscope[2].split('-')[2][0]

    time_stem_branch_list = [
        [u"甲子",u"丙子", u"戊子", u"庚子", u"壬子"],
        [u"乙丑",u"丁丑", u"己丑", u"辛丑", u"癸丑"],
        [u"丙寅",u"戊寅", u"庚寅", u"壬寅", u"甲寅"],
        [u"丁卯",u"己卯", u"辛卯", u"癸卯", u"乙卯"],
        [u"戊辰",u"庚辰", u"壬辰", u"甲辰", u"丙辰"],
        [u"己巳",u"辛巳", u"癸巳", u"己巳", u"丁巳"],
        [u"庚午", u"壬午",u"甲午", u"丙午", u"戊午"],
        [u"辛未",u"癸未", u"乙未", u"丁未", u"己未"],
        [u"壬申",u"甲申", u"丙申", u"戊申", u"庚申"],
        [u"癸酉",u"乙酉", u"丁酉", u"己酉", u"辛酉"],
        [u"甲戌",u"丙戌", u"戊戌", u"庚戌", u"壬戌"],
        [u"乙亥",u"丁亥", u"己亥", u"辛亥", u"癸亥"]
    ]
    sky_branch = [u'甲', u'乙', u'丙', u'丁', u'戊', u'己', u'庚', u'辛', u'壬', u'癸']

    index = 0
    for index in range(10):
        if day_stem == sky_branch[index]:
            break

    index_X = index - 5 if index >= 5 else index
    index_Y = int((hour + 1) / 2)

    # Generate horoscope
    horoscope = horoscope[2] + '-' + time_stem_branch_list[index_Y][index_X]

    wuxing_dic = {
        u"金": [u"申", u"酉", u"庚", u"辛"],
        u"木": [u"寅", u"卯", u"甲", u"乙"],
        u"水": [u"子", u"亥", u"壬", u"癸"],
        u"火": [u"巳", u"午", u"丙", u"丁"],
        u"土": [u"辰", u"戌", u"丑", u"未", u"戊", u"己"]
    }
    wuxing = {}
    horoscope_list = list(''.join(horoscope.split('-')))
    for key, value in wuxing_dic.items():
        count = 0
        for item in horoscope_list:
            if item in value:
                count += 1
        wuxing[key] = count
    return wuxing


def name_score(name, sur_type=1):
    """
    Get number of name from 1518.com
    :param name: full name
    :param sur_type: surname single(1) or double(2)
    :return: name score
    """
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
              'User-Agent': 'Chrome/63.0.3239.84 Safari/537.36'
              }
    name = str(name.encode('gbk')).split("'")[1].replace('\\x', '%')
    name_url = 'http://m.1518.com/xingming_view.php?word={}&submit1=&FrontType={}'
    page_html = requests.get(name_url.format(name, sur_type), headers=header)
    page_html = page_html.content
    parse_file = BeautifulSoup(page_html, 'lxml')
    name_score = parse_file.select('dt > u strong')
    try:
        score = name_score[0].text.split('分')[0]
    except IndexError:
        score = 0
    finally:
        score = int(score)
    return True if score > SCORE_LINE else False


def output_wuxing(year, month, day, hour):
    """
    Compute WuXing with birth datetime.
    :param year:
    :param month:
    :param day:
    :param hour:
    :return: attribute list
    """
    wuxing = compute_wuxing(year, month, day, hour)
    print("[*] 出生日期：%s年%s月%s日, %s时" % (year, month, day, hour))
    attr_list = [attr for attr in wuxing if wuxing[attr] < 2]
    name_attr = list(set(['金', '木', '水', '火', '土']) - set(attr_list))
    print("[*] 五行属性：%s\n" % ', '.join(name_attr))
    return attr_list


def filter_name(surname, gender, attr):
    """
    Filter names with gender, general name word and name score.
    :param surname: surname of name.
    :param gender: gender of name.
    :param attr: attribute list of name.
    :return: None
    """
    sur_type = 1 if len(surname) == 1 else 2
    db_obj = DBOP()
    name_tuple = db_obj.get_wuxing_name(attr)  # Get all match words
    match_count = 0
    while 1:
        if match_count == 5:
            break
        name_info = name_tuple[randint(0, len(name_tuple))]
        name_id, name = name_info[0], name_info[1]
        full_name = surname + name
        # Match gender and general name word.
        if gender != ngender.guess(full_name)[0][0].upper() or not db_obj.match_name_word(name):
            continue
        if not name_score(full_name, sur_type):
            continue
        print("[-] 候选名字：%s" % full_name)
        match_count += 1
        name_source = db_obj.get_name_source(name_id)
        print("[-] 名字出处：")
        print(name_source[2])
        print(name_source[1] + '(' + name_source[0] + ')')
        print(name_source[3])
        print('\n')


def sigint_handler(signum, frame):
    print('You pressed the Ctrl+C.')
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)

    parser = argparse.ArgumentParser(description="Name children with birth datetime and WuXing balance.")
    parser.add_argument("-s", metavar="surname", required=True, help="Surname.")
    parser.add_argument("-g", metavar="gender", choices=('F', 'M'), required=True, help="Gender(F/M).")
    parser.add_argument("-y", type=int, choices=range(1901, 2049), metavar="year", required=True,
                        help="Year of birth date.")
    parser.add_argument("-m", type=int, choices=range(1, 13), metavar="month", required=True,
                        help="Month of birth date.")
    parser.add_argument("-d", type=int, choices=range(1, 32), metavar="day", required=True,
                        help="Day of birth date.")
    parser.add_argument("-H", type=int, choices=range(0, 24), metavar="hour", required=True,
                        help="Hour of birth datetime.")
    args = parser.parse_args()

    attr_list = output_wuxing(args.y, args.m, args.d, args.H)
    filter_name(args.s, args.g, attr_list)
