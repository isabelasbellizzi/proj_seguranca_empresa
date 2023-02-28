import requests


class TestSystemsEndToEnd():

    def test_systems_no_token_forbidden_403_error(self):
        response = requests.get("https://dev-seguranca-academy.azurewebsites.net/systems")
        assert response.status_code == 403

    ###CREATE###
    
    def test_systems_post_and_response_201_ok(self):
        # Arrange
        auth={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}
        post={"system_name": "system", "token_id": "89093123-732c-44e8-92a6-46c36811f567"}

        # Act
        response = requests.post("https://dev-seguranca-academy.azurewebsites.net/systems/", headers=auth, json=post)
        response_body = response.json()

        # Assert
        assert response_body["system_name"] == "system"
        assert response.status_code == 201
    
    ###READ###

    def test_systems_get_system_200_and_response_ok(self):
        # Arrange
        auth={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}

        # Act
        response = requests.get("https://dev-seguranca-academy.azurewebsites.net/systems/261", headers=auth)
        response_body = response.json()

        assert response_body["system_name"] == "Test System"
        assert response.status_code == 200

    def test_systems_get_all_200_and_response_ok(self):
        # Arrange
        auth={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}

        # Act
        response = requests.get("https://dev-seguranca-academy.azurewebsites.net/systems/", headers=auth)
        response_body = response.json()

        assert response_body[0]["system_name"] == "Controle do Fumo 2"
        assert response.status_code == 200

    def test_systems_get_all_max_records_params_200_and_response_ok(self):
        # Arrange
        auth={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}

        # Act
        response = requests.get("https://dev-seguranca-academy.azurewebsites.net/systems/?max_records=1", headers=auth)
        response_body = response.json()

        assert response_body[0]["system_name"] == "Controle do Fumo 2"
        assert response.status_code == 200
        
    def test_systems_get_all_system_name_params_200_and_response_ok(self):
        # Arrange
        auth={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}

        # Act
        response = requests.get("https://dev-seguranca-academy.azurewebsites.net/systems/?system_name=system", headers=auth)
        response_body = response.json()

        assert response_body[0]["system_name"] == "system"
        assert response.status_code == 200

    def test_systems_get_all_system_status_params_200_and_response_ok(self):
        # Arrange
        auth={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}

        # Act
        response = requests.get("https://dev-seguranca-academy.azurewebsites.net/systems/?system_status=1", headers=auth)
        response_body = response.json()

        assert response_body[0]["system_name"] == "Controle do Fumo 2"
        assert response.status_code == 200
        
    ###UPDATE###
    
    def test_systems_update_system_204_ok(self):
        # Arrange
        auth={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}
        put={"token_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6","system_name": "update"}

        # Act
        response = requests.put("https://dev-seguranca-academy.azurewebsites.net/systems/262", headers=auth, json=put)

        # Assert
        assert response.status_code == 204
        
    
    ###DELETE###
    
    def test_systems_delete_system_204_ok(self):
        # Arrange
        auth={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}

        # Act
        response = requests.delete("https://dev-seguranca-academy.azurewebsites.net/systems/262", headers=auth)

        # Assert
        assert response.status_code == 204
        