from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Outward
from ..views import case_updates, outward_cases


class OutwardCasesTests(TestCase):
    def setUp(self):
        Outward.objects.create(reference='SCP234576', subject='investigations', query='Tax Examination.')

    def test_outward_cases_view_success_status_code(self):
        url = reverse('case_updates', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_outward_cases_view_not_found_status_code(self):
        url = reverse('outward_cases', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_outward_cases_url_resolves_outward_cases_view(self):
        view = resolve('/outwards/1/')
        self.assertEquals(view.func, outward_cases)

    def test_board_topics_view_contains_navigation_links(self):
        outward_cases_url = reverse('outward_cases', kwargs={'pk': 1})
        homepage_url = reverse('landing')
        new_topic_url = reverse('new_case', kwargs={'pk': 1})
        response = self.client.get(outward_cases_url)
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))