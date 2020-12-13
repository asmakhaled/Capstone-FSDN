import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies


class AgencyTestCase(unittest.TestCase):
    """This class represents the Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency"
        self.database_path = "postgres://{}@{}/{}".format(
            'postgres:1234', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.assistant_token = {
            'Authorization': 'Bearer '
            + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6I'
            + 'jBFMW02cW1xc09yUDc3SlZKeGRMZSJ9.'
            + 'eyJpc3MiOiJodHRwczovL2FzbWEta2hhbGVkLmV1LmF1dG'
            + 'gwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMzE4M'
            + 'Dk2NjQ0NzQwNTgwMjMzOSIsImF1ZCI6WyJhZ2VuY3ktYXBpI'
            + 'iwiaHR0cHM6Ly9hc21hLWtoYWxlZC5ldS5hdXRoMC5jb20vd'
            + 'XNlcmluZm8iXSwiaWF0IjoxNjA3ODUyMjgyLCJleHAiOjE2MD'
            + 'c5Mzg2ODIsImF6cCI6IjFPeTNGNE12b3hDcENQdWRnaTZZQnZ'
            + 'YSW1LUTQxbUtLIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlb'
            + 'WFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6'
            + 'bW92aWVzIl19.PAXxTm8JHY43FFX1yJSQaSh0drTwFxiB2_f6oW'
            + 'KPPgxI0ToQLljHdzLyJi0d79FSAjrZOon4FBSkcs1NfKj9R2Gq5'
            + 'UOB5b7pMEGqoYVM0FMOt2tOi8Owlk1fcY7zNnsmRw0ps11Q9hR_'
            + 'V-SpJ_KzSDHKIkW_j9ADEf9qWcAcR7piHIJTuHFLuD7obENPJPwh'
            + 'n9NWYH1HdKLyhpSkef_iMGGgJlW7rJKC_nKhJsSIk2fB1Tf4L7b'
            + 'yU7Byx4TCuIpxzpwQ28QY8Gw57ZLPxIMj22Qkz7F-o2SXLSfS'
            + 'jC1xaMYoekwYcJPPDCJp8j-e02rjeYVcRGBsAIGdYlUbm20q5A'
        }

        self.director_token = {
            'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsIn'
            + 'R5cCI6IkpXVCIsImtpZCI6IjBFMW02cW1xc09yUDc3SlZKeGR'
            + 'MZSJ9.eyJpc3MiOiJodHRwczovL2FzbWEta2hhbGVkLmV1LmF'
            + '1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmQwYTVjM2Q4NWEy'
            + 'YzAwNmVkYjU2MzMiLCJhdWQiOiJhZ2VuY3ktYXBpIiwiaWF0I'
            + 'joxNjA3ODUyMzkxLCJleHAiOjE2MDc5Mzg3OTEsImF6cCI6Ij'
            + 'FPeTNGNE12b3hDcENQdWRnaTZZQnZYSW1LUTQxbUtLIiwic2N'
            + 'vcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3Jz'
            + 'IiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY'
            + '3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ'
            + '.F_QG-qQniwGyJNLqY1izrry5H2kEEPje7XPuG6eOyWgnclse'
            + 'ymqkO0e_1QPds6G6AWo0FNmkt9Z9MNe_fxv9OPWQyTOYLObWX'
            + 'B9TmgGc632NpAPi6F8H1sgoz7iJO1w__LUqZsvG-Gw8OAs0fs'
            + 'oS-UH8JJ4tYgtbpGUOrIDoD0Yzxk792qIv52NFnnGvXyhLG2f'
            + 'vF1xBbBy8U03tnjkyWO3Q7BB29jSfp4JJ09ma4pl3AuCEvuK2'
            + 'Y1QWWjQjq9G7v99mOTVbxQYgkStUWfouPfXYtiTj0cTjxHEMz'
            + 'qT2licHs0s7QUlVlvY_FtHX8z4aJMeZwrLAOCeLsLmfO1-A1A'
        }

        self.producer_token = {
            'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR'
            + '5cCI6IkpXVCIsImtpZCI6IjBFMW02cW1xc09yUDc3SlZKeGRMZ'
            + 'SJ9.eyJpc3MiOiJodHRwczovL2FzbWEta2hhbGVkLmV1LmF1dG'
            + 'gwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMjQyMTI2'
            + 'NjI3MDExNTE5Nzc5MiIsImF1ZCI6WyJhZ2VuY3ktYXBpIiwiaH'
            + 'R0cHM6Ly9hc21hLWtoYWxlZC5ldS5hdXRoMC5jb20vdXNlcmlu'
            + 'Zm8iXSwiaWF0IjoxNjA3ODUyNTQ0LCJleHAiOjE2MDc5Mzg5ND'
            + 'QsImF6cCI6IjFPeTNGNE12b3hDcENQdWRnaTZZQnZYSW1LUTQx'
            + 'bUtLIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsIn'
            + 'Blcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6'
            + 'bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYX'
            + 'RjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9y'
            + 'cyIsInBvc3Q6bW92aWVzIl19.CExA51Z9yMeGGv5SFMN0UFBxs'
            + 'eNNPJ8lWPZwSJ0w0w3ku0RcMXhnuG_XQnZIW43i3QzvcLOlwv2'
            + 'xhBprkh6a8dVuUR8LurBp0UkEaXdIijCdotiCaEWDHRGUoz_5K'
            + 'N3-mg84fks8HOAcGu487XqnOHnrcNkiCabip2Q0ozn3VPKVXiD'
            + 'TqAPvx0u2rlcWsdICNE9Ngv9PDrDgwhW8ZHwXbBXCtZlLfXRFG'
            + 'rZrfxEfNH7rYIiB2syEmGzwb3P4mDwJz1aqB2fT1Jr7tyZaBAv'
            + 'wB2B4C-kkhquYOLyfcHNiqLX8XXAynbTdmyIF8hxZYaSdUP_xY'
            + 'qR-BIRd-a4Rhs4YUg'
        }

        self.unauthorized_token = {
            'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5'
            + 'cCI6IkpXVCIsImtpZCI6IjBFMW02cW1xc09yUDc3SlZKeGRMZSJ'
            + '9.eyJpc3MiOiJodHRwczovL2FzbWEta2hhbGVkLmV1LmF1dGgwL'
            + 'mNvbS8iLCJzdWIiOiJhdXRoMHw1ZmQzNmJhMmM3ZjEzNjAwNzlm'
            + 'ZTRkMmIiLCJhdWQiOiJhZ2VuY3ktYXBpIiwiaWF0IjoxNjA3ODU'
            + 'yNzc2LCJleHAiOjE2MDc5MzkxNzYsImF6cCI6IjFPeTNGNE12b3'
            + 'hDcENQdWRnaTZZQnZYSW1LUTQxbUtLIiwic2NvcGUiOiIiLCJwZ'
            + 'XJtaXNzaW9ucyI6W119.JJb6FglSr0oAOkHVvt0hScgt0qHJxai'
            + 'KZxck16eYNszzw2pW7ggf5bi07rhOBrqsPor8Frsj0DlrO_miua'
            + 'uWzUYsKuBTeCCem6L3o0RhSMyVpStmSa8CiAz9H4XocXb1P7XvQ'
            + 'v5heTQJSDsU1djWg6W1hlyqSgEt3BKSJ_31SbECSkAgaxbbfGE4'
            + 'h8nEztjqTgB-xxpPpvf3AKB4AQbFwtLzPm0HnKFYPf1rwDPOJTE'
            + 'b4Tiz0oc2gNXlvCK4dwBxl1LYDvH72fEUW83ZlmS5LR_GJsAnj'
            + 'X3YtrqJs-3YNTwUQVP-85PqhTHY_9-UdabHiihjvQgqHTrazY7i'
            + 'TS5yjg'
        }

        self.new_actor = {
            'name': 'liam neeson',
            'age': 68,
            'gender': 'male'
        }

        self.new_movie = {
            'title': 'Non-Stop',
            'date': 'February 28, 2014'
        }

        self.new_age = {'age': 30}

        self.new_title = {'title': 'Unknown'}

        self.wrong_actor = {
            'name': 'johnny depp',
            'age': 57,
            'gender': ''
        }

        self.wrong_movie = {
            'title': '',
            'date': ''
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Test for successful operation.
    """

    # test add actor
    def test_1_add_actor(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['totalActors'])

    # test add movie
    def test_2_add_movie(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['totalMovies'])

    # test edit actor
    def test_3_edit_actor(self):
        res = self.client().patch(
            '/actors/1',
            json=self.new_age,
            headers=self.director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertTrue(data['age'])

    # test edit movie
    def test_4_edit_movie(self):
        res = self.client().patch(
            '/movies/1',
            json=self.new_title,
            headers=self.director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertTrue(data['title'])

    # test get actors
    def test_5_get_actors(self):
        res = self.client().get(
            '/actors', headers=self.assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # test get movies
    def test_6_get_movies(self):
        res = self.client().get(
            '/movies', headers=self.assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # test delete an actor
    def test_7_delete_actors(self):
        res = self.client().delete(
            '/actors/1', headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    # test delete a movie
    def test_8_delete_movies(self):
        res = self.client().delete(
            '/movies/1', headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    """
    Test for expected errors
    """

    # test request get movies with unauthorized token
    def test_403_unauthorized_get_actors(self):
        res = self.client().get(
            '/actors', headers=self.unauthorized_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    # test request get actors with unauthorized token
    def test_403_unauthorized_get_movies(self):
        res = self.client().get(
            '/movies', headers=self.unauthorized_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    # test request post actor with assistant token
    def test_403_unauthorized_post_actor(self):
        res = self.client().post(
            '/actors', headers=self.assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    # test request delete movie with director token
    def test_403_unauthorized_delete_movie(self):
        res = self.client().delete(
            '/movies/1', headers=self.director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    # test if we want to delete an actor that does not
    # exists
    def test_422_delete_unavailable_actor(self):
        res = self.client().delete(
            '/actors/1000', headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # test if we want to delete a movie that does not exists
    def test_422_delete_unavailable_movie(self):
        res = self.client().delete(
            '/movies/1000', headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # test if the add actor failed
    def test_422_add_actor_failed(self):
        res = self.client().post(
            '/actors',
            json=self.wrong_actor,
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # test if the add movie failed
    def test_422_add_movie_failed(self):
        res = self.client().post(
            '/movies',
            json=self.wrong_movie,
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # test if the edit actor failed
    def test_404_edit_actor_failed(self):
        res = self.client().patch(
            '/actors/1000',
            json=self.new_age,
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'resource not found')

    # test if the edit movie failed
    def test_404_edit_movie_failed(self):
        res = self.client().patch(
            '/movies/1000',
            json=self.new_title,
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
