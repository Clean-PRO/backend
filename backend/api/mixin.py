from rest_framework import mixins, viewsets


class CreateUpdateListSet(
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet,
        ): # noqa (E123)
    pass
