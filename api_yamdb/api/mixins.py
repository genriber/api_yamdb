from rest_framework import viewsets, mixins


class RestrictedActionsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Кастомный вьюсет (миксин)
    который ограничивает методы взаимодействия
    согласно документации.
    """

    pass
