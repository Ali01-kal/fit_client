import json

from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from clients.models import Client
from memberships.models import Subscription
from programs.models import Program
from reviews.models import Review


def error_response(message, status=400, code="bad_request"):
    return JsonResponse({"error": {"code": code, "message": message}}, status=status)


def paginate_queryset(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(request.GET.get("page"))
    return page_obj, {
        "count": paginator.count,
        "num_pages": paginator.num_pages,
        "page": page_obj.number,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
    }


@require_http_methods(["GET"])
def api_clients(request):
    qs = Client.objects.select_related("primary_trainer").all()
    if request.GET.get("search"):
        q = request.GET["search"]
        qs = qs.filter(Q(name__icontains=q) | Q(email__icontains=q))
    if request.GET.get("status") in {"active", "inactive"}:
        qs = qs.filter(is_active=request.GET["status"] == "active")
    if request.GET.get("trainer"):
        qs = qs.filter(primary_trainer_id=request.GET["trainer"])
    if request.GET.get("ordering") in {"name", "-name", "created_at", "-created_at"}:
        qs = qs.order_by(request.GET["ordering"])
    page_obj, meta = paginate_queryset(request, qs)
    return JsonResponse(
        {
            "results": [
                {
                    "id": c.id,
                    "name": c.name,
                    "slug": c.slug,
                    "email": c.email,
                    "phone": c.phone,
                    "is_active": c.is_active,
                    "trainer": c.primary_trainer.name if c.primary_trainer else None,
                }
                for c in page_obj.object_list
            ],
            "meta": meta,
        }
    )


@require_http_methods(["GET"])
def api_client_detail(request, slug):
    client = get_object_or_404(
        Client.objects.select_related("primary_trainer").prefetch_related("subscriptions__plan"),
        slug=slug,
    )
    return JsonResponse(
        {
            "id": client.id,
            "name": client.name,
            "slug": client.slug,
            "email": client.email,
            "phone": client.phone,
            "trainer": client.primary_trainer.name if client.primary_trainer else None,
            "subscriptions": [
                {
                    "id": s.id,
                    "plan": s.plan.name,
                    "status": s.status,
                    "starts_on": s.starts_on.isoformat(),
                    "ends_on": s.ends_on.isoformat(),
                }
                for s in client.subscriptions.select_related("plan").all()
            ],
        }
    )


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_programs(request):
    if request.method == "GET":
        qs = Program.objects.select_related("trainer", "category").all()
        filters = {
            "search": request.GET.get("search"),
            "category": request.GET.get("category"),
            "difficulty": request.GET.get("difficulty"),
            "trainer": request.GET.get("trainer"),
        }
        if filters["search"]:
            q = filters["search"]
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        if filters["category"]:
            qs = qs.filter(category_id=filters["category"])
        if filters["difficulty"]:
            qs = qs.filter(difficulty=filters["difficulty"])
        if filters["trainer"]:
            qs = qs.filter(trainer_id=filters["trainer"])
        if request.GET.get("ordering") in {"name", "-name", "duration_minutes", "-duration_minutes"}:
            qs = qs.order_by(request.GET["ordering"])
        page_obj, meta = paginate_queryset(request, qs)
        return JsonResponse(
            {
                "results": [
                    {
                        "id": p.id,
                        "name": p.name,
                        "slug": p.slug,
                        "difficulty": p.difficulty,
                        "trainer": p.trainer.name if p.trainer else None,
                        "category": p.category.name if p.category else None,
                        "duration_minutes": p.duration_minutes,
                    }
                    for p in page_obj.object_list
                ],
                "meta": meta,
            }
        )
    if not request.user.is_authenticated:
        return error_response("Authentication required", 403, "forbidden")
    if not (request.user.is_staff or request.user.groups.filter(name="manager").exists()):
        return error_response("Insufficient permissions", 403, "forbidden")
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return error_response("Invalid JSON")
    for field in ("name", "description", "difficulty"):
        if not payload.get(field):
            return error_response(f"Field '{field}' is required")
    program = Program.objects.create(
        name=payload["name"],
        description=payload["description"],
        difficulty=payload["difficulty"],
        duration_minutes=payload.get("duration_minutes", 60),
        max_clients=payload.get("max_clients", 10),
        trainer_id=payload.get("trainer"),
        category_id=payload.get("category"),
    )
    return JsonResponse({"id": program.id, "slug": program.slug, "name": program.name}, status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_program_detail(request, slug):
    program = get_object_or_404(Program, slug=slug)
    if request.method == "GET":
        return JsonResponse(
            {
                "id": program.id,
                "name": program.name,
                "slug": program.slug,
                "description": program.description,
                "difficulty": program.difficulty,
                "duration_minutes": program.duration_minutes,
                "max_clients": program.max_clients,
            }
        )
    if not request.user.is_authenticated:
        return error_response("Authentication required", 403, "forbidden")
    if not (request.user.is_staff or request.user.groups.filter(name="manager").exists()):
        return error_response("Insufficient permissions", 403, "forbidden")
    if request.method == "DELETE":
        program.delete()
        return JsonResponse({"deleted": True})
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return error_response("Invalid JSON")
    for field in ["name", "description", "difficulty", "duration_minutes", "max_clients"]:
        if field in payload:
            setattr(program, field, payload[field])
    if "trainer" in payload:
        program.trainer_id = payload["trainer"]
    if "category" in payload:
        program.category_id = payload["category"]
    try:
        program.full_clean()
        program.save()
    except Exception as exc:
        return error_response(str(exc))
    return JsonResponse({"updated": True})


@require_http_methods(["GET"])
def api_subscriptions(request):
    qs = Subscription.objects.select_related("client", "plan").all()
    if request.GET.get("status"):
        qs = qs.filter(status=request.GET["status"])
    if request.GET.get("client"):
        qs = qs.filter(client_id=request.GET["client"])
    page_obj, meta = paginate_queryset(request, qs)
    return JsonResponse(
        {
            "results": [
                {
                    "id": s.id,
                    "client": s.client.name,
                    "plan": s.plan.name,
                    "status": s.status,
                    "starts_on": s.starts_on.isoformat(),
                    "ends_on": s.ends_on.isoformat(),
                }
                for s in page_obj.object_list
            ],
            "meta": meta,
        }
    )


@require_http_methods(["GET"])
def api_reviews(request):
    qs = Review.objects.select_related("client", "program", "trainer").all()
    if request.GET.get("rating"):
        qs = qs.filter(rating=request.GET["rating"])
    if request.GET.get("program"):
        qs = qs.filter(program_id=request.GET["program"])
    page_obj, meta = paginate_queryset(request, qs)
    return JsonResponse(
        {
            "results": [
                {
                    "id": r.id,
                    "client": r.client.name,
                    "program": r.program.name if r.program else None,
                    "trainer": r.trainer.name if r.trainer else None,
                    "rating": r.rating,
                    "comment": r.comment,
                    "published": r.is_published,
                }
                for r in page_obj.object_list
            ],
            "meta": meta,
        }
    )


@require_http_methods(["GET"])
def api_stats(request):
    subs_by_status = list(
        Subscription.objects.values("status").annotate(total=Count("id")).order_by("status")
    )
    top_trainers = list(
        Program.objects.values("trainer__name")
        .exclude(trainer__isnull=True)
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )
    avg_rating = Review.objects.aggregate(v=Avg("rating"))["v"] or 0
    return JsonResponse(
        {
            "subscriptions_by_status": subs_by_status,
            "top_trainers": top_trainers,
            "avg_rating": avg_rating,
        }
    )
