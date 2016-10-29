#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

class Generator(object):

    def __init__(self,n):
        self.n = n
        self.num , self.nums = 0 ,[]

    def __iter__(self):
        return self


