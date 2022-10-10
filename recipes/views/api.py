from functools import partial
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from tag.models import Tag
from rest_framework.views import APIView


class RecipeAPIv2List(APIView):
    def get(self, request):
        recipes = Recipe.objects.get_published()[:5]
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RecipeSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            author_id=1,
            category_id=1,
            tags=[3, 4]
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class RecipeAPIv2Detail(APIView):
    def get_recipe(self, pk):
        recipe = get_object_or_404(
            Recipe.objects.get_published(),
            pk=pk
        )
        return recipe

    def get(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(
            instance=recipe,
            context={'request': request},
        )
        return Response(serializer.data)

    def patch(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data
        )

    def delete(self, request, pk):
        recipe = self.get_recipe(pk)
        recipe.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
        # many=False,
        # context={'request': request},
    )
    return Response(serializer.data)
