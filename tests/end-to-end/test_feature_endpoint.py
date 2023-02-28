import requests

class TestFeatureEndToEnd():
    invalid_feature_id = 1

    host = "https://seguranca-academy.azurewebsites.net/"
    auth = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}

    existing_paper_id = (requests.get(f"{host}papers/", headers=auth)).json()[0]["paper_id"]
    existing_function_id = (requests.get(f"{host}functions/", headers=auth)).json()[0]["function_id"]

    post_json = {"paper_id":existing_paper_id, "function_id":existing_function_id, "create":"true"}
    put_json = {"delete":"false"}

    def test_get_no_token_error(self):
        response = requests.get(f"{self.host}features")
        assert response.status_code == 403

    def test_insert_ok(self):
        # Act
        response = requests.post(f"{self.host}features/", headers=self.auth, json=self.post_json)
        response_body = response.json()

        # Assert
        assert response_body["create"] == True
        assert response_body["read"] == False
        assert response_body["update"] == False
        assert response_body["delete"] == False
        assert response_body["paper_id"] == self.existing_paper_id
        assert response_body["function_id"] == self.existing_function_id
        assert response.status_code == 201

    def test_insert_duplicated_object_error(self):
        # Act
        response = requests.post(f"{self.host}features/", headers=self.auth, json=self.post_json)
        # Assert
        assert response.status_code == 400

    def test_insert_not_found_error(self):
        # Arrange
        post = {"paper_id":1, "function_id":1, "create":"true"}

        # Act
        response = requests.post(f"{self.host}features/", headers=self.auth, json=post)

        # Assert
        assert response.status_code == 404

    def test_get_all_ok(self):
        # Act
        response = requests.get(f"{self.host}features/", headers=self.auth)

        # Assert
        assert response.status_code == 200

    def test_get_all_max_records_ok(self):
        # Arrange
        max_records = 2

        # Act
        response = requests.get(f"{self.host}features/?max_records={max_records}", headers=self.auth)
        response_body = response.json()

        # Assert
        assert len(response_body) <= max_records
        assert response.status_code == 200

    def test_get_all_query_paper_id_ok(self):
        # Act
        response = requests.get(f"{self.host}features/?paper_id={self.existing_paper_id}", headers=self.auth)
        response_body = response.json()

        # Assert
        for feature in response_body:
            assert feature["paper_id"] == self.existing_paper_id
        assert response.status_code == 200

    def test_get_all_query_function_id_ok(self):
        # Act
        response = requests.get(f"{self.host}features/?function_id={self.existing_function_id}", headers=self.auth)
        response_body = response.json()

        # Assert
        for feature in response_body:
            assert feature["function_id"] == self.existing_function_id
        assert response.status_code == 200

    def test_get_ok(self):
        # Arrange
        feature_id = (requests.get(f"{self.host}features/?paper_id={self.existing_paper_id}&function_id={self.existing_function_id}", headers=self.auth)).json()[0]["feature_id"]

        # Act
        response = requests.get(f"{self.host}features/{feature_id}", headers=self.auth)
        response_body = response.json()

        # Assert
        assert response_body['feature_id'] == feature_id
        assert response.status_code == 200

    def test_get_not_found_error(self):
        # Act
        response = requests.get(f"{self.host}features/{self.invalid_feature_id}", headers=self.auth)

        # Assert
        assert response.status_code == 404

    def test_update_ok(self):
        feature_id = requests.get(f"{self.host}features/?paper_id={self.existing_paper_id}&function_id={self.existing_function_id}", headers=self.auth).json()[0]["feature_id"]

        # Act
        response = requests.put(f"https://seguranca-academy.azurewebsites.net/features/{feature_id}", headers=self.auth, json=self.put_json)

        # Assert
        assert response.status_code == 204

    def test_update_not_found_error(self):
        # Act
        response = requests.put(f"https://seguranca-academy.azurewebsites.net/features/{self.invalid_feature_id}", headers=self.auth, json=self.put_json)

        # Assert
        assert response.status_code == 404

    def test_delete_not_found_error(self):
        # Act
        response = requests.delete(f"https://seguranca-academy.azurewebsites.net/features/{self.invalid_feature_id}", headers=self.auth)

        # Assert
        assert response.status_code == 404

    def test_delete_ok(self):
        # Arrange
        feature_id = requests.get(f"https://seguranca-academy.azurewebsites.net/features/?paper_id={self.existing_paper_id}&function_id={self.existing_function_id}", headers=self.auth).json()[0]["feature_id"]

        # Act
        response = requests.delete(f"https://seguranca-academy.azurewebsites.net/features/{feature_id}", headers=self.auth)

        # Assert
        assert response.status_code == 204
