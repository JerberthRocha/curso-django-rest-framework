from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipe_detail_url_is_correct(self):
        url = reverse('recipes:recipe', kwargs={'pk': 1})  # args=(1,)
        self.assertEqual(url, '/recipes/1/')

    def test_recipe_category_url_is_correct(self):
        # kwargs={'category_id':1}
        url = reverse('recipes:category', args=(1,))
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipe_search_url_is_correct(self):
        # kwargs={'category_id':1}
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')

