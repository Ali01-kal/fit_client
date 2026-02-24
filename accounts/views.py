from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from clients.models import ClientFavorite
from reviews.models import Review
from .forms import RegisterForm, UserProfileForm
from .models import UserProfile


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("core:dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        group, _ = Group.objects.get_or_create(name=form.cleaned_data["role"])
        self.object.groups.add(group)
        login(self.request, self.object)
        messages.success(self.request, "Регистрация прошла успешно.")
        return response


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = "accounts/profile_detail.html"

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx["favorite_clients"] = (
            ClientFavorite.objects.select_related("client")
            .filter(user=user)
            .order_by("-created_at")[:5]
        )
        ctx["my_reviews"] = (
            Review.objects.select_related("program", "trainer")
            .filter(client__user=user)
            .order_by("-created_at")[:5]
        )
        client_record = getattr(user, "client_record", None)
        ctx["my_subscriptions"] = (
            client_record.subscriptions.select_related("plan").all()[:5] if client_record else []
        )
        return ctx


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "accounts/profile_form.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def form_valid(self, form):
        messages.success(self.request, "Профиль обновлён.")
        return super().form_valid(form)


def profile_redirect(request):
    return redirect("accounts:profile" if request.user.is_authenticated else "login")


class RateLimitedLoginView(auth_views.LoginView):
    template_name = "registration/login.html"
    max_attempts = 5
    window_minutes = 10
    lock_minutes = 10

    def _state(self):
        return self.request.session.setdefault(
            "login_rate_limit",
            {"attempts": [], "locked_until": None},
        )

    def dispatch(self, request, *args, **kwargs):
        state = self._state()
        now = timezone.now()
        locked_until_raw = state.get("locked_until")
        if locked_until_raw:
            try:
                locked_until = timezone.datetime.fromisoformat(locked_until_raw)
                if timezone.is_naive(locked_until):
                    locked_until = timezone.make_aware(locked_until, timezone.get_current_timezone())
            except Exception:
                locked_until = None
            if locked_until and locked_until > now:
                remaining = int((locked_until - now).total_seconds() // 60) + 1
                messages.error(
                    request,
                    f"Слишком много попыток входа. Попробуйте через {remaining} мин.",
                )
            else:
                state["locked_until"] = None
                request.session.modified = True
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        state = self._state()
        state["attempts"] = []
        state["locked_until"] = None
        self.request.session.modified = True
        return super().form_valid(form)

    def form_invalid(self, form):
        state = self._state()
        now = timezone.now()
        window_start = now - timedelta(minutes=self.window_minutes)
        attempts = []
        for ts in state.get("attempts", []):
            try:
                parsed = timezone.datetime.fromisoformat(ts)
                if timezone.is_naive(parsed):
                    parsed = timezone.make_aware(parsed, timezone.get_current_timezone())
                if parsed >= window_start:
                    attempts.append(parsed)
            except Exception:
                continue
        attempts.append(now)
        state["attempts"] = [x.isoformat() for x in attempts]
        if len(attempts) >= self.max_attempts:
            state["locked_until"] = (now + timedelta(minutes=self.lock_minutes)).isoformat()
            messages.error(
                self.request,
                "Слишком много неудачных попыток. Вход временно ограничен.",
            )
        self.request.session.modified = True
        return super().form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        state = self._state()
        locked_until_raw = state.get("locked_until")
        if locked_until_raw:
            try:
                locked_until = timezone.datetime.fromisoformat(locked_until_raw)
                if timezone.is_naive(locked_until):
                    locked_until = timezone.make_aware(locked_until, timezone.get_current_timezone())
                if locked_until > timezone.now():
                    form.fields["username"].widget.attrs["disabled"] = True
                    form.fields["password"].widget.attrs["disabled"] = True
            except Exception:
                pass
        return form
