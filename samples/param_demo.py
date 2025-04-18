#!/usr/bin/env python
# encoding: utf-8
# @author: liusir
# @file: param_demo.py
# @time: 2021/7/18 2:55 下午

import unittest
import paramunittest

# @paramunittest.parametrized(
#     (100,80,180),
#     (30,40,70),
#     (60,90,150)
# )
# @paramunittest.parametrized(
#     {'numa':100,'numb':80,'numc':180},
#     {'numa':30,'numb':40,'numc':70},
#     {'numa':60,'numb':90,'numc':150}
# )
# test_data = [{'numa':100,'numb':80,'numc':180},{'numa':30,'numb':40,'numc':70},{'numa':60,'numb':90,'numc':150}]
def get_data():
    test_data = [{'numa':100,'numb':80,'numc':180,'case_name':'测试用例01'},{'numa':30,'numb':40,'numc':70,'case_name':'测试用例02'},{'numa':60,'numb':90,'numc':150,'case_name':'测试用例03'}]
    return test_data
@paramunittest.parametrized(
    *get_data()
)
class ParamDemo(paramunittest.ParametrizedTestCase):  # unittest.TestCase
    def setParameters(self, numa,numb,numc,case_name):
        self.a = numa
        self.b = numb
        self.c = numc
        self.case_name = case_name
    def test_add_case(self):
        self._testMethodName = self.case_name
        print('%d+%d?=%d'%(self.a,self.b,self.c))
        self.assertEqual( self.a + self.b ,self.c )
if __name__=="__main__":
    unittest.main(verbosity=2)