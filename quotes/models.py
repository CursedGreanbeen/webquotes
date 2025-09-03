from django.db import models


class Source(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    objects = models.Manager()

    text = models.TextField(unique=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    weight = models.PositiveIntegerField(default=1)
    views = models.IntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'"{self.text}" - {self.source}'
