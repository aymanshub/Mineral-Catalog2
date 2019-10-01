import random
from django.shortcuts import render, get_object_or_404
from .models import Mineral
from django.db.models import Q
from django.template.defaultfilters import slugify


def get_categories(slugged=False):

    # getting all distinct categories
    categories_raw = Mineral.objects.values_list('category', flat=True) \
        .distinct().order_by('category')

    categories_raw = list(categories_raw)

    if slugged:
        slugged_list = [slugify(cate) for cate in categories_raw]
        return slugged_list
    else:
        return categories_raw


def get_random_mineral():
    minerals_all = Mineral.objects.all()
    random_mineral = random.choice(minerals_all)

    return random_mineral


def mineral_list(request, letter='a', slugged_category=None):
    """
    Minerals list view, gets all the requested minerals objects
    either by their first letter name or by category
    in addition, chooses a random mineral object.
    :return: rendered html template object
    """

    raw_list = get_categories(slugged=False)
    # slugged_list = list(zip(*categories_list_noneed))[0]
    slugged_list = get_categories(slugged=True)

    # removing all duplicate slugs having unique ordered list
    categories_list = sorted(set(slugged_list))

    if slugged_category:
        # finding out all the raw categories that belong to the same slug
        category_indexes = []
        for index, item in enumerate(slugged_list):
            if item == slugged_category:
                category_indexes.append(index)

        minerals_by_category = Mineral.objects.filter(
            category__in=[raw_list[index] for index in category_indexes]
        )
        minerals = minerals_by_category
        letter = None
    else:
        minerals_by_letter = Mineral.objects.filter(name__startswith=letter)
        minerals = minerals_by_letter

    # random mineral
    random_mineral = get_random_mineral()

    return render(request, 'main_app/index.html',
                  {'minerals': minerals,
                   'random_mineral': random_mineral,
                   'categories_list': categories_list,
                   'selected_letter': letter,
                   'selected_category': slugged_category,
                   })


def search(request):
    """
    Gets all the minerals objects whose any field contains the search term.
    The names of the minerals that match the search will
    be displayed in the list view.
    in addition, chooses a random mineral object.
    :return: rendered html template object
    """
    term = request.GET.get('q')

    # filter using Q objects for OR relation search
    minerals_found = Mineral.objects.filter(
        Q(name__icontains=term) |
        Q(image_caption__icontains=term) |
        Q(category__icontains=term) |
        Q(formula__icontains=term) |
        Q(strunz_classification__icontains=term) |
        Q(color__icontains=term) |
        Q(crystal_system__icontains=term) |
        Q(unit_cell__icontains=term) |
        Q(crystal_symmetry__icontains=term) |
        Q(cleavage__icontains=term) |
        Q(mohs_scale_hardness__icontains=term) |
        Q(luster__icontains=term) |
        Q(streak__icontains=term) |
        Q(diaphaneity__icontains=term)|
        Q(optical_properties__icontains=term) |
        Q(refractive_index__icontains=term) |
        Q(crystal_habit__icontains=term) |
        Q(specific_gravity__icontains=term) |
        Q(group__icontains=term)
    )

    slugged_list = get_categories(slugged=True)
    # removing all duplicate slugs having unique ordered list
    categories_list = sorted(set(slugged_list))
    random_mineral = get_random_mineral()

    return render(request, 'main_app/index.html',
                  {'minerals': minerals_found,
                   'random_mineral': random_mineral,
                   'categories_list': categories_list,
                   })


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
    random_mineral = get_random_mineral()

    # slugging all categories
    slugged_list = get_categories(slugged=True)

    # removing all duplicate slugs having unique ordered list
    categories_list = sorted(set(slugged_list))

    return render(request,
                  'main_app/mineral_detail.html',
                  {
                      'mineral': mineral,
                      'net_mineral_attributes': net_mineral_attributes,
                      'random_mineral': random_mineral,
                      'categories_list': categories_list,
                  }
                  )



