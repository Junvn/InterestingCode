# coding:utf-8

__author__ = 'Janvn'

from wxpy import *
import unittest

'''
用python更加了解微信好友

微信公众号：python中文社区
'''

class WechatTest(unittest.TestCase):

    # #测试获取好友对象
    # def testGetObjectSet(self):
    #     bot = Bot()
    #     my_friends = bot.friends()
    #     print(type(my_friends))

    def testCountSex(self):
        '''
        测试统计好友性别数量
        :return:
        '''

        bot = Bot()
        my_friends = bot.friends()
        #print(type(my_friends))

        sex_dict = {'male':0,'female':0}
        for friend in my_friends:
            if friend.sex==1:
                sex_dict['male'] += 1
            elif friend.sex==2:
                sex_dict['female'] += 1

        print(sex_dict)


def main():
    pass


if __name__ == '__main__':
    unittest.main()