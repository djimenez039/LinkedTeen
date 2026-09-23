from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)
    profile_photo = forms.ImageField(
        required=False,
        label='Profile photo',
        help_text='Optional. JPG, PNG, or GIF up to 5 MB.',
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}),
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'profile_photo')

    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')
        if photo and photo.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Profile photo must be 5 MB or smaller.')
        return photo


class ProfilePhotoForm(forms.ModelForm):
    profile_photo = forms.ImageField(
        required=False,
        label='Profile photo',
        help_text='Optional. JPG, PNG, or GIF up to 5 MB.',
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*', 'class': 'form-control'}),
    )

    class Meta:
        model = get_user_model()
        fields = ('profile_photo',)

    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')
        if photo and photo.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Profile photo must be 5 MB or smaller.')
        return photo


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
