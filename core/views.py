from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from clients.models import Client
from memberships.models import Subscription
from programs.models import Program, ProgramCategory
from reviews.models import Review


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["featured_programs"] = Program.objects.select_related("trainer", "category").filter(is_active=True)[:6]
        ctx["categories"] = ProgramCategory.objects.annotate(total=Count("programs")).order_by("-total")[:6]
        ctx["reviews"] = Review.objects.select_related("client", "program", "trainer").filter(is_published=True)[:5]
        return ctx


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["stats"] = {
            "clients": Client.objects.count(),
            "programs": Program.objects.count(),
            "active_subscriptions": Subscription.objects.filter(status="active").count(),
            "avg_rating": Review.objects.aggregate(v=Avg("rating"))["v"] or 0,
        }
        ctx["recent_clients"] = Client.objects.select_related("primary_trainer")[:5]
        ctx["top_categories"] = ProgramCategory.objects.annotate(total=Count("programs")).order_by("-total")[:5]
        return ctx


class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactView(TemplateView):
    template_name = "core/contact.html"

    def post(self, request, *args, **kwargs):
        messages.success(request, "Сообщение отправлено (демо-режим).")
        return self.get(request, *args, **kwargs)


def healthcheck(request):
    return HttpResponse("ok")


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)
