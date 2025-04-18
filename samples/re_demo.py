#!/usr/bin/env python
# encoding: utf-8
# @author: liusir
# @file: re_demo.py
# @time: 2021/7/14 8:24 下午

import re
# 正则基础及应用

source_str = 'newdream123'
print( source_str[3:8] )

# 写法一：
pattern = re.compile(r'newdream')  # 创建pattern对象
result = re.match( pattern , source_str )
print( result )

# 写法二：
result = re.search( 'dream' , source_str)
print( result )

# match ：匹配开头部分
# search : 扫描整个str进行匹配
# split :  按照能够匹配的子串进行分割，返回的是列表
# findall: 扫描整个str进行匹配,并把所有匹配项做成一个列表返回
source_str_1 = 'china&usa&english'
print( source_str_1.split('&') )
print(  re.split('&',source_str_1) )

source_str_2 = 'china123usa10english'
print( re.split('\d+',source_str_2) )

source_str_3 = '123456newdream789aaa000'
print( re.findall('\D+',source_str_3) )

