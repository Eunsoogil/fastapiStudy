import pytest
from buildthing import app
import requests
import json


# 테스트에서 동적으로 변할 변수들을 위해 클래스를 만든다
class VariableForTest:
    def __init__(self):
        self.header = {
            'Authorization': ''
        }
        self.post_result_id = 0


variableForTest = VariableForTest()

login_url = ''
login_body = {
    "id": "",
    "password": "",
    "auth_type": ""
}
test_url = ''


@pytest.fixture
def api():
    api = app.test_client()

    return api


# @pytest.mark.dependency()
def test_pytest_login(api):
    response = requests.post(login_url, json=login_body)
    data = json.loads(response.text)
    assert 200 == response.status_code
    # 토큰의 타입을 비교한다
    assert type('str') == type(data['access_token'])
    # 헤더에 붙인다
    variableForTest.header['Authorization'] = 'JWT ' + data['access_token']


# 기본적으로 작성순으로 동작하지만, 아래와 같이 특정 모듈이 된 이후에 실행하도록 설정할 수도 있다
# @pytest.mark.dependency(depends=['test_pytest_login'])
def test_pytest_post(api):
    post_data = {
        "store_kind": "",
        "location": "",
        "crops_rank": "",
        "measure": "",
        "market_name": ""
    }
    print(variableForTest.header['Authorization'])
    response = requests.post(test_url, headers=variableForTest.header, json=post_data)
    data = json.loads(response.text)
    assert 200 == response.status_code


# @pytest.mark.dependency(depends=['test_pytest_post'])
def test_pytest_get1(api):
    response = requests.get(test_url, headers=variableForTest.header)
    data = json.loads(response.text)

    # 방금 등록한 데이터의 정보를 기억한다
    variableForTest.post_result_id = data['list'][0]['id']
    assert 200 == response.status_code


# @pytest.mark.dependency(depends=['test_pytest_get1'])
def test_pytest_delete(api):
    print(variableForTest.post_result_id)
    delete_data = {
        "id": variableForTest.post_result_id
    }
    response = requests.delete(test_url, headers=variableForTest.header, json=delete_data)
    data = json.loads(response.text)
    assert 200 == response.status_code


# @pytest.mark.dependency(depends=['test_pytest_delete'])
def test_pytest_get2(api):
    response = requests.get(test_url, headers=variableForTest.header)
    data = json.loads(response.text)
    assert 200 == response.status_code

    # 삭제된 정보가 남아있으면 안된다
    assert not data['list']
