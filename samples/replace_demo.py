#!/usr/bin/env python
# encoding: utf-8
# @author: liusir
# @file: replace_demo.py
# @time: 2021/7/14 9:30 下午

import re

tmp_variables = {'token_value': '47_q9bceTVwE-xz_15eckX4yWDwmwHpTbvWoSCfo0GSyEAR4WYZCnhEcxQozsnGSHiiZByJPh64cREbHRhDDS_PpAcR9xvlGRNYo3y47I5llfpk8TFf9HpsnJDAy8d0wmVWSTF_Xx9HNAKnAfwLRSOdAAADEA'}
str_01 = '{"access_token":"${token_value}"}'
value = re.findall('\\${\w+}',str_01)[0]
print( value )
str_01 = str_01.replace( value , tmp_variables[value[2:-1]] )
print( str_01 )

tmp_variables = {"token":"123","n1":"456"}
str_02 = '{"access_token":"${token}"},${n1}' #?
for v in re.findall('\\${\w+}',str_02):
    str_02 = str_02.replace( v,tmp_variables[v[2:-1]] )
print( str_02 )



# .....?
str_01 = '{"access_token":"47_q9bceTVwE-xz_15eckX4yWDwmwHpTbvWoSCfo0GSyEAR4WYZCnhEcxQozsnGSHiiZByJPh64cREbHRhDDS_PpAcR9xvlGRNYo3y47I5llfpk8TFf9HpsnJDAy8d0wmVWSTF_Xx9HNAKnAfwLRSOdAAADEA"}'


