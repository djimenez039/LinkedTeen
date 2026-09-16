from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate, get_user_model


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class EmailOrUsernameAuthenticationForm(forms.Form):
    username = forms.CharField(label='Username or email')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None

    def clean(self):
        cleaned = super().clean()
        identifier = cleaned.get('username')
        password = cleaned.get('password')
        if identifier and password:
            user_model = get_user_model()
            user = user_model.objects.filter(email__iexact=identifier).first()
            username = user.username if user else identifier
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Invalid username/email or password.')
        return cleaned

    def get_user(self):
        return self.user_cache
