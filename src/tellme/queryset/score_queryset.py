from django.db import models


class ScoreQuerySet(models.QuerySet):
    def fetch_latest(self, limit=15):
        return self.all().order_by('-date_created')[:limit]