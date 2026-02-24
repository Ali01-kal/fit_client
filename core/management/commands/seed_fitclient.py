from datetime import date, timedelta
import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from clients.models import Client
from memberships.models import MembershipPlan, Subscription
from programs.models import Equipment, Exercise, Program, ProgramCategory
from trainers.models import Trainer


class Command(BaseCommand):
    help = "Seed demo data for fitClient"

    def handle(self, *args, **options):
        User.objects.get_or_create(username="manager", defaults={"email": "manager@example.com"})
        trainer, _ = Trainer.objects.get_or_create(
            email="trainer1@example.com",
            defaults={"name": "Айбек Тренер", "specialization": "Crossfit", "experience_years": 5},
        )
        category, _ = ProgramCategory.objects.get_or_create(name="Функциональный тренинг")
        equipment_defs = [
            ("Гантели", {"quantity": 20, "is_available": True}),
            ("Штанга", {"quantity": 8, "is_available": True}),
            ("Коврик", {"quantity": 30, "is_available": True}),
            ("Эспандер", {"quantity": 25, "is_available": True}),
            ("Скакалка", {"quantity": 18, "is_available": True}),
            ("TRX", {"quantity": 6, "is_available": True}),
            ("Гиря 16кг", {"quantity": 10, "is_available": True}),
        ]
        equipments = []
        for eq_name, eq_defaults in equipment_defs:
            eq, _ = Equipment.objects.get_or_create(name=eq_name, defaults=eq_defaults)
            equipments.append(eq)

        for i in range(1, 6):
            program, _ = Program.objects.get_or_create(
                name=f"Программа {i}",
                defaults={
                    "description": "Демо программа тренировок",
                    "trainer": trainer,
                    "category": category,
                    "difficulty": random.choice(["beginner", "mid", "pro"]),
                    "duration_minutes": random.choice([45, 50, 60, 75]),
                },
            )
            # Attach 2-4 equipment items per program.
            selected_equipment = random.sample(equipments, k=random.randint(2, 4))
            program.equipments.add(*selected_equipment)

            # Ensure each program has a set of exercises.
            exercise_templates = [
                ("Разминка", 1, 10, 20),
                ("Приседания", 4, 12, 60),
                ("Отжимания", 4, 10, 45),
                ("Планка", 3, 1, 40),
                ("Тяга", 4, 12, 60),
                ("Берпи", 3, 12, 50),
            ]
            chosen = random.sample(exercise_templates, k=4)
            for idx, (ex_name, sets, reps, rest) in enumerate(chosen, start=1):
                Exercise.objects.get_or_create(
                    program=program,
                    name=ex_name,
                    defaults={
                        "sets": sets,
                        "reps": reps,
                        "rest_seconds": rest,
                        "sort_order": idx,
                    },
                )
        plans = []
        plan_defs = [
            ("Старт 8", {"price": 12000, "duration_days": 30, "visit_limit": 8}),
            ("Стандарт 12", {"price": 18000, "duration_days": 30, "visit_limit": 12}),
            ("Стандарт 16", {"price": 22000, "duration_days": 30, "visit_limit": 16}),
            ("Премиум 20", {"price": 28000, "duration_days": 30, "visit_limit": 20}),
            ("Безлимит 30", {"price": 26000, "duration_days": 30, "visit_limit": 999}),
            ("Утренний 12", {"price": 14000, "duration_days": 30, "visit_limit": 12}),
            ("Квартал 36", {"price": 48000, "duration_days": 90, "visit_limit": 36}),
            ("Квартал Безлимит", {"price": 69000, "duration_days": 90, "visit_limit": 999}),
            ("Полугодовой 72", {"price": 92000, "duration_days": 180, "visit_limit": 72}),
            ("Полугодовой Безлимит", {"price": 129000, "duration_days": 180, "visit_limit": 999}),
            ("Годовой 144", {"price": 169000, "duration_days": 365, "visit_limit": 144}),
            ("Годовой Безлимит", {"price": 239000, "duration_days": 365, "visit_limit": 999}),
            ("VIP 90", {"price": 75000, "duration_days": 90, "visit_limit": 999}),
        ]
        for plan_name, defaults in plan_defs:
            plan, _ = MembershipPlan.objects.get_or_create(name=plan_name, defaults=defaults)
            plans.append(plan)
        for i in range(1, 11):
            client, _ = Client.objects.get_or_create(
                email=f"client{i}@example.com",
                defaults={"name": f"Клиент {i}", "phone": f"+770700000{i:02d}", "primary_trainer": trainer},
            )
            selected_plan = plans[(i - 1) % len(plans)]
            status = random.choice(["active", "active", "active", "paused", "expired"])
            Subscription.objects.get_or_create(
                client=client,
                plan=selected_plan,
                starts_on=date.today() - timedelta(days=i),
                defaults={"status": status, "visits_used": random.randint(0, min(selected_plan.visit_limit, 15))},
            )
        self.stdout.write(self.style.SUCCESS("Seed data created"))
