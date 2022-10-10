from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer
from django.shortcuts import get_object_or_404
from tag.models import Tag
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination


class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
    )
    return Response(serializer.data)
