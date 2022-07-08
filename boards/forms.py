from django import forms
from django.utils.safestring import mark_safe

from .models import Post, Topic, Board


class FiveNumFields(forms.MultiWidget):
    def __init__(self, attrs=None):
        self.widgets = [
            forms.TextInput(),
            forms.TextInput(),
            forms.TextInput(),
            forms.TextInput(),
            forms.TextInput(),
        ]
        super().__init__(self.widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(' ')
        return [None, None]


class NameMultiField(forms.MultiValueField):
    widget = FiveNumFields()

    def __init__(self):
        fields = (
            forms.CharField(
                max_length=25,
            ),
            forms.CharField(
                max_length=25,
            ),
            forms.CharField(
                max_length=25,
            ),
            forms.CharField(
                max_length=25,
            ),
            forms.CharField(
                max_length=25,
            )
        )
        super(NameMultiField, self).__init__(
            fields=fields,
            require_all_fields=False,
        )

    def compress(self, data_list):
        return ' '.join(data_list)


class NewTopicForm(forms.ModelForm):
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Incongruent, Privileged, Secrets, Policy'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
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
    nature_of_information_requested = forms.MultipleChoiceField(choices=information_choices,
                                                                widget=forms.CheckboxSelectMultiple())
    nature_of_information_received = forms.MultipleChoiceField(choices=information_choices,
                                                               widget=forms.CheckboxSelectMultiple())
    point_of_contact_name = NameMultiField()
    point_of_contact_email = NameMultiField()
    point_of_contact_telephone1 = NameMultiField()
    point_of_contact_telephone2 = NameMultiField()

    class Meta:
        model = Topic
        fields = ['progress', 'notes', 'requesting_party_reference_number',
                  'taxpayer_status', 'time_to_completion', 'nature_of_information_requested',
                  'nature_of_information_received', 'others',
                  'point_of_contact_name',
                  'point_of_contact_email', 'point_of_contact_telephone1', 'point_of_contact_telephone2'
                  ]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['notes', ]


class BoardModelForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('tax_period',)
        widgets = {
            'tax_period': forms.Select(choices=Board.tax_period_choices)
        }
