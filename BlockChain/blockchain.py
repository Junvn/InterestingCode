#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:janvn
# datetime:18-8-4 上午9:27
# software:PyCharm


Class BlockChain(object):
    def __init__(self):
        '''
        初始构造函数
        :param self:
        :return:
        '''
        self.chain=[] #存储区块链
        self.current_transactions=[] #保存交易

    def new_block(self):
        '''
        创建新的区块并且增加其到链
        :param self:
        :return:
        '''
        pass

    def new_transactions(self):
        '''
        增加新的交易到交易列表中
        :param self:
        :return:
        '''
        pass