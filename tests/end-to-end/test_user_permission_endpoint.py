from uuid import uuid4
import requests
from faker import Faker
import random

class TestUserPermissionEndToEnd():
    
    local = "http://127.0.0.1:5000/user_permissions/"
    homolog = "https://dev-seguranca-academy.azurewebsites.net/user_permissions/"
    auth = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}
    
    new_paper_id = str(random.randint(100,1000))
    new_user_id = str(random.randint(100,1000))
    new_azure_id = uuid4()

    data={"user_id": new_user_id,"paper_id":new_paper_id}
    data_user_already_registered={"user_id": 72,"paper_id":new_paper_id}
    data_paper_already_registered={"user_id": new_user_id,"paper_id":52}
    data_already_registered={"user_id": 72, "paper_id":52}
    data_valid={"user_id": 99, "paper_id":661}


    def test_no_token_error(self):
        response = requests.get(self.homolog)
        assert response.status_code == 403

    ###CREATE###

    def test_insert_not_found_404_error(self):
        # Act
        response = requests.post(self.homolog, headers=self.auth, json=self.data)

        # Assert
        assert response.status_code == 404

    def test_insert_duplicate_400_error(self):
        # Arrange
        post={"user_id":"72","paper_id":"55"}

        # Act
        response = requests.post(self.homolog, headers=self.auth, json=post)
        response_body = response.json()

        # Assert
        assert response_body ["msg"] == f"This user permission already exists. [user_permission_id=70]"
        assert response.status_code == 400

    def test_insert_user_permission_201_ok(self):
        # Act
        response = requests.post(self.homolog, headers=self.auth, json=self.data_valid)

        # Assert
        assert response.status_code == 201



    ###READ###

    def test_get_all_ok_200(self):
        # Arrange
        auth={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiIiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.OtpKgD5KQS6L-AL6vjtO6LQcZi4oahImZdy-lgXTC_c'}

        # Act
        response = requests.get(self.homolog, headers=self.auth)
        response_body = response.json()

        # Assert
        assert response_body
        assert response.status_code == 200


    def test_get_ok_200(self):
        # Act
        response = requests.get(f"{self.homolog}/9", headers=self.auth)
        response_body = response.json()

        # Assert
        assert response_body["user_permission_id"] == 9
        assert response.status_code == 200
        
    def test_get_not_found_404(self):
        # Arrange

        # Act
        response = requests.get(f"{self.homolog}/0", headers=self.auth)

        # Assert
        assert response.status_code == 404

    
    ###DELETE###
    def test_delete_ok_204(self):
        # Act
        response = requests.delete("https://dev-seguranca-academy.azurewebsites.net/user_permissions/70", headers=self.auth)

        # Assert
        assert response.status_code == 204

 
    def test_delete_not_found_404(self):
        # Act
        response = requests.get(f"{self.homolog}/0", headers=self.auth)

        # Assert
        assert response.status_code == 404