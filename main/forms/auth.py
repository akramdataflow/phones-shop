from django import forms
from django.contrib.auth.forms import UserCreationForm


from core.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(label='اسم المستخدم، رقم الجوال، او البريد الإلكتروني')
    password = forms.CharField(widget=forms.PasswordInput, label='كلمة المرور')

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, label='اسم المستخدم')
    email = forms.EmailField(required=False, label='البريد الإلكتروني')
    phone_number = forms.CharField(max_length=15, required=True, label='رقم الجوال')
    password1 = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تاكيد كلمة المرور', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user, 
                phone_number=self.cleaned_data['phone_number']
            )
        return user