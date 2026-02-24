from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from core.permissions import ManagerRequiredMixin

from .forms import MembershipPlanForm, SubscriptionForm
from .models import MembershipPlan, Subscription


def membership_plan_list(request):
    qs = MembershipPlan.objects.annotate(
        total_subscriptions=Count("subscriptions"),
        active_subscriptions=Count(
            "subscriptions", filter=Q(subscriptions__status="active")
        ),
    ).order_by("price")
    search = request.GET.get("search", "").strip()
    if request.GET.get("active") in {"0", "1"}:
        qs = qs.filter(is_active=request.GET.get("active") == "1")
    if search:
        qs = qs.filter(name__icontains=search)
    page_obj = Paginator(qs, 10).get_page(request.GET.get("page"))
    stats = {
        "plans_total": MembershipPlan.objects.count(),
        "plans_active": MembershipPlan.objects.filter(is_active=True).count(),
        "subs_active": Subscription.objects.filter(status="active").count(),
        "subs_paused": Subscription.objects.filter(status="paused").count(),
    }
    return render(
        request,
        "memberships/plan_list.html",
        {
            "page_obj": page_obj,
            "plans": page_obj.object_list,
            "filters": request.GET,
            "stats": stats,
        },
    )


class MembershipPlanCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
    model = MembershipPlan
    form_class = MembershipPlanForm
    template_name = "memberships/plan_form.html"
    success_url = reverse_lazy("memberships:plans")

    def form_valid(self, form):
        messages.success(self.request, "Тариф создан.")
        return super().form_valid(form)


class SubscriptionListView(LoginRequiredMixin, DetailView):
    model = MembershipPlan
    template_name = "memberships/subscription_list.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["subscriptions"] = self.object.subscriptions.select_related("client").all()
        ctx["status_counts"] = (
            self.object.subscriptions.values("status").annotate(total=Count("id")).order_by("status")
        )
        return ctx


class SubscriptionCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = "memberships/subscription_form.html"
    success_url = reverse_lazy("memberships:plans")

    def get_initial(self):
        initial = super().get_initial()
        plan_id = self.request.GET.get("plan")
        if plan_id and plan_id.isdigit():
            initial["plan"] = int(plan_id)
        initial.setdefault("status", "active")
        initial.setdefault("visits_used", 0)
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Абонемент клиента создан.")
        return super().form_valid(form)
