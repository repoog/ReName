# coding=utf-8

import random
import argparse
try:
    from boxcalendar import boxcalendar
except ImportError:
    print "[!_!]ERROR INFO: You have to install boxcalendar module."
    exit()

from include.DB import DBOP
from include.boxcalendar import *


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
    for index in xrange(10):
        if day_stem == sky_branch[index]:
            break

    index_X = index - 5 if index >= 5 else index
    index_Y = (hour + 1) / 2

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


def output_wuxing(year, month, day, hour):
    """
    Compute WuXing with birth datetime.
    :param year:
    :param month:
    :param day:
    :param hour:
    :param min:
    :return: attribute list
    """
    wuxing = compute_wuxing(year, month, day, hour)
    print u"[-_-] 生辰：%s年%s月%s日, %s时" % (year, month, day, hour)
    attr_list = [attr for attr in wuxing if wuxing[attr] < 2]
    print u"[-_-] 五行缺：%s\n" % ', '.join(attr_list)
    return attr_list


def output_name(attr_list):
    """
    Output rand names and poem source.
    :param attr_list:
    :return:
    """
    db_obj = DBOP()
    name_tuple = db_obj.get_wuxing_name(attr_list)  # Get all match words
    # Randomize output 5 names
    for num in xrange(5):
        index = random.randint(0, len(name_tuple)-1)
        name = name_tuple[index]
        name_source = db_obj.get_name_source(name[0])
        print u"[^_^] 候选名字%s：%s" % (str(num+1), name[1])
        print u"[*_*] 出自：\n%s\n%s(%s)\n%s\n" % \
              (name_source[2], name_source[1], name_source[0], name_source[3])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Name children with birth datetime and WuXing balance.")
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
    output_name(attr_list)
