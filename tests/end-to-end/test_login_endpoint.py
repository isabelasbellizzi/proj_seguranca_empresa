import requests


class TestLogin():

    def test_login_response_201_and_response_token_ok(self):

        response = requests.put("https://dev-seguranca-academy.azurewebsites.net/login", json={'email':'sergio.wellington1@transfero.com', 'senha':'Tony@123'})
        response_body = response.json()
        token = response_body["token"]
        assert response_body["token"] == token
        assert response.status_code == 201

    def test_login_response_400_error(self):

        response = requests.put("https://dev-seguranca-academy.azurewebsites.net/login", json={'email':'sergio.wellington@transfero.com', 'senha':'Tony123'})
        assert response.status_code == 400
