# coding:utf-8

__author__ = 'Janvn'

from wxpy import *
import unittest
import re
import jieba
import pandas as pd
import numpy
from scipy.misc import imread
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt

'''
用python更加了解微信好友

微信公众号：python中文社区
'''

class WechatTest(unittest.TestCase):

    # def testGetObjectSet(self):
    #     '''
    #     测试获取好友对象
    #     :return:
    #     '''
    #     bot = Bot()
    #     my_friends = bot.friends()
    #     print(type(my_friends))


    # def testCountSex(self):
    #     '''
    #     测试统计好友性别数量
    #     :return:
    #     '''
    #
    #     bot = Bot()
    #     my_friends = bot.friends()
    #     #print(type(my_friends))
    #
    #     sex_dict = {'male':0,'female':0}
    #     for friend in my_friends:
    #         if friend.sex==1:
    #             sex_dict['male'] += 1
    #         elif friend.sex==2:
    #             sex_dict['female'] += 1
    #
    #     print(sex_dict)


    # def testCountArea(self):
    #     '''
    #     统计好友分布区域
    #     :return:
    #     '''
    #
    #     #使用字典统计各省份好友数量
    #     province_dict = {'北京': 0, '上海': 0, '天津': 0, '重庆': 0, '河北': 0, '山西': 0, '吉林': 0,
    #                      '辽宁': 0, '黑龙江': 0, '陕西': 0, '甘肃': 0, '青海': 0, '山东': 0, '福建': 0,
    #                      '浙江': 0, '台湾': 0, '河南': 0, '湖北': 0, '湖南': 0, '江西': 0,'江苏': 0,
    #                      '安徽': 0, '广东': 0, '海南': 0, '四川': 0, '贵州': 0, '云南': 0, '内蒙古': 0,
    #                      '新疆': 0, '宁夏': 0, '广西': 0, '西藏': 0, '香港': 0, '澳门': 0}
    #
    #     bot = Bot()
    #     my_friends = bot.friends()
    #
    #     # 统计省份
    #     for friend in my_friends:
    #         if friend.province in province_dict.keys():
    #             province_dict[friend.province] += 1
    #         print(province_dict)
    #
    #     # 生成json array格式
    #     data = []
    #     for key,value in province_dict.items():
    #         data.append({'name':key,'value':value})
    #     print(data)


    # def write_txt_file(self,path,txt):
    #     '''
    #     写入txt
    #     :param path:
    #     :param txt:
    #     :return:
    #     '''
    #     with open(path,'a',encoding='gb18030',newline='') as f:
    #         f.write(txt)


    # def testCountSign(self):
    #     '''
    #     统计好友签名，写入到signtures.txt文件中
    #     :return:
    #     '''
    #     bot = Bot()
    #     my_friends = bot.friends()
    #     for friend in my_friends:
    #         # 对数据进行清洗，将标点符号等对词频统计造成影响的因素剔除
    #         pattern = re.compile(r'[一-龥]+')
    #         filterdata = re.findall(pattern,friend.signature)
    #
    #         with open('signatures.txt','a',encoding='utf8',newline='') as f:
    #             f.write(''.join(filterdata))

    def testCountWord(self):
        '''
        通过词频统计生成词云
        :return:
        '''
        with open('signatures.txt','r',encoding='utf8',newline='') as f:
            content = f.read()
            segment = jieba.lcut(content)
            words_df = pd.DataFrame({'segment':segment})

            stopwords = pd.read_csv("stopwords.txt",index_col=False,quoting=3,sep=" ",names=['stopword'],encoding='utf8')
            words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

            words_stat = words_df.groupby(by=['segment'])['segment'].agg({'计数':numpy.size})
            words_stat = words_stat.reset_index().sort_values(by=['计数'],ascending=False)
            # print(words_df)

            #设置词云属性
            color_mask=imread('background.jfif')
            # wordcloud=WordCloud(background_color='white',
            #                     max_words=100,
            #                     mask=color_mask,
            #                     max_font_size=100,
            #                     random_state=42,
            #                     width=1000,height=860,margin=2,
            #                     )

            wordcloud = WordCloud(font_path='simhei.ttf',   #从网上下载simhei.ttf字体文件
                                  background_color='white',
                                  max_words=100,
                                  mask=color_mask,
                                  max_font_size=100,
                                  random_state=42,
                                  width=1000, height=860, margin=2,
                                  )

            # word_frequence=dict()
            # for x in words_stat.head(100).values:
            #     word_frequence[x[0]]=x[1]

            word_frequence={x[0]:x[1] for x in words_stat.head(100).values}
            #print(word_frequence)

            word_frequence_dict={}
            for key in word_frequence:
                word_frequence_dict[key] = word_frequence[key]
            print(word_frequence_dict)

            wordcloud.generate_from_frequencies(word_frequence_dict)
            image_colors = ImageColorGenerator(color_mask)
            wordcloud.recolor(color_func=image_colors)
            wordcloud.to_file('output.png')
            plt.imshow(wordcloud)
            plt.axis('off')
            plt.show()

def main():
    pass


if __name__ == '__main__':
    unittest.main()
