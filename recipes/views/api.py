from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from ..serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from tag.models import Tag
from ..serializers import TagSerializer


@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.get_published()[:5]
        serializer = RecipeSerializer(
            instance=recipes, 
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)
    elif request.method == 'POST':
        return Response('POST', status.HTTP_201_CREATED)


@api_view()
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk
    )
    serializer = RecipeSerializer(
        instance=recipe, 
        context={'request': request},
    )
    return Response(serializer.data)


    #MUDANDO MENSAGEM E STATUS CODE
    # recipe = Recipe.objects.get_published().filter(pk=pk).first()
    
    # if recipe:
    #     serializer = RecipeSerializer(instance=recipe)
    #     return Response(serializer.data)
    # else:
    #     return Response({
    #         'detail': 'Não encontrTag   #     }, status=status.HTTP_418_IM_A_TEAPOT)

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