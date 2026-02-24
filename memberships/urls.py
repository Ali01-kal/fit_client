from django.urls import path

from .views import MembershipPlanCreateView, SubscriptionCreateView, SubscriptionListView, membership_plan_list

urlpatterns = [
    path("plans/", membership_plan_list, name="plans"),
    path("plans/create/", MembershipPlanCreateView.as_view(), name="plan_create"),
    path("plans/<slug:slug>/subscriptions/", SubscriptionListView.as_view(), name="plan_subscriptions"),
    path("subscriptions/create/", SubscriptionCreateView.as_view(), name="subscription_create"),
]
