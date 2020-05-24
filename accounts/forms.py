from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django import forms

class UserSignUpForm(UserCreationForm):
 
    class Meta :
        model = User
        fields = ('username', 'email', 'password1', 'password2',)       
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-custom','placeholder':'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-custom','placeholder':'Enter Email'}),
        }
        labels = {
            'username' : (''),
            'email' : (''),
        }    
        help_texts = {
            'username': None,
            'email': None,
        } 
    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-custom', 'placeholder': 'Enter Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-custom', 'placeholder': 'Re-Enter Password'})   
        self.fields['password2'].help_text = None
        self.fields['email'].max_length = None
        self.fields['email'].required=True
        self.fields['password1'].label = False
        self.fields['password2'].label = False

class UserAuthenticationForm(AuthenticationForm):

    class Meta :
        model = User
        fields = ('username','password')       
    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-custom', 'placeholder': 'Enter Username'}) 
        self.fields['username'].help_text = None
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-custom', 'placeholder': 'Enter Password'}) 
        self.fields['password'].help_text = None
        self.fields['password'].label = False



