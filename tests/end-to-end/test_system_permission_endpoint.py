import requests

class TestSystemPermissionsEndToEnd():

    host = "https://dev-seguranca-academy.azurewebsites.net/"
    route = "https://dev-seguranca-academy.azurewebsites.net/system_permissions/"
    auth = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}


    def test_get_no_token_error(self):
        response = requests.get(f"{self.route}1")
        assert response.status_code == 403
        
    def test_get_wrong_params_error(self):
        response = requests.get(f"{self.route}abc", headers=self.auth)
        assert response.status_code == 422
        
    def test_get_not_found_error(self):
        response = requests.get(f"{self.route}0", headers=self.auth)
        assert response.status_code == 404
        
    def test_get_ok(self):
        response = requests.get(f"{self.route}1", headers=self.auth)
        assert response.status_code == 200