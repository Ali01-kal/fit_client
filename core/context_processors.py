from clients.models import Client
from programs.models import Program
from trainers.models import Trainer


def global_stats(request):
    try:
        return {
            "global_stats": {
                "clients": Client.objects.count(),
                "trainers": Trainer.objects.count(),
                "programs": Program.objects.count(),
            }
        }
    except Exception:
        return {"global_stats": {"clients": 0, "trainers": 0, "programs": 0}}
