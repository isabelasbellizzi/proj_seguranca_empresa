import requests


class TestHealthcheck():

    def test_healthcheck_response_200_ok(self):
        response = requests.get("https://dev-seguranca-academy.azurewebsites.net/")
        assert response.status_code == 200

    def test_healthcheck_return_ok(self):
        response = requests.get("https://dev-seguranca-academy.azurewebsites.net/")
        response_body = response.json()
        assert response_body["name"] == "Seguranca"
    
