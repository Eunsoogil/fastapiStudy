import unittest
import requests
import json

'''
assertEqual(a, b)           a == b
assertNotEqual(a, b)        a != b
assertTrue(x)               bool(x) is True
assertFalse(x)              bool(x) is False
assertIs(a, b)              a is b
assertIsNot(a, b)           a is not b
assertIsNone(x)             x is None
assertIsNotNone(x)          x is not None
assertIn(a, b)              a in b
assertNotIn(a, b)           a not in b
assertIsInstance(a, b)      isinstance(a, b)
assertNotIsInstance(a, b)   not isinstance(a, b)
'''


# 테스트에서 동적으로 변할 변수들을 위해 클래스를 만든다
class VariableForTest:
    def __init__(self):
        self.header = {
            'Authorization': ''
        }
        self.post_result_id = 0


variableForTest = VariableForTest()


class UnitTestKamisDashBoard(unittest.TestCase):
    # 변하지 않을 정적 변수를 설정한다
    def setUp(self):
        self.login_url = ''
        self.login_body = {
            "id": "",
            "password": "",
            "auth_type": ""
        }
        self.test_url = ''

    # 주의 : 아래의 테스트 모듈들은 작성된 순서가 아닌 알파벳 순서로 동작한다
    # 따라서 integration test시에는 알파벳 순서에 맞게 작성한다
    # 또한, test_ 라는 이름으로 시작하지 않으면 동작되지 않는다
    def test_unittest1_login(self):
        response = requests.post(self.login_url, json=self.login_body)
        data = json.loads(response.text)
        self.assertEqual(200, response.status_code)
        # 토큰의 타입을 비교한다
        self.assertEqual(type('str'), type(data['access_token']))
        # 헤더에 붙인다
        variableForTest.header['Authorization'] = 'JWT ' + data['access_token']

    def test_unittest2_post(self):
        post_data = {
            "store_kind": "",
            "location": "",
            "crops_rank": "",
            "measure": "",
            "market_name": ""
        }
        print(variableForTest.header['Authorization'])
        response = requests.post(self.test_url, headers=variableForTest.header, json=post_data)
        data = json.loads(response.text)
        self.assertEqual(200, response.status_code)

    def test_unittest3_get(self):
        response = requests.get(self.test_url, headers=variableForTest.header)
        data = json.loads(response.text)

        # 방금 등록한 데이터의 정보를 기억한다
        variableForTest.post_result_id = data['list'][0]['id']
        self.assertEqual(200, response.status_code)

    def test_unittest4_delete(self):
        print(variableForTest.post_result_id)
        delete_data = {
            "id": variableForTest.post_result_id
        }
        response = requests.delete(self.test_url, headers=variableForTest.header, json=delete_data)
        data = json.loads(response.text)
        self.assertEqual(200, response.status_code)

    def test_unittest5_get(self):
        response = requests.get(self.test_url, headers=variableForTest.header)
        data = json.loads(response.text)
        self.assertEqual(200, response.status_code)

        # 삭제된 정보가 남아있으면 안된다
        self.assertFalse(data['list'])


if __name__ == '__main__':
    unittest.main()
