from uuid import uuid4
import requests
from faker import Faker
import random


class TestOwnerEndToEnd():
    
    homolog = "https://seguranca-academy.azurewebsites.net/owners/"
    auth = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}

    new_user_id = str(random.randint(1,1000))
    new_system_id = str(random.randint(1,1000))
    new_email = Faker().email()
    invalid_fake_id = 9999999999999999999


    existing_user_id = (requests.get("https://seguranca-academy.azurewebsites.net/users/", headers=auth)).json()[3]["user_id"]
    existing_system_id = (requests.get("https://seguranca-academy.azurewebsites.net/systems/1", headers=auth)).json()["system_id"]

    post_error_user_not_found={"user_id": new_user_id, "system_id": "263"}

    post_error_system_not_found={"user_id": existing_user_id, "system_id": new_system_id}
    post_error_duplicate={"user_id": 71, "system_id": 1}

    post_new={"user_id": existing_user_id, "system_id": existing_system_id}

    def test_owners_no_token_forbidden_403_error(self):
        response = requests.get(self.homolog)
        assert response.status_code == 403

    ###CREATE###

    def test_owners_post_201_ok(self):
        # Act
        response = requests.post(self.homolog, headers=self.auth, json=self.post_new)
 
        # Assert
        assert response.status_code == 201

    def test_owners_post_user_not_found_404_error(self):
        # Act
        response = requests.post(self.homolog, headers=self.auth, json=self.post_error_user_not_found)

        # Assert
        assert response.status_code == 404

    def test_owners_post_system_not_found_404_error(self):
        # Act
        response = requests.post(self.homolog, headers=self.auth, json=self.post_error_system_not_found)

        # Assert
        assert response.status_code == 404


    def test_owners_post_duplicate_400_error(self):
        # Act
        response = requests.post(self.homolog, headers=self.auth, json=self.post_error_duplicate)

        # Assert
        assert response.status_code == 400

    ###READ###

    def test_get_all_owners_200_ok(self):
        # Act
        response = requests.get(self.homolog, headers=self.auth)

        # Assert
        assert response.status_code == 200

    def test_get_owner_404_error(self):
         # Act
        response = requests.get(f"{self.homolog}/0", headers=self.auth)

        # Assert
        assert response.status_code == 404

    def test_get_owner_200_ok(self):
         # Act
        response = requests.get(f"{self.homolog}/1", headers=self.auth)
        response_body = response.json()

        # Assert
        assert response_body['system_id'] == 1
        assert response_body['user_id'] == 71
        assert response.status_code == 200
    
    def test_get_owner_system_by_email_404_not_found_error(self):
        # Act
        response = requests.get(f"{self.homolog}systems/testeendpoint@transfero.com", headers=self.auth)

        # Assert
        assert response.status_code == 404

    def test_delete_owner_404_not_found_error(self):
        # Act
        response = requests.delete(f"{self.homolog}/0", headers=self.auth)

        # Assert
        assert response.status_code == 404
        
    def test_delete_owner_204_ok(self):
        # Act
        response = requests.delete(f"{self.homolog}/15", headers=self.auth)

        # Assert
        assert response.status_code == 204