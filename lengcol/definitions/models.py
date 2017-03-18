from django.db import models


class Term(models.Model):
    value = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.value


class Definition(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    value = models.TextField()

    def __str__(self):
        return self.value
