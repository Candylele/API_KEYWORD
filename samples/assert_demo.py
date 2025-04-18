
import json

# 检查json中的字段
import re

str_01 ='{"access_token":"47_drbApL6nqZOJMNB2EOGccMcSvZyi0zGBaEuLB37bkcdQIrk38lkSDUSxuVl6ITLHhmQVGFfZVaYlf9vbU_PSaw4Cmn8GCiJtVHuKz00soJMcrFwA7nSAvStrUVYY4AXlkOgmOJ8UcM-7vBRTTZJhAGAZFP","expires_in":7200}'
json_obj = json.loads( str_01 )  # 将JSON格式数据反序列化为python对象，如字典，列表，数字等
if 'access_token' in json_obj.keys():
    print( True )
else:
    print( False )

check_keys = ['access_token','expires_in']
tmp_result = []
for check_key in check_keys:
    if check_key in str_01:
        tmp_result.append(True)
    else:
        tmp_result.append(False)
if False in tmp_result:
    print( False )
if True in tmp_result:
    print(True)

# 检查json中的key_value对应字段
str_01 ='{"access_token":"47_drbApL6nqZOJMNB2EOGccMcSvZyi0zGBaEuLB37bkcdQIrk38lkSDUSxuVl6ITLHhmQVGFfZVaYlf9vbU_PSaw4Cmn8GCiJtVHuKz00soJMcrFwA7nSAvStrUVYY4AXlkOgmOJ8UcM-7vBRTTZJhAGAZFP","expires_in":7200}'
json_obj = json.loads( str_01 )

check_key = '{"expires_in":7200}'  # ==>字符串
check_key_obj = json.loads( check_key ) # ==》字典
check_items = check_key_obj.items() # ==> 获取item对象
print( check_items )
print( json_obj.items() )

for check_item in check_items:
    if check_item in json_obj.items():
        print(True)
    else:
        print(False)

#a = 10 ;  a in [8,9,10]  ;  a = [10] ; a in [8,9,10]

str_01 ='{"access_token":"47_drbApL6nqZOJMNB2EOGccMcSvZyi0zGBaEuLB37bkcdQIrk38lkSDUSxuVl6ITLHhmQVGFfZVaYlf9vbU_PSaw4Cmn8GCiJtVHuKz00soJMcrFwA7nSAvStrUVYY4AXlkOgmOJ8UcM-7vBRTTZJhAGAZFP","expires_in":7200}'
reg_str = '"access_token":(.+?)"'
match = re.search( reg_str,str_01 )
if match:
    print(match.group(1))
    print( True )
else:
    print( False )


# str_01 ='{"access_token":"47_drbApL6nqZOJMNB2EOGccMcSvZyi0zGBaEuLB37bkcdQIrk38lkSDUSxuVl6ITLHhmQVGFfZVaYlf9vbU_PSaw4Cmn8GCiJtVHuKz00soJMcrFwA7nSAvStrUVYY4AXlkOgmOJ8UcM-7vBRTTZJhAGAZFP","expires_in":7200}'
# reg_str = '"access_token":47(.+?)"'
# if re.findall( reg_str,str_01 ) :
#     print( True )
# else:
#     print( False )



