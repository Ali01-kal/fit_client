from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from core.permissions import ManagerRequiredMixin, TrainerOrManagerRequiredMixin

from .forms import ClientForm
from .models import Client, ClientFavorite


def client_list(request):
    qs = Client.objects.select_related("primary_trainer").all()
    search = request.GET.get("search", "").strip()
    trainer = request.GET.get("trainer")
    status = request.GET.get("status")
    ordering = request.GET.get("ordering", "name")
    if search:
        qs = qs.filter(Q(name__icontains=search) | Q(email__icontains=search))
    if trainer:
        qs = qs.filter(primary_trainer_id=trainer)
    if status in {"active", "inactive"}:
        qs = qs.filter(is_active=(status == "active"))
    if ordering in {"name", "-name", "created_at", "-created_at"}:
        qs = qs.order_by(ordering)
    page_obj = Paginator(qs, 8).get_page(request.GET.get("page"))
    return render(
        request,
        "clients/client_list.html",
        {
            "page_obj": page_obj,
            "clients": page_obj.object_list,
            "filters": request.GET,
            "favorite_client_ids": set(
                ClientFavorite.objects.filter(user=request.user).values_list("client_id", flat=True)
            )
            if request.user.is_authenticated
            else set(),
        },
    )


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "clients/client_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Client.objects.select_related("primary_trainer").prefetch_related(
            "subscriptions__plan", "metrics"
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["is_favorite"] = ClientFavorite.objects.filter(
            user=self.request.user, client=self.object
        ).exists()
        return ctx


class ClientCreateView(LoginRequiredMixin, TrainerOrManagerRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:list")

    def form_valid(self, form):
        messages.success(self.request, "Клиент создан.")
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, TrainerOrManagerRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        messages.success(self.request, "Клиент обновлён.")
        return reverse_lazy("clients:detail", kwargs={"slug": self.object.slug})


class ClientDeleteView(LoginRequiredMixin, ManagerRequiredMixin, DeleteView):
    model = Client
    template_name = "clients/client_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("clients:list")

    def form_valid(self, form):
        messages.success(self.request, "Клиент удалён.")
        return super().form_valid(form)


def toggle_client_favorite(request, slug):
    if not request.user.is_authenticated:
        return redirect("login")
    client = get_object_or_404(Client, slug=slug)
    favorite, created = ClientFavorite.objects.get_or_create(user=request.user, client=client)
    if created:
        messages.success(request, f"'{client.name}' добавлен в избранное.")
    else:
        favorite.delete()
        messages.info(request, f"'{client.name}' удалён из избранного.")
    return redirect("clients:detail", slug=slug)
