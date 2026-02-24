from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["client", "program", "trainer", "rating", "comment", "is_published"]
        widgets = {"comment": forms.Textarea(attrs={"rows": 4})}
