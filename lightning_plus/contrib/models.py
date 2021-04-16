from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F
from django.shortcuts import get_object_or_404 as _get_object_or_404

from .exceptions import NotFound


def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError, ValidationError):
        raise NotFound


# TODO: pagination


class BaseManager(models.Manager):
    def get_or_404(self, pk):
        return get_object_or_404(super().get_queryset().filter(pk=pk))

    def first_or_404(self, **kwargs):
        return get_object_or_404(super().get_queryset().filter(**kwargs))


class Model(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True

    objects = BaseManager()
    queryset = BaseManager()

    @classmethod
    def filter(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs)

    @classmethod
    def get(cls, pk):
        return cls.objects.get(pk=pk)

    @classmethod
    def get_or_404(cls, **kwargs) -> Model:
        return get_object_or_404(cls.objects.filter(**kwargs))

    @classmethod
    def find_or_404(cls, **kwargs) -> Model:
        return get_object_or_404(cls.objects.filter(**kwargs))

    @classmethod
    def find_first(cls, **kwargs) -> Model:
        return cls.objects.filter(**kwargs).first()

    @classmethod
    def one_or_404(cls, **kwargs) -> Model:
        return get_object_or_404(cls.objects.filter(**kwargs))

    @classmethod
    def first_or_404(cls, **kwargs) -> Model:
        return get_object_or_404(cls.objects.filter(**kwargs))

    def incr(self, field):
        return self.__class__.objects.filter(id=self.id).update(**{field: F(field) + 1})

    def decr(self, field):
        return self.__class__.objects.filter(id=self.id).update(**{field: F(field) - 1})

    def to_dict(self, fields: list[str]) -> dict:
        raise NotImplementedError
