import math
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models
from django.db.models import DurationField, Sum
from django.utils.text import Truncator

from django.utils.html import mark_safe
from markdown import markdown

from django_countries.fields import CountryField

from multiselectfield import MultiSelectField


class Board(models.Model):
    A = "Request for Information"
    B = "Automatic Exchange of Information"
    C = "Spontaneous Exchange of Information"
    D = "Tax Examination Abroad"
    E = "Joint Audit"
    F = "Industry Wide Exchange of Information"

    query_choices = (
        (A, 'Request for Information'), (B, 'Automatic Exchange of Information'),
        (C, 'Spontaneous Exchange of Information'), (D, 'Tax Examination Abroad'), (E, 'Joint Audit'),
        (F, 'Industry Wide Exchange of Information'),
    )

    A = "OECD Model Tax Convention"
    B = "UN Model Tax Convention"
    C = "Global Forum Mutual Administrative Assistance Agreement"
    D = "Global Forum Model Tax Information Exchange Agreement"
    E = "African Tax Administration Forum Mutual Administrative Assistance Agreement"
    F = "Regional instruments and agreements"

    instrument_choices = (
        (A, 'OECD Model Tax Convention'), (B, 'UN Model Tax Convention'),
        (C, 'Global Forum Mutual Administrative Assistance Agreement'),
        (D, 'Global Forum Model Tax Information Exchange Agreement'),
        (E, 'African Tax Administration Forum Mutual Administrative Assistance Agreement'),
        (F, 'Regional instruments and agreements')
    )

    A = "Income Tax"
    B = "Value Added Tax"
    C = "Payroll Taxes"
    D = "Excise Tax"
    E = "Other Tax"

    type_choices = (
        (A, 'Income Tax'), (B, 'Value Added Tax'),
        (C, 'Payroll Taxes'),
        (D, 'Excise Tax'),
        (E, 'Other Tax'),
    )

    A = "Bulk"
    B = "Group"
    C = "Single"

    query_type_choices = (
        (A, 'Bulk'), (B, 'Group'),
        (C, 'Single'),
    )

    tax_period_choices = (
        ('2015', '2015'),
        ('2016', '2016'),
        ('2017', '2017'),
        ('2018', '2018'),
        ('2019', '2019'),
        ('2020', '2020'),
        ('2021', '2021'),
        ('Custom', 'Custom')
    )
    employees_list = []
    user = User.objects.all()
    for i in user:
        a = (str(i), str(i))
        employees_list.append(a)

    employee = models.CharField(max_length=100, choices=employees_list, default="")
    reference = models.CharField(max_length=12, default="SRC.I.", unique=True)
    subject = models.CharField(max_length=100, default="", editable=True)
    instrument = models.CharField(max_length=100, choices=instrument_choices, default=A)
    query = models.CharField(max_length=150, choices=query_choices, default=A)
    query_type = models.CharField(max_length=25, choices=query_type_choices, default=A)
    tax_period = models.CharField(max_length=15, default="", choices=tax_period_choices, editable=True)
    start_tax_period = models.DateField(default="2015-12-12", editable=True)
    end_tax_period = models.DateField(default="2020-12-31", editable=True)
    tax_type = models.CharField(max_length=100, choices=type_choices, default=A)
    if_other_tax_type = models.CharField(max_length=50, default="n/a", editable=True)
    country = CountryField(blank_label='select a country')
    document = models.FileField(upload_to='documents/', default="")

    def __str__(self):
        return self.reference

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    A = "Acknowledgement sent"
    B = "Case rejected"
    C = "Interim report sent"
    D = "Allocated to SRC Department"
    E = "Allocated to Third Party"
    F = "Partial / Interim Response sent"
    G = "Final Response sent"
    H = "Partial / Interim Response Received"
    I = "Final Response Received"
    J = "Case Finalised"

    progress_choices = (
        (A, 'Acknowledgement sent'), (B, 'Case rejected'),
        (C, 'Interim report sent'), (D, 'Allocated to SRC Department'), (E, 'Allocated to Third Party'),
        (F, 'Partial / Interim Response sent'), (G, 'Final Response sent'), (H, 'Partial / Interim Response Received'),
        (I, 'Final Response Received'), (J, 'Case Finalised')
    )

    A = "3 Days"
    B = "30 days"
    C = "60 days"
    D = "90 days"
    E = "120 days"
    F = "180 days"
    G = "360 days"

    span_choices = (
        (A, '3 days'), (B, '30 days'),
        (C, '60 days'), (D, '90 days'), (E, '120 days'),
        (F, '180 days'), (G, '360 days')
    )

    A = "Not Registered"
    B = "Active"
    C = "Inactive"
    D = "In Good Standing"
    E = "Non-Compliant"
    F = "Struck Off"
    G = "Dissolved"

    status_choices = (
        (A, 'Not Registered'), (B, 'Active'),
        (C, 'Inactive'), (D, 'In Good Standing'), (E, 'Non-Compliant'),
        (F, 'Struck Off'), (G, 'Dissolved'), (H, 'Not Applicable'),
    )

    A = "Bank"
    B = "BO"
    C = "Directors"
    D = "Accounting"
    E = "Invoices"
    F = "Agreements"
    G = "Contracts"
    H = "Others"

    information_choices = (
        (A, 'Bank'), (B, 'BO'),
        (C, 'Directors'),
        (D, 'Accounting'),
        (E, 'Invoices'),
        (F, 'Agreements'),
        (G, 'Contracts'),
        (H, 'Others')
    )

    progress = models.CharField(max_length=40, choices=progress_choices, default=A)
    requesting_party_reference_number = models.CharField(max_length=20, default="", editable=True)
    taxpayer_status = models.CharField(max_length=40, choices=status_choices, default=A)
    last_updated = models.DateTimeField(auto_now_add=True)
    case_age = DurationField(blank=True, null=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    nature_of_information_requested = MultiSelectField(choices=information_choices)
    nature_of_information_received = MultiSelectField(choices=information_choices)
    date_received = models.DateField(auto_now_add=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_process_finished = models.DateTimeField(auto_now=True)
    time_to_completion = models.CharField(max_length=35, choices=span_choices, default=A)
    point_of_contact_name = models.CharField(max_length=150, default="", editable=True)
    others = models.CharField(max_length=60, default="", editable=True)
    point_of_contact_email = models.CharField(max_length=250, default="", editable=True)
    point_of_contact_telephone1 = models.CharField(max_length=150, blank=True, default="0123430000", editable=True)
    point_of_contact_telephone2 = models.CharField(max_length=150, blank=True, default="0123430001", editable=True)
    total = models.DurationField(blank=True, null=True)

    def __str__(self):
        return self.progress

    def whenpublished(self):
        now = timezone.now()
        diff = now - self.date_created

        if diff.days == 0 and 0 <= diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and 60 <= diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and 3600 <= diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if 1 <= diff.days < 365:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

    def whenlasted(self):
        # closed = timezone.now()
        diff = self.date_process_finished - self.date_created

        if diff.days == 0 and 0 <= diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second"
            else:
                return str(seconds) + " seconds"

        if diff.days == 0 and 60 <= diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + " minute"
            else:
                return str(minutes) + " minutes"

        if diff.days == 0 and 3600 <= diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + " hour"
            else:
                return str(hours) + " hours"

        # 1 day to 30 days
        if 1 <= diff.days < 365:
            days = diff.days

            if days == 1:
                return str(days) + " day"
            else:
                return str(days) + " days"

    def whencounted(self):
        # closed = timezone.now()
        diff = self.date_process_finished - self.date_created
        days = diff.days
        if diff.days == 0:
            diff.days == 1
            return str(days)
        else:
            return str(days)


def whenalerted(self):
    # now = timezone.now()
    diff = self.span - self.case_age

    if diff.days == 0 and 0 <= diff.seconds < 60:
        seconds = diff.seconds

        if seconds == 1:
            return "0 day"

    if diff.days == 0 and 60 <= diff.seconds < 3600:
        minutes = math.floor(diff.seconds / 60)

        if minutes == 1:
            return " 0 day"

    if diff.days == 0 and 3600 <= diff.seconds < 86400:
        hours = math.floor(diff.seconds / 3600)

        if hours == 1:
            return " 0 day"

    # 1 day to 30 days
    if 1 <= diff.days < 365:
        days = diff.days

        if days == 1:
            return days + " 1 day"
        else:
            return days + " days"


class Post(models.Model):
    notes = models.TextField(max_length=4000, default="", editable=True)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        truncated_notes = Truncator(self.notes)
        return truncated_notes.chars(30)

    def get_notes_as_markdown(self):
        return mark_safe(markdown(self.notes, safe_mode='escape'))



