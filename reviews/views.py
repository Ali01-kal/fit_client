from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ReviewForm
from .models import Review


def review_list(request):
    qs = Review.objects.select_related("client", "program", "trainer").all()
    if request.GET.get("rating"):
        qs = qs.filter(rating=request.GET["rating"])
    if request.GET.get("published") in {"0", "1"}:
        qs = qs.filter(is_published=request.GET["published"] == "1")
    page_obj = Paginator(qs, 10).get_page(request.GET.get("page"))
    avg_rating = qs.aggregate(v=Avg("rating"))["v"] or 0
    return render(
        request,
        "reviews/review_list.html",
        {"page_obj": page_obj, "reviews": page_obj.object_list, "avg_rating": avg_rating},
    )


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/review_form.html"
    success_url = reverse_lazy("reviews:list")

    def form_valid(self, form):
        messages.success(self.request, "Отзыв сохранён.")
        return super().form_valid(form)
