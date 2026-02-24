from django import forms

from .models import Program


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = [
            "name",
            "description",
            "trainer",
            "category",
            "difficulty",
            "duration_minutes",
            "max_clients",
            "is_active",
            "equipments",
        ]
        widgets = {"equipments": forms.CheckboxSelectMultiple}
