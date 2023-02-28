import requests

class TestFunctionEndToEnd():
    invalid_function_id = 1
    new_function_name = "nomenovo3nomenovo"

    host = "https://seguranca-academy.azurewebsites.net/"
    auth = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}

    existing_system_id = (requests.get(f"{host}systems/", headers=auth)).json()[0]["system_id"]
    existing_paper_id = (requests.get(f"{host}papers/", headers=auth)).json()[0]["paper_id"]

    post_json = {"name":new_function_name, "function_type":"1", "system_id":existing_system_id}
    put_json = {"function_name":new_function_name, "function_type":"2"}


    def test_get_no_token_error(self):
        response = requests.get(f"{self.host}functions/")
        assert response.status_code == 403

    def test_insert_ok(self):
        # Act
        response = requests.post(f"{self.host}functions/", headers=self.auth, json=self.post_json)
        response_body = response.json()

        # Assert
        assert response_body["name"] == self.new_function_name
        assert response.status_code == 201

    def get_function_id_inserted(self):
        function_id = (requests.get(f"{self.host}functions/?function_name={self.new_function_name}", headers=self.auth)).json()[0]["function_id"]
        return function_id

    def test_insert_duplicated_name_error(self):
        # Act
        response = requests.post(f"{self.host}functions/", headers=self.auth, json=self.post_json)

        # Assert
        assert response.status_code == 400

    def test_insert_not_found_error(self):
        # Arrange
        post_json_invalid_system_id = {"name":"nomenovo3nomenovo", "function_type":"1", "system_id":"2"}

        # Act
        response = requests.post(f"{self.host}functions/", headers=self.auth, json=post_json_invalid_system_id)

        # Assert
        assert response.status_code == 404

    def test_update_ok(self):
        # Arrange
        function_id = self.get_function_id_inserted()

        # Act
        response = requests.put(f"{self.host}functions/{function_id}", headers=self.auth, json=self.put_json)

        # Assert
        assert response.status_code == 204

    def test_update_not_found_error(self):
        # Act
        response = requests.put(f"{self.host}functions/{self.invalid_function_id}", headers=self.auth, json=self.put_json)

        # Assert
        assert response.status_code == 404

    def test_update_duplicated_name_error(self):
        # Arrange
        get_functions_response = requests.get(f"{self.host}functions/", headers=self.auth)
        get_functions_response_body = get_functions_response.json()
        function_id = None
        for function in  get_functions_response_body:
            if function["name"] != self.new_function_name:
                function_id = function["function_id"]
                break

        # Act
        response = requests.put(f"{self.host}functions/{function_id}", headers=self.auth, json=self.put_json)

        # Assert
        assert response.status_code == 400

    def test_get_all_ok(self):
        # Act
        response = requests.get(f"{self.host}functions/", headers=self.auth)

        # Assert
        assert response.status_code == 200

    def test_get_all_max_records_ok(self):
        # Arrange
        max_records = 2

        # Act
        response = requests.get(f"{self.host}functions/?max_records={max_records}", headers=self.auth)
        response_body = response.json()

        # Assert
        assert len(response_body) <= max_records
        assert response.status_code == 200

    def test_get_all_system_id_ok(self):
        # Act
        response = requests.get(f"{self.host}functions/?system_id={self.existing_system_id}", headers=self.auth)
        response_body = response.json()

        # Assert
        for function in response_body:
            assert function["system_id"] == self.existing_system_id
        assert response.status_code == 200

    def test_get_all_function_name_ok(self):
        # Act
        response = requests.get(f"{self.host}functions/?function_name={self.new_function_name}", headers=self.auth)
        response_body = response.json()

        # Assert
        for function in response_body:
            assert function["name"] == self.new_function_name
        assert response.status_code == 200

    def test_get_all_function_type_ok(self):
        # Arrange
        function_type = 2

        # Act
        response = requests.get(f"{self.host}functions/?function_type={function_type}", headers=self.auth)
        response_body = response.json()

        # Assert
        for function in response_body:
            assert function["function_type"] == function_type
        assert response.status_code == 200

    def test_get_ok(self):
        # Arrange
        function_id = self.get_function_id_inserted()

        # Act
        response = requests.get(f"{self.host}functions/{function_id}", headers=self.auth)
        response_body = response.json()

        # Assert
        assert response_body['function_id'] == function_id
        assert response_body['system_id'] == self.existing_system_id
        assert response_body['name'] == self.new_function_name
        assert response.status_code == 200

    def test_get_not_found_error(self):
        # Act
        response = requests.get(f"{self.host}functions/{self.invalid_function_id}", headers=self.auth)

        # Assert
        assert response.status_code == 404


    def test_delete_not_found_error(self):
        # Act
        response = requests.delete(f"{self.host}functions/{self.invalid_function_id}", headers=self.auth)

        # Assert
        assert response.status_code == 404

    def test_delete_foreign_key_error(self):
        # Arrange
        function_id = self.get_function_id_inserted()

        post_feature_json = {"paper_id":self.existing_paper_id,"function_id":function_id,"create": "true"}
        requests.post(f"{self.host}features/", headers=self.auth, json=post_feature_json)

        # Act
        response = requests.delete(f"{self.host}functions/{function_id}", headers=self.auth)

        # Assert
        assert response.status_code == 400

    def test_delete_ok(self):
        # Arrange
        function_id = self.get_function_id_inserted()

        feature_id = (requests.get(f"{self.host}features/?function_id={function_id}", headers=self.auth)).json()[0]["feature_id"]
        requests.delete(f"{self.host}features/{feature_id}", headers=self.auth)

        # Act
        response = requests.delete(f"{self.host}functions/{function_id}", headers=self.auth)

        # Assert
        assert response.status_code == 204
