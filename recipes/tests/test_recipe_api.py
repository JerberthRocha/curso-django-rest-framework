from unicodedata import category
from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixin
from django.urls import reverse
from unittest.mock import patch


class RecipeAPIv2Test(test.APITestCase, RecipeMixin):
    def get_recipe_reverse_url(self, reverse_result=None):
        api_url = reverse_result or reverse('recipes:recipes-api-list')
        return api_url

    def get_recipe_api_list(self, reverse_result=None):
        api_url = self.get_recipe_reverse_url(reverse_result)
        response = self.client.get(api_url)
        return response

    def get_jwt_access_token(self):
        userdata = {
            'username': 'user',
            'password': 'password'
        }
        self.make_author(
            username=userdata.get('username'),
            password=userdata.get('password')
        )

        response = self.client.post(
            reverse('recipes:token_obtain_pair'),
            data={**userdata}
        )
        return response.data.get('access')
    
    def get_recipe_raw_data(self):
        return {
            'id': 50,
            'title': 'This is the title',
            'description': 'This is the description',
            'preparation_time': 1,
            'preparation_time_unit': 'Minutes',
            'servings': '1',
            'servings_unit': 'Person',
            'preparation_steps': 'This is the preparation steps'
        }

    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_recipe_api_list()
        self.assertEqual(
            response.status_code,
            200
        )

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        # AJUSTANDO OS DADOS
        wanted_number_of_recipes = 7
        self.make_recipe_in_batch(qtd=wanted_number_of_recipes)

        # EXECUTANDO A AÇÃO
        response = self.get_recipe_api_list()
        qtd_of_loaded_recipes = len(response.data.get('results'))

        # EXECUTANDO ASSERÇÃO
        self.assertEqual(
            wanted_number_of_recipes,
            qtd_of_loaded_recipes
        )

    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        recipes = self.make_recipe_in_batch(qtd=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        response = self.get_recipe_api_list()

        self.assertEqual(
            len(response.data.get('results')),
            1
        )

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=10)
    def test_recipe_api_lists_can_load_recipes_by_category_id(self):
        # CREATE CATEGORIES
        category_wanted = self.make_category(name='WANTED_CATEGORY')
        category_not_wanted = self.make_category(name='NOT_WANTED_CATEGORY')

        # CREATE 10 RECIPES
        recipes = self.make_recipe_in_batch(qtd=10)

        # CHANGE ALL RECIPES TO WANTED CATEGORY
        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()

        # CHANGE ONE RECIPE TO THE NOT WANTED CATEGORY
        # AS A RESULT, THIS RECIPE SHOULD NOT SHOW IN THE PAGE
        recipes[0].category = category_not_wanted
        recipes[0].save()

        # ACTION: GET RECIPES BY WANTED CATEGORY_ID
        api_url = reverse('recipes:recipes-api-list') + \
            f'?category_id={category_wanted.id}'
        response = self.get_recipe_api_list(reverse_result=api_url)

        # WE SHOULD ONLY SEE RECIPES FROM THE WANTED CATEGORY
        self.assertEqual(
            len(response.data.get('results')),
            9
        )

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        api_url = self.get_recipe_reverse_url()
        response = self.client.post(api_url)
        self.assertEqual(
            response.status_code,
            401
        )

    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        data = self.get_recipe_raw_data()
        response = self.client.post(
            self.get_recipe_reverse_url(),
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.get_jwt_access_token()}'
        )

        self.assertEqual(
            response.status_code, 
            201
        )
