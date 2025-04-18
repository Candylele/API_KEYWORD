#!/usr/bin/env python
# encoding: utf-8
# @author: liusir
# @file: pytest_demo.py
# @time: 2021/7/25 4:30 下午

data_list = [
    {'case_id':"case01",'case_step':[1,2]},
    {'case_id':"case02",'case_step':[3,4]},
    {'case_id':"case03",'case_step':[5,6]}
]

lista = ["hello",'world','xiaoming']
print( ";".join(lista) )

listb = data_list[0].keys()
print( ','.join(listb) )

case_list = []
for data in data_list:
    case_list.append( tuple(data.values()) )
print( case_list )
