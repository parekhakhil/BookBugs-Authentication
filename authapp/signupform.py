from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import StrictButton

from .models import UserProfile

class SignupForm(forms.Form):
    first_name = forms.CharField(min_length=2, max_length=30, required=True)
    last_name = forms.CharField(min_length=2, max_length=30, required=True)
    email = forms.EmailField(min_length=8,max_length=100,required=True)
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_show_labels = True

        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = None
            del self.fields[field].widget.attrs['placeholder']

        self.helper.layout = Layout(
            'first_name', 'last_name', 'username', 
            'email', 'password1', 'password2',
            StrictButton(
                'Sign Up', type='submit',
                css_class='btn black btn-large waves-effect waves-light right'
            ),
        )

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        # creating profile for user if signup was successful
        #profile = UserProfile(user=user)
        #profile.save()
        user.save()