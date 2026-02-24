from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count
from django.shortcuts import render
from django.views import View

from clients.models import Client
from memberships.models import Subscription
from programs.models import ProgramCategory
from reviews.models import Review


class ReportsDashboardView(LoginRequiredMixin, View):
    template_name = "reports/dashboard.html"

    def get(self, request):
        category_stats = ProgramCategory.objects.annotate(total_programs=Count("programs")).order_by("-total_programs")
        top_clients = Client.objects.annotate(total_reviews=Count("reviews")).order_by("-total_reviews", "name")[:10]
        metrics = {
            "clients_total": Client.objects.count(),
            "subscriptions_active": Subscription.objects.filter(status="active").count(),
            "avg_review": Review.objects.aggregate(v=Avg("rating"))["v"] or 0,
        }
        return render(request, self.template_name, {"category_stats": category_stats, "top_clients": top_clients, "metrics": metrics})
