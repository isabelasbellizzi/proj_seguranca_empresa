import requests


class TestPaperEndToEnd():
    invalid_paper_id = 999999999999999999999999999999999999999999999999999
    new_paper_name = "nomenov5432"
    update_paper_name ="nomeno3no454"

    host = "https://seguranca-academy.azurewebsites.net/"
    auth = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJfaWQiOiJkZjIwNTEwOS1mNmYxLTExZWMtYjMyYy01NjZmZTE0MTAyNzQiLCJlbWFpbCI6InNlcmdpby53ZWxsaW5ndG9uQHRyYW5zZmVyby5jb20ifSwiZXhwaXJlcyI6bnVsbH0.O6sOt5LxM1_FpojLCS_yn5cxg5hbQYJRDivf7vtJaHU'}
    existing_system_id = (requests.get(f"{host}systems/", headers=auth)).json()[0]["system_id"]
    existing_paper_id = (requests.get(f"{host}papers/", headers=auth)).json()[0]["paper_id"]
    existing_function_id = (requests.get(f"{host}functions/", headers=auth)).json()[0]["function_id"]
    existing_user_id = (requests.get(f"{host}users/", headers=auth)).json()[0]["user_id"]
    post_json = {"paper_name":new_paper_name, "system_id":existing_system_id}
    put_json = {"paper_name":update_paper_name, "system_id":existing_system_id}


    def test_get_no_token_error(self):
        response = requests.get("https://seguranca-academy.azurewebsites.net/papers")
        assert response.status_code == 403


    ##################CREATE#####################
    def test_insert_ok(self):
        # Arrange

        # Act
        response = requests.post(f"{self.host}papers/", headers=self.auth, json=self.post_json)
        response_body = response.json()

        # Assert
        assert response_body['name'] == self.new_paper_name
        assert response.status_code == 201

    def get_paper_id_inserted(self):
        paper_id = (requests.get(f"{self.host}papers/?paper_name={self.new_paper_name}", headers=self.auth)).json()[0]["paper_id"]
        return paper_id

    def get_paper_id_updated(self):
        paper_id = (requests.get(f"{self.host}papers/?paper_name={self.update_paper_name}", headers=self.auth)).json()[0]["paper_id"]
        return paper_id

    def test_insert_duplicate_ok(self):
        # Arrange

        # Act
        response = requests.post(f"{self.host}papers/", headers=self.auth, json=self.post_json)
        response_body = response.json()

        # Assert
        assert response_body['msg'] == f'This paper name already exists. [paper_name={self.new_paper_name}]'
        assert response.status_code == 400

    def test_insert_system_not_found_ok(self):
        # Arrange
        post={"paper_name":"nomenovo","system_id":"99999999999999999999999999999999"}

        # Act
        response = requests.post(f"{self.host}papers/", headers=self.auth, json=post)
        response_body = response.json()

        # Assert
        assert response_body['msg'] == f'System not found. [system_id={post["system_id"]}]'
        assert response.status_code == 400

    ###############READ###############
    def test_get_all_ok(self):
        # Arrange
        # Act
        response = requests.get(f"{self.host}papers/", headers=self.auth)
        response_body = response.json()

        # Assert
        assert response_body
        assert response.status_code == 200

    def test_get_all_max_records_ok(self):
        # Arrange
        max_records = 2

        # Act
        response = requests.get(f"{self.host}papers/?max_records={max_records}", headers=self.auth)
        response_body = response.json()

        # Assert
        assert len(response_body) <= max_records
        assert response.status_code == 200

    def test_get_all_status_ok(self):
        # Act
        response = requests.get(f"{self.host}papers/?paper_status=1", headers=self.auth)

        # Assert
        assert response.status_code == 200

    def test_get_ok(self):
        # Arrange
        paper_id = self.get_paper_id_inserted()
        # Act
        response = requests.get(f"{self.host}papers/{paper_id}", headers=self.auth)
        response_body = response.json()

        # Assert
        assert response_body["paper_id"] == paper_id
        assert response_body["name"] == self.new_paper_name
        assert response_body['system_id'] == self.existing_system_id
        assert response.status_code == 200

    def test_get_not_found_error(self):
        # Act
        response = requests.get(f"{self.host}papers/{self.invalid_paper_id}", headers=self.auth)

        # Assert
        assert response.status_code == 404


    ###############UPDATE###############

    def test_update_ok(self):
        # Arrange
        paper_id = self.get_paper_id_inserted()
        # Act
        response = requests.put(f"{self.host}papers/{paper_id}", headers=self.auth,json=self.put_json)

        # Assert
        assert response.status_code == 204

    def test_update_not_found_error(self):
        # Act
        response = requests.put(f"{self.host}papers/{self.invalid_paper_id}", headers=self.auth, json=self.put_json)

        # Assert
        assert response.status_code == 404

    def test_update_duplicated_name_error(self):
        # Arrange
        get_papers_response = requests.get(f"{self.host}papers/", headers=self.auth).json()
        paper_id = None
        for paper in  get_papers_response:
            if paper["name"] != self.new_paper_name:
                paper_id = paper["paper_id"]
                break

        # Act
        response = requests.put(f"{self.host}papers/{paper_id}", headers=self.auth, json=self.put_json)

        # Assert
        assert response.status_code == 400

    ###############DELETE###############

    def test_delete_not_found_error(self):
        # Act
        response = requests.delete(f"{self.host}papers/{self.invalid_paper_id}", headers=self.auth)

        # Assert
        assert response.status_code == 404

    def test_delete_foreign_key_error(self):
        # Arrange
        paper_id =self.get_paper_id_updated()

        post_feature_json = {"paper_id":paper_id,"function_id":self.existing_function_id,"create": "true"}
        requests.post(f"{self.host}features/", headers=self.auth, json=post_feature_json)
        post_user_permission_json = {"paper_id":paper_id,"user_id":self.existing_user_id}
        requests.post(f"{self.host}user_permissions/", headers=self.auth, json=post_user_permission_json)

        # Act
        response = requests.delete(f"{self.host}papers/{paper_id}", headers=self.auth)

        # Assert
        assert response.status_code == 404

    def test_delete_ok(self):

        # Arrange
        paper_id =self.get_paper_id_updated()

        feature_id = (requests.get(f"{self.host}features/?max_records=0&paper_id={paper_id}", headers=self.auth)).json()[0]["feature_id"]
        requests.delete(f"{self.host}features/{feature_id}", headers=self.auth)

        user_permission_id = (requests.get(f"{self.host}user_permissions/?max_records=0&paper_id={paper_id}", headers=self.auth)).json()[0]["user_permission_id"]
        requests.delete(f"{self.host}user_permissions/{user_permission_id}", headers=self.auth)

        # Act
        response = requests.delete(f"{self.host}papers/{paper_id}", headers=self.auth)

        # Assert
        assert response.status_code == 204
