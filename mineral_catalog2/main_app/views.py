import random
from django.shortcuts import render, get_object_or_404
from .models import Mineral


def mineral_list(request):
    """
    Minerals list view, gets all the minerals entries objects
    in addition, chooses a random mineral object.
    Finally sends for a template rendering
    :return: rendered html template object
    """
    minerals = Mineral.objects.all()
    random_mineral = random.choice(minerals)
    return render(request, 'main_app/index.html',
                  {'minerals': minerals,
                   'random_mineral': random_mineral})


def mineral_detail(request, pk):
    """
    Single mineral detail view, tries to get the requested
    mineral entry object.
    in addition:
        sets the categories order by the most common attributes
        chooses a random mineral object.
    Finally sends for a template rendering
    :return: rendered html template object
    """
    mineral = get_object_or_404(Mineral, pk=pk)
    # The category order for displaying the most common first.
    ordered_category = [
        'category',
        'group',
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
        'streak',
        'optical_properties',
        'refractive_index',
        'unit_cell',
        'crystal_symmetry',
    ]
    # getting the most common categories attributes for the requested mineral
    net_mineral_attributes = []
    for category in ordered_category:
        attribute_value = getattr(mineral, category, False)
        if attribute_value:
            net_mineral_attributes.append({category: attribute_value})
    # choosing a random mineral entry object
    random_mineral = random.choice(Mineral.objects.all())
    return render(request,
                  'main_app/mineral_detail.html',
                  {
                      'mineral': mineral,
                      'net_mineral_attributes': net_mineral_attributes,
                      'random_mineral': random_mineral,
                  }
                  )



