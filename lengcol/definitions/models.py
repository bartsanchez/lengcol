from django.db import models


class Term(models.Model):
    value = models.CharField(max_length=255)


class Definition(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    value = models.TextField()
