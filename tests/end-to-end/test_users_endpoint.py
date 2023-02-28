from uuid import uuid4
import requests


class TestUsersEndToEnd():
    
    route = "https://seguranca-academy.azurewebsites.net/users/"
    auth = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}
    existing_user = (requests.get(f"{route}71", headers=auth)).json()["user_email"]
    azure = str(uuid4())
    email = "newemailtesttet@endtoend.com"
    email2 = "updatedemail@endtoend.com"
    
    post = {"azure_id": azure, "user_email": email}
    put = {"azure_id": azure, "user_email": email2}
    


    def test_users_no_token_forbidden_403_error(self):
        response = requests.get(self.route)
        assert response.status_code == 403

    ###CREATE###

    def test_users_post_user_and_response_201_ok(self):
        # Act
        response = requests.post(self.route, headers=self.auth, json=self.post)
        response_body = response.json()

        # Assert
        assert response_body["user_email"] == self.email
        assert response.status_code == 201

    def test_users_post_existing_user_and_response_400_error(self):
        #Arrange
        user = (requests.get(f"{self.route}", headers=self.auth)).json()[0]["user_email"]
        post_wrong = {"azure_id": self.azure, "user_email": user}
        
        # Act
        response = requests.post(self.route, headers=self.auth, json=post_wrong)
        response_body = response.json()

        # Assert
        assert response_body["msg"] == f"This email was already registered. [user_email={user}]"
        assert response.status_code == 400

    ###READ###

    def test_users_get_all_200_and_response_ok(self):
        # Arrange
        auth={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}
        
        # Act
        response = requests.get(self.route, headers=auth)
        response_body = response.json()

        # Assert
        assert response_body[0]['user_email'] == "tes4teswaggesgsgsgr4@teste.com"
        assert response.status_code == 200


    def test_users_get_single_user_200_and_response_ok(self):
        # Arrange
        auth={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}

        # Act
        response = requests.get(f"{self.route}/2", headers=auth)
        response_body = response.json()

        # Assert
        assert response_body['user_email'] == "teste@atualizado.com"
        assert response.status_code == 200
        
    def test_users_get_single_user_not_found_404_error(self):
        # Arrange
        auth={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}

        # Act
        response = requests.get(f"{self.route}/0", headers=auth)
        response_body = response.json()

        # Assert
        assert response_body['msg'] == "User not found. [user_id=0]"
        assert response.status_code == 404
  

    def test_users_get_by_email_single_user_and_response_200_ok(self):
        # Arrange
        auth={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}


        # Act
        response = requests.get(f"{self.route}email/tes4teswagger4@teste.com", headers=auth)
        response_body = response.json()

        # Assert
        assert response_body["user_id"] == 76
        assert response.status_code == 200
        
    def test_users_get_by_email_single_user_not_found_404_error(self):
        # Arrange
        auth={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}


        # Act
        response = requests.get(f"{self.route}email/fakefake@fake.com", headers=auth)
        response_body = response.json()

        # Assert
        assert response_body["msg"] == "User not found. [user_email=fakefake@fake.com]"
        assert response.status_code == 404


    ###UPDATE###

    def test_users_update_user_400_duplicated_error(self):
        # Arrange
        user = (requests.get(f"{self.route}email/{self.email}", headers=self.auth)).json()
        user_id = user["user_id"]
        user_email = user["user_email"]
        put_wrong = {"azure_id": self.azure, "user_email": user_email}

        # Act
        response = requests.put(f"{self.route}{user_id}", headers=self.auth, json=put_wrong)
        response_body = response.json()

        # Assert
        assert response_body["msg"] == f"There is already a user with that email. [user_email=[{user_email}]"
        assert response.status_code == 400
        
    def test_users_update_user_404_not_found_error(self):
        # Act
        response = requests.put(f"{self.route}0", headers=self.auth, json={"azure_id": self.azure, "user_email": "email@2.com"})
        response_body = response.json()

        # Assert
        assert response_body["msg"] == "User not found. [user_id=0]"
        assert response.status_code == 404

    def test_users_update_user_204_ok(self):
        # Arrange
        user = (requests.get(f"{self.route}email/{self.email}", headers=self.auth)).json()
        user_id = user["user_id"]

        # Act
        response = requests.put(f"{self.route}{user_id}", headers=self.auth, json=self.put)

        # Assert
        assert response.status_code == 204


    ###DELETE###

    def test_users_delete_user_204_ok(self):
        # Arrange
        user = (requests.get(f"{self.route}email/{self.email2}", headers=self.auth)).json()
        user_id = user["user_id"]

        # Act
        response = requests.delete(f"{self.route}/{user_id}", headers=self.auth)

        # Assert
        assert response.status_code == 204
        
    def test_users_delete_user_not_found_404_error(self):
        # Act
        response = requests.delete(f"{self.route}/0", headers=self.auth)

        # Assert
        assert response.status_code == 404
    
    
    
