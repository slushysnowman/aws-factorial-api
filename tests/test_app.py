import unittest

from container.app.app import app


class TestApp(unittest.TestCase):

    test_client = app.test_client()

    def test_root_status_code(self):
        response = self.test_client.get("/")

        self.assertEqual(response.status_code, 404)

    def test_correct_path_status_code(self):
        response = self.test_client.get("/api/v1/factorial")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(b"Please supply number parameter", response.data)

    def test_correct_parameters(self):
        response = self.test_client.get("/api/v1/factorial?number=5")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(b'{"factorial":120}\n', response.data)

    def test_negative_parameter(self):
        response = self.test_client.get("/api/v1/factorial?number=-1")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(b"Invalid value", response.data)

    def test_non_integer_parameter(self):
        response = self.test_client.get("/api/v1/factorial?number=0.2")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(b"Invalid value", response.data)

    def test_wrong_parameter_name(self):
        response = self.test_client.get("/api/v1/factorial?capsicum=5")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(b"Please supply number parameter", response.data)
