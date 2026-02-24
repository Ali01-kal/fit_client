from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import random

from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "role", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Suggest a ready-to-use username so the user can register faster.
        if not self.is_bound:
            self.fields["username"].initial = f"fituser_{random.randint(1000, 9999)}"
        self.fields["username"].widget.attrs.update({"placeholder": "Имя пользователя"})
        self.fields["first_name"].widget.attrs.update({"placeholder": "Имя"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Фамилия"})
        self.fields["email"].widget.attrs.update({"placeholder": "Email"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Пароль"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Повторите пароль"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()
            profile = user.userprofile
            profile.role = self.cleaned_data["role"]
            profile.save()
        return user


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField()

    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name", "email", "phone", "avatar", "birth_date", "bio")
        widgets = {"birth_date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(self.instance, "user_id", None):
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            profile.save()
        return profile
