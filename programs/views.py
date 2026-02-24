from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from core.permissions import TrainerOrManagerRequiredMixin
from reviews.models import Review

from .forms import ProgramForm
from .models import Program


def program_list(request):
    qs = Program.objects.select_related("trainer", "category").prefetch_related("equipments")
    search = request.GET.get("search", "").strip()
    category = request.GET.get("category")
    difficulty = request.GET.get("difficulty")
    ordering = request.GET.get("ordering", "name")
    if search:
        qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))
    if category:
        qs = qs.filter(category_id=category)
    if difficulty:
        qs = qs.filter(difficulty=difficulty)
    if ordering in {"name", "-name", "duration_minutes", "-duration_minutes"}:
        qs = qs.order_by(ordering)
    page_obj = Paginator(qs, 8).get_page(request.GET.get("page"))
    return render(
        request,
        "programs/program_list.html",
        {"page_obj": page_obj, "programs": page_obj.object_list, "filters": request.GET},
    )


class ProgramDetailView(DetailView):
    model = Program
    template_name = "programs/program_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Program.objects.select_related("trainer", "category").prefetch_related(
            "equipments", "exercises"
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["average_rating"] = Review.objects.filter(program=self.object).aggregate(v=Avg("rating"))["v"] or 0
        return ctx


class ProgramCreateView(LoginRequiredMixin, TrainerOrManagerRequiredMixin, CreateView):
    model = Program
    form_class = ProgramForm
    template_name = "programs/program_form.html"
    success_url = reverse_lazy("programs:list")

    def form_valid(self, form):
        messages.success(self.request, "Программа создана.")
        return super().form_valid(form)


class ProgramUpdateView(LoginRequiredMixin, TrainerOrManagerRequiredMixin, UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = "programs/program_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        messages.success(self.request, "Программа обновлена.")
        return reverse_lazy("programs:detail", kwargs={"slug": self.object.slug})
