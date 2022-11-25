import requests
import json
import os


## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eco.settings")

## 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()

# 불러올 Django Model을 import
from comment.models import Post


def parse_api():
    page_num = 500 # 불러올 api 개수

    #def parse_api():
    url = 'http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List'
    params ={'serviceKey' : 'fxcOtnmW0mTezqetB0dx1G1KaxU7Y2ViXciJIoyVMnt13LgiM9N54UsVF4qy99JF53XXOThnBwiK22qshdYwwA==', 'pageNo' : '1', 'numOfRows' : f'{page_num}', 'type' : 'json' }

    response = requests.get(url, params=params, verify=False)

    contents = response.text

    #문자열을 json으로 변경
    json_ob = json.loads(contents)
    body = {}
    for i in range(page_num):
        body[i] = json_ob['DisasterMsg'][1]['row'][:][:][i]['md101_sn'] # create_at만 저장
        # tmp = body[i]
        # body[i] = tmp[10]
    return body


#이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':
    python_dict = parse_api()
    for t, l in python_dict.items():
        Post(post_pk=l).save()
