from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from ..serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status


@api_view()
def recipe_api_list(request):
    recipes = Recipe.objects.get_published()[:5]
    serializer = RecipeSerializer(instance=recipes, many=True)
    return Response(serializer.data)


@api_view()
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk
    )
    serializer = RecipeSerializer(instance=recipe)
    return Response(serializer.data)


    #MUDANDO MENSAGEM E STATUS CODE
    # recipe = Recipe.objects.get_published().filter(pk=pk).first()
    
    # if recipe:
    #     serializer = RecipeSerializer(instance=recipe)
    #     return Response(serializer.data)
    # else:
    #     return Response({
    #         'detail': 'Não encontrado'
    #     }, status=status.HTTP_418_IM_A_TEAPOT)