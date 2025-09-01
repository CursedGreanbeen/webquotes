from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    objects = models.Manager()

    text = models.TextField(unique=True)  # unique=True для предотвращения дубликатов цитат
    source = models.ForeignKey(Source, on_delete=models.CASCADE)  # Связь "многие к одному"
    weight = models.PositiveIntegerField(default=1)  # "Вес" цитаты
    views = models.IntegerField(default=0)  # Счетчик просмотров
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'"{self.text}" - {self.source}'
