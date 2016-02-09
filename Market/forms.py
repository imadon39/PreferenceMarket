from django import forms
from django.contrib.auth.models import User
from types import *
from django.forms.widgets import RadioSelect

class StringListField(forms.CharField):
    def prepare_value(self, value):
        return ', '.join(value)

    def to_python(self, value):
        if not value:
            return []
        return [item.strip() for item in value.split(',')]

class CreateNewUserForm(forms.Form):
    username = forms.CharField(label='username', widget=forms.TextInput)
    age = forms.IntegerField(label='age', widget=forms.NumberInput)
    gender = forms.ChoiceField(label='gender', widget=forms.RadioSelect,choices= (('m','male'),('f','female')))
    email = forms.CharField(label='email',required=False, widget=forms.EmailInput)
    password1 = forms.CharField(label='password1', widget=forms.PasswordInput)
    password2 = forms.CharField(label='password2', widget=forms.PasswordInput)

    #Check the form
    def clean(self):
        cleaned_data = super(CreateNewUserForm, self).clean()
        username = cleaned_data.get("username")
        age = cleaned_data.get("age")
        gender = cleaned_data.get("gender")
        email = cleaned_data.get("email")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        #Check username availability
        if User.objects.filter(username=username).exists():
            self.add_error('username', "The entered username already exists, please try again.")

        elif password1 and password2 and (password1 != password2):
            self.add_error('password1', "Password mismatch! , please try again.")

        elif type(password1) is not NoneType:
            if len(password1) < 5:
                self.add_error('password1', "The password length must be greater than 5")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label='username', widget=forms.TextInput)
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    #Check the form
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        #Check username 
        if not User.objects.filter(username=username).exists():
            self.add_error('username', "The entered username not exists, please try again.")

        return cleaned_data

class CreateRetailStoreNameForm(forms.Form):
    name = forms.CharField(label='name', widget=forms.TextInput)
    #Check the form
    def clean(self):
        cleaned_data = super(CreateRetailStoreNameForm, self).clean()
        name = cleaned_data.get("name")

        return cleaned_data

class TransactionForm(forms.Form):
    amount = forms.IntegerField(label='amount', widget=forms.NumberInput)

    def clean(self):
        cleaned_data = super(TransactionForm, self).clean()
        amount = cleaned_data.get("amount")

        return cleaned_data

class NewLevelForm(forms.Form):
    level = forms.CharField(widget = forms.TextInput)

    def clean(self):
        cleaned_data = super(NewLevelForm, self).clean()

        return clean_data

class CreateNewIdeaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        levels = kwargs.pop('levels')
        super(CreateNewIdeaForm, self).__init__(*args, **kwargs)
        counter = 1
        for lev in levels:
            self.fields['question-' + str(counter)] = forms.CharField(label="levels")
            counter += 1

        def clean(self):
            cleaned_data = super(NewIdeaForm, self).clean()
            name = cleaned_data.get("levels")

            return cleaned_data

        