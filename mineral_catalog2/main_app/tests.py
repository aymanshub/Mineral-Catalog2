from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.db import models

from .models import Mineral


class MineralViewTests(TestCase):
    def setUp(self):
        self.default_organic_gray_mineral = Mineral.objects.create(
            # A default mineral name should starts with 'A' letter
            name="Aowan",
            image_filename="240px-Abramovite.jpg",
            image_caption='one of the very old stones',
            category='Organic',
            streak='light gray',
        )

        self.b_organic_haze_mineral = Mineral.objects.create(
            # A non-default mineral name should starts with not 'A' letter
            name="Beeri",
            category='Organic',
            streak='haze'
        )
        self.b_new_gray_mineral = Mineral.objects.create(
            # A non-default mineral name should starts with not 'A' letter
            name="borkani",
            category='new',
            streak='light gray',
        )

        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_homepage_default_view(self):
        response = self.client.get(reverse('minerals:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.default_organic_gray_mineral,
                      response.context['minerals'])
        self.assertNotIn(self.b_organic_haze_mineral,
                         response.context['minerals'])
        self.assertNotIn(self.b_new_gray_mineral,
                         response.context['minerals'])
        self.assertTemplateUsed(response, 'main_app/index.html')
        self.assertTemplateNotUsed(response, 'main_app/mineral_detail.html')
        self.assertEqual(True,
                         self.default_organic_gray_mineral
                         .name.upper().startswith('A'))
        self.assertEqual(len(response.context['minerals']), 1)
        self.assertContains(response,
                            self.default_organic_gray_mineral.name)

    def test_by_letter_list_view(self):
        response = self.client.get(reverse('minerals:list_by_letter',
                                           kwargs={'letter': 'B'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.b_organic_haze_mineral,
                      response.context['minerals'])
        self.assertIn(self.b_new_gray_mineral,
                      response.context['minerals'])
        self.assertNotIn(self.default_organic_gray_mineral,
                         response.context['minerals'])
        self.assertEquals(len(response.context['minerals']), 2)
        self.assertEqual(True,
                         self.b_organic_haze_mineral
                         .name.upper().startswith('B'))
        self.assertTemplateUsed(response, 'main_app/index.html')

    def test_by_category_list_view(self):
        response = self.client.get(reverse(
            'minerals:list_by_category', kwargs={
                'selected_category':
                    slugify(self.b_organic_haze_mineral.category)
            }
        ))

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.b_organic_haze_mineral,
                      response.context['minerals'])
        self.assertIn(self.default_organic_gray_mineral,
                      response.context['minerals'])
        self.assertEquals(len(response.context['minerals']), 2)
        self.assertTemplateUsed(response, 'main_app/index.html')

    def test_by_streak_list__view(self):
        response = self.client.get(reverse(
            'minerals:list_by_streak', kwargs={
                'selected_streak':
                    slugify(self.default_organic_gray_mineral.streak)
            }
        ))

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.default_organic_gray_mineral,
                      response.context['minerals'])
        self.assertIn(self.b_new_gray_mineral,
                      response.context['minerals'])
        self.assertEquals(len(response.context['minerals']), 2)

    def test_random_mineral_functionality(self):
        response = self.client.get(reverse('minerals:list'))
        self.assertEqual(response.status_code, 200)
        # random_mineral
        self.assertIn(response.context['random_mineral'],
                      [
                          self.default_organic_gray_mineral,
                          self.b_organic_haze_mineral,
                          self.b_new_gray_mineral,
                      ]
                      )

    def test_mineral_detail_view(self):
        response = self.client.get(
            reverse('minerals:detail',
                    kwargs={'pk': self.default_organic_gray_mineral.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/mineral_detail.html')

        # the selected mineral for this test has only 5 attributes:
        self.assertContains(response,
                            self.default_organic_gray_mineral.name)
        self.assertContains(response,
                            self.default_organic_gray_mineral.image_filename)
        self.assertContains(response,
                            self.default_organic_gray_mineral.image_caption)
        self.assertContains(response,
                            self.default_organic_gray_mineral.category)
        self.assertContains(response,
                            self.default_organic_gray_mineral.streak)

        # making sure all other "ordered_category" attributes are not
        # contained in the details page according to mineral_detail view
        ordered_category = [
            'formula',
            'strunz_classification',
            'crystal_system',
            'mohs_scale_hardness',
            'luster',
            'color',
            'specific_gravity',
            'cleavage',
            'diaphaneity',
            'crystal_habit',
            'optical_properties',
            'refractive_index',
            'unit_cell',
            'crystal_symmetry',
        ]

        for attribute in ordered_category:
            self.assertNotContains(response, attribute)

    def test_search_view(self):
        response = self.client.get(reverse('minerals:search'),
                                   {
                                       'q':
                                           self.default_organic_gray_mineral
                                   .streak.split()[-1],
                                   })
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.default_organic_gray_mineral,
                      response.context['minerals'])
        self.assertIn(self.b_new_gray_mineral,
                      response.context['minerals'])
        self.assertNotIn(self.b_organic_haze_mineral.name,
                         response.context['minerals'])


class ModelTests(TestCase):

    def test_mineral_model_field_types(self):
        # Verifies if Model fields types are correct
        for field in Mineral._meta.fields:
            if not field.name == 'id':
                self.assertEqual(isinstance(field, models.CharField), True)
