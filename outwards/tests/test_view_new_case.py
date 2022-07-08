from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..forms import NewCaseForm
from ..models import Outward, Update, Case
from ..views import new_case


class NewTopicTests(TestCase):
    def setUp(self):
        Outward.objects.create(reference='SCP234576', subject='investigations', query='Tax Examination.')
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.client.login(username='john', password='123')

    def test_new_case_view_success_status_code(self):
        url = reverse('new_case', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_case_view_not_found_status_code(self):
        url = reverse('new_case', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_case_url_resolves_new_case_view(self):
        view = resolve('/outwards/1/new/')
        self.assertEquals(view.func, new_case)

    def test_new_case_view_contains_link_back_to_outward_cases_view(self):
        new_case_url = reverse('new_case', kwargs={'pk': 1})
        outward_cases_url = reverse('outward_cases', kwargs={'pk': 1})
        response = self.client.get(new_case_url)
        self.assertContains(response, 'href="{0}"'.format(outward_cases_url))

    def test_csrf(self):
        url = reverse('new_case', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        url = reverse('new_case', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewCaseForm)

    def test_new_case_valid_update_data(self):
        url = reverse('new_case', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'notes': 'Lorem ipsum dolor sit amet'
        }
        self.client.update(url, data)
        self.assertTrue(Case.objects.exists())
        self.assertTrue(Case.objects.exists())

    def test_new_case_invalid_update_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_case', kwargs={'pk': 1})
        response = self.client.update(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_case_invalid_update_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_case', kwargs={'pk': 1})
        data = {
            'subject': '',
            'notes': ''
        }
        response = self.client.update(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Case.objects.exists())
        self.assertFalse(Case.objects.exists())


class LoginRequiredNewCaseTests(TestCase):
    def setUp(self):
        Outward.objects.create(reference='SCP234576', subject='investigations', query='Tax Examination.')
        self.url = reverse('new_case', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))