from django.test import TestCase
from rest_framework.test import APIClient
from apps.authorization.models import User

# Create your tests here.
class TestRegistration(TestCase):
    def tearDown(self) -> None:
        pass

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create(self):
        count = User.objects.all().count()
        self.assertEqual(count, 0)
        response = self.client.post('/auth/registration/', {'email':'test@test.ru', 'password':'my_password'})
        self.assertEqual(response.status_code, 201)
        count = User.objects.all().count()
        self.assertEqual(count, 1)

    def test_bad_params(self):
        count = User.objects.all().count()
        self.assertEqual(count, 0)

        response = self.client.post('/auth/registration/', {'email': 'test', 'password': 'my_password'})
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/auth/registration/', {'email': 'test@test.ru', 'password': 'my_password'})
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/auth/registration/', {'email': 'test@test.ru', 'password': 'my_password'})
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/auth/registration/', {'email': 'testw@test.ru'})
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/auth/registration/', {'email': 'test2@test.ru', 'password': ''})
        self.assertEqual(response.status_code, 400)

        count = User.objects.all().count()
        self.assertEqual(count, 1)

class TestProfile(TestCase):
    def tearDown(self) -> None:
        pass

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.post('/auth/registration/', {'email': 'test1@test.ru', 'password': 'test1'})
        self.client.post('/auth/registration/', {'email': 'test2@test.ru', 'password': 'test2'})

    def test_profile(self):
        response = self.client.get('/auth/profile/1/')
        self.assertEqual(response.data['email'], 'test1@test.ru')

        response = self.client.post('/auth/profile/1/')
        self.assertEqual(response.status_code, 405)

        response = self.client.put('/auth/profile/1/')
        self.assertEqual(response.status_code, 405)

        response = self.client.patch('/auth/profile/1/', {'email': 'mod@test.ru'})
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/auth/profile/1/')
        self.assertEqual(response.data['email'], 'mod@test.ru')

        response = self.client.get('/auth/profile/100/')
        self.assertEqual(response.status_code, 404)

        response = self.client.delete('/auth/profile/1/')
        self.assertEqual(response.status_code, 204)
        response = self.client.get('/auth/profile/1/')
        self.assertEqual(response.status_code, 404)