from django.test import TestCase
from django.urls import reverse

from .models import Mineral


class MineralViewTests(TestCase):
    def setUp(self):
        self.mineral = Mineral.objects.create(
            name="Mineral A",
            image_filename="Zunyite.jpg",
            image_caption="This is a test image caption!",
            category="Mineral tests",
            formula="a Operator should be first",
            strunz_classification="",
            color="ColorA",
            group="test groupA"
        )
        self.mineral2 = Mineral.objects.create(
            name="Mineral B",
            image_filename="Zunyite.jpg",
            image_caption="This is a test image caption!",
            category="Mineral tests",
            formula="b Operator should be first",
            strunz_classification="",
            color="ColorB",
            group="test groupB",
        )

    def test_mineral_list_view(self):
        resp = self.client.get(reverse('minerals:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral, resp.context['minerals'])
        self.assertIn(self.mineral2, resp.context['minerals'])
        self.assertTemplateUsed(resp, 'main_app/index.html')
        self.assertContains(resp, self.mineral.name)
        self.assertContains(resp, self.mineral2.name)

    def test_mineral_detail_view(self):
        resp = self.client.get(reverse('minerals:detail',
                                       kwargs={'pk': self.mineral.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.mineral.name)
        self.assertContains(resp, self.mineral.image_filename)
        self.assertContains(resp, self.mineral.image_caption)
        self.assertContains(resp, self.mineral.category)
        self.assertContains(resp, self.mineral.formula)
        self.assertContains(resp, self.mineral.strunz_classification)
        self.assertContains(resp, self.mineral.color)
        self.assertContains(resp, self.mineral.group)



