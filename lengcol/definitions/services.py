from definitions import models


class ObjectGathering:
    @classmethod
    def _objects(cls):
        return cls.model.objects

    @classmethod
    def _get_objects(cls, order_by=None, items=None):
        objects = cls._objects()
        if order_by:
            objects = objects.order_by(order_by)

        return objects.all()[:items]

    @classmethod
    def _get_last_objects(cls, items=5):
        return cls._get_objects(order_by='-created', items=items)


class DefinitionGathering(ObjectGathering):
    model = models.Definition

    @classmethod
    def _get_definitions(cls, order_by=None, items=None):
        return cls._get_objects(order_by, items)

    @classmethod
    def get_last_definitions(cls, items=5):
        return cls._get_last_objects(items=items)


class TermGathering(ObjectGathering):
    model = models.Term

    @classmethod
    def _get_terms(cls, order_by=None, items=None):
        return cls._get_objects(order_by, items)

    @classmethod
    def get_last_terms(cls, items=5):
        return cls._get_last_objects(items=items)
