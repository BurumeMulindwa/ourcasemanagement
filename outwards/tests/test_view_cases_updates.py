from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Outward, Update, Case
from ..views import case_updates


class CaseUpdatesTests(TestCase):
    def setUp(self):
        outward = Outward.objects.create(reference='SCP.I.234852', subject='investigations', query='Tax Examination.')
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        case = Case.objects.create(progress='Acknowledgement sent', requesting_party_reference_number='SA1234', last_updated='09.01.2022', case_age='5 days ago',
        board='SCF.I.1265', initiator='Marcel Tireaux', date_received='01.01.2022', date_created='01.01.2022', instrument='UN Model Tax Convention', point_of_contact_name='Dario' ,
        point_of_contact_surname='Mulolo', point_of_contact_title='Head of Investigations', point_of_contact_email='dariomulolo@gmail.com',
        point_of_contact_telephone1='0123456789', point_of_contact_telephone2='0123456987')
        Update.objects.create(notes='lorem ipsum' , case='SCR.I.4512' , created_at='01.01.2022 14:00' , updated_at='02.01.2022 14:00' , author='Dario Mulolo', updated_by=user)
        url = reverse('case_updates', kwargs={'pk': outward.pk, 'case_pk': case.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/outwards/1/cases/1/')
        self.assertEquals(view.func, case_updates)