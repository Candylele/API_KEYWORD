
import requests
import jsonpath
import re

url_params = {"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}
response = requests.get( url='https://api.weixin.qq.com/cgi-bin/token',
                         params=url_params)
v = response.json()
value = jsonpath.jsonpath( v,'$.access_token' )[0]
print( value )
v = response.text
# print( v )
value = re.findall( '"access_token":"(.+?)"',v )[0]
print( value )