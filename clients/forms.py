from django import forms

from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "name",
            "email",
            "phone",
            "gender",
            "birth_date",
            "primary_trainer",
            "avatar",
            "notes",
            "is_active",
        ]
        widgets = {"birth_date": forms.DateInput(attrs={"type": "date"})}
