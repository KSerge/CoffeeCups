from django.forms import ModelForm, Textarea, PasswordInput, Select
from .models import Person, IncomingRequest
from django.contrib.auth.models import User
from .widjets import CalendarWidget
from django.forms.models import modelformset_factory

CHOICES = ('1', '2',)


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        fields = ('bio', 'other_contacts', 'date_of_birth', 'jabber', 'skype', 'profile_image')
        widgets = {
            'bio': Textarea(attrs={'cols': 50, 'rows': 5, 'maxlength': 250}),
            'other_contacts': Textarea(attrs={'cols': 50, 'rows': 5, 'maxlength': 250}),
            'date_of_birth': CalendarWidget(attrs={'class': 'datepicker'}),
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        widgets = {
            'password': PasswordInput()
        }


class UserEditForm(UserForm):
    class Meta(UserForm.Meta):
        exclude = ('username', 'password',)


class IncomingRequestForm(ModelForm):
    class Meta:
        model = IncomingRequest
        fields = ('path', 'priority')
        widgets = {
            'priority': Select(choices=CHOICES)
        }

IncomingRequestFormSet = modelformset_factory(IncomingRequest, form=IncomingRequestForm)
# IncomingRequestFormSet = modelformset_factory(IncomingRequest)
