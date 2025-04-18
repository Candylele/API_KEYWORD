
# jsonpath是专门用来解析响应正文为json数据格式的情况
# jsonpath是一个第三方模块，需要pip install jsonpath
import jsonpath

json_obj = {'age':18,'name':'xiaohong','books':[ {'bookname':'黄帝内经'},{'bookname':'月亮与六便士'} ]}
value = jsonpath.jsonpath( json_obj,'$.name' )[0]
value1 = jsonpath.jsonpath( json_obj,'$.books[1].bookname' )
value2 = jsonpath.jsonpath( json_obj,'$.books[1].bookname' )[0]
# 解析json数据  bejson
print(value)
print(value1)
print(value2)
