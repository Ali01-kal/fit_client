from django import forms

from .models import MembershipPlan, Subscription


class MembershipPlanForm(forms.ModelForm):
    class Meta:
        model = MembershipPlan
        fields = ["name", "price", "duration_days", "visit_limit", "is_active"]


class SubscriptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["client"].empty_label = "Выберите клиента"
        self.fields["plan"].empty_label = "Выберите тариф"
        self.fields["status"].initial = "active"
        self.fields["visits_used"].initial = 0
        self.fields["visits_used"].widget.attrs.update({"min": 0, "placeholder": "0"})
        self.fields["starts_on"].widget.attrs.update({"placeholder": "Дата начала"})
        self.fields["ends_on"].widget.attrs.update({"placeholder": "Авторасчёт (можно оставить пустым)"})

    class Meta:
        model = Subscription
        fields = ["client", "plan", "starts_on", "ends_on", "status", "visits_used"]
        widgets = {
            "starts_on": forms.DateInput(attrs={"type": "date"}),
            "ends_on": forms.DateInput(attrs={"type": "date"}),
        }
