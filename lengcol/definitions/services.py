from definitions import models


class DefinitionGathering:
    @classmethod
    def _objects(cls):
        return models.Definition.objects

    @classmethod
    def _get_definitions(cls, order_by=None, items=None):
        objects = cls._objects()
        if order_by:
            objects = objects.order_by(order_by)

        return objects.all()[:items]

    @classmethod
    def get_last_definitions(cls, items=5):
        return cls._get_definitions(order_by='-created', items=items)
