from django.forms import ModelForm, Textarea, PasswordInput
from .models import Person
from django.contrib.auth.models import User


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        fields = ('bio', 'other_contacts', 'date_of_birth', 'jabber', 'skype', 'profile_image')
        widgets = {
            'bio': Textarea(attrs={'cols': 50, 'rows': 5, 'maxlength': 250}),
            'other_contacts': Textarea(attrs={'cols': 50, 'rows': 5, 'maxlength': 250}),
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