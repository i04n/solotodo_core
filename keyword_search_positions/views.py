from django_filters import rest_framework

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import list_route, detail_route

from solotodo_core.s3utils import PrivateS3Boto3Storage
from .forms.keyword_search_current_positions_form import \
    KeywordSearchCurrentPositionsForm
from .models import KeywordSearch, KeywordSearchUpdate, \
    KeywordSearchEntityPosition
from .pagination import KeywordSearchUpdatePagination
from .serializers import KeywordSearchSerializer, \
    KeywordSearchUpdateSerializer, KeywordSearchCreationSerializer, \
    KeywordSearchEntityPositionSerializer
from .filters import KeywordSearchUpdateFilterSet


class KeywordSearchViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = KeywordSearch.objects.all()
    serializer_class = KeywordSearchSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return KeywordSearch.objects.none()
        elif user.is_superuser:
            return KeywordSearch.objects.all()
        else:
            return KeywordSearch.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return KeywordSearchCreationSerializer
        else:
            return KeywordSearchSerializer

    @list_route(methods=['get'])
    def current_positions_report(self, request):
        user = request.user
        form = KeywordSearchCurrentPositionsForm(user, request.GET)

        if not form.is_valid():
            return Response({
                'errors': form.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        report_path = form.generate_report(user)['path']

        storage = PrivateS3Boto3Storage()
        report_url = storage.url(report_path)
        return Response({
            'url': report_url
        })


class KeywordSearchUpdateViewSet(mixins.RetrieveModelMixin,
                                 mixins.ListModelMixin,
                                 viewsets.GenericViewSet):
    queryset = KeywordSearchUpdate.objects.all()
    serializer_class = KeywordSearchUpdateSerializer
    filter_backends = (rest_framework.DjangoFilterBackend, SearchFilter,
                       OrderingFilter)
    filter_class = KeywordSearchUpdateFilterSet
    pagination_class = KeywordSearchUpdatePagination

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return KeywordSearchUpdate.objects.none()
        elif user.is_superuser:
            return KeywordSearchUpdate.objects.all()
        else:
            return KeywordSearchUpdate.objects.filter(search__user=user)

    @detail_route()
    def positions(self, request, pk):
        update = self.get_object()
        positions = update.positions.all().select_related('entity')
        serializer = KeywordSearchEntityPositionSerializer(
            positions, many=True, context={'request': request})

        return Response(serializer.data)


class KeywordSearchEntityPositionViewSet(mixins.RetrieveModelMixin,
                                         mixins.ListModelMixin,
                                         viewsets.GenericViewSet):
    queryset = KeywordSearchEntityPosition.objects.all()
    serializer_class = KeywordSearchEntityPositionSerializer
    pagination_class = KeywordSearchUpdatePagination

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return KeywordSearchEntityPosition.objects.none()
        elif user.is_superuser:
            return KeywordSearchEntityPosition.objects.all()
        else:
            return KeywordSearchEntityPosition.objects.filter(
                update__search__user=user)
