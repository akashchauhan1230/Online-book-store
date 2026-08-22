# pyrefly: ignore [missing-import]
from django.test import TestCase
# pyrefly: ignore [missing-import]
from django.urls import reverse

from mainapp.models import LoginInfo, UserInfo


class IndexViewTests(TestCase):
    def test_index_renders_for_anonymous_visitors(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_redirects_when_session_user_does_not_exist(self):
        session = self.client.session
        session['userid'] = 'ghost@example.com'
        session.save()

        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_category_page_renders_successfully(self):
        response = self.client.get(reverse('category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')

    def test_userdash_renders_successfully(self):
        login = LoginInfo.objects.create(usertype='user', username='tester@example.com', password='pw')
        UserInfo.objects.create(name='Tester', email='tester@example.com', contactno='1112223334', password='pw', cpassword='pw', login=login)
        session = self.client.session
        session['userid'] = 'tester@example.com'
        session.save()

        response = self.client.get(reverse('userdash'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userdash.html')

    def test_admindash_renders_successfully(self):
        login = LoginInfo.objects.create(usertype='admin', username='admin@example.com', password='pw')
        session = self.client.session
        session['adminid'] = 'admin@example.com'
        session.save()

        response = self.client.get(reverse('admindash'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admindash.html')


class AuthViewTests(TestCase):
    def setUp(self):
        self.login = LoginInfo.objects.create(
            usertype='user',
            username='alice@example.com',
            password='secret123',
        )
        self.user = UserInfo.objects.create(
            name='Alice',
            email='alice@example.com',
            contactno='9876543210',
            password='secret123',
            cpassword='secret123',
            login=self.login,
        )

    def test_login_with_valid_credentials_redirects_to_index(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'alice@example.com', 'password': 'secret123'},
        )

        self.assertRedirects(response, reverse('index'))
        self.assertEqual(self.client.session.get('userid'), 'alice@example.com')

    def test_login_with_invalid_credentials_redirects_back_to_login(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'alice@example.com', 'password': 'wrongpassword'},
        )

        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('userid', self.client.session)

    def test_register_creates_user_and_login_record(self):
        response = self.client.post(
            reverse('register'),
            {
                'name': 'Bob',
                'email': 'bob@example.com',
                'contactno': '1234567891',
                'password': 'strongpass',
                'cpassword': 'strongpass',
            },
        )

        self.assertRedirects(response, reverse('login'))
        self.assertTrue(LoginInfo.objects.filter(username='bob@example.com', usertype='user').exists())
        self.assertTrue(UserInfo.objects.filter(email='bob@example.com').exists())
