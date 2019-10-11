import random
from django.shortcuts import render, get_object_or_404
from .models import Mineral
from django.db.models import Q
from django.template.defaultfilters import slugify


def raw_values(attribute_name):
    """
    Gets all values of the requested attribute_name based on the DB values
    :param attribute_name: String representation of the attribute name
    :return: A new list, having distinct values of the attribute name parameter
    """
    # getting all distinct attribute names
    names_raw = Mineral.objects.values_list(attribute_name, flat=True) \
        .distinct().order_by(attribute_name)

    return list(names_raw)


def slug_em(names):
    """
    Slugs all the names list items
    :param names: String list of names
    :return: a new slugged names list
    """
    return [slugify(name) for name in names]


def get_random_mineral():
    """
    Gets a random mineral from the existing minerals table
    :return: A single Mineral object
    """
    minerals_all = Mineral.objects.all()
    random_mineral = random.choice(minerals_all)

    return random_mineral


def get_minerals_by(attribute_name, raw_values_list, slugged_values_list,
                    selected_value):
    """
    Gets all minerals having attribute_name with the selected_value
    :param slugged_values_list: helper list of slugged_values_list
    :param raw_values_list: helper list of raw_values_list
    :param attribute_name: string of Mineral attribute
    :param selected_value: string of the selected Mineral attribute value
    :return: A Queryset of all minerals objects having the attribute_name with
    selected_value
    """

    # finding out all the raw categories that belong to the same slug
    value_indexes = []
    for index, item in enumerate(slugged_values_list):
        if item == selected_value:
            value_indexes.append(index)

    lookup = attribute_name+'__'+'in'

    minerals_by_attribute = Mineral.objects.filter(
        **{lookup: [raw_values_list[index] for index in value_indexes]}
    )

    return minerals_by_attribute


def mineral_list(request, letter='a',
                 selected_category=None,
                 selected_streak=None):
    """
    Minerals list view, gets all the requested minerals objects
    either by their first letter name or by category
    in addition, chooses a random mineral object.
    :return: rendered html template object
    """

    # removing all duplicates, having a unique ordered list
    raw_categories = raw_values('category')
    slugged_categories = slug_em(raw_categories)
    categories_list = sorted(set(slugged_categories))

    raw_streaks = raw_values('streak')
    slugged_streaks = slug_em(raw_streaks)
    streaks_list = sorted(set(slugged_streaks))

    if selected_category:
        minerals = get_minerals_by('category', raw_categories,
                                   slugged_categories, selected_category)
        selected_streak = None
        letter = None
    elif selected_streak:
        minerals = get_minerals_by('streak', raw_streaks,
                                   slugged_streaks, selected_streak)
        selected_category = None
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
                   'streaks_list': streaks_list,
                   'selected_letter': letter,
                   'selected_category': selected_category,
                   'selected_streak': selected_streak,
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
        Q(diaphaneity__icontains=term) |
        Q(optical_properties__icontains=term) |
        Q(refractive_index__icontains=term) |
        Q(crystal_habit__icontains=term) |
        Q(specific_gravity__icontains=term) |
        Q(group__icontains=term)
    )

    raw_categories = raw_values('category')
    slugged_categories = slug_em(raw_categories)
    categories_list = sorted(set(slugged_categories))

    raw_streaks = raw_values('streak')
    slugged_streaks = slug_em(raw_streaks)
    streaks_list = sorted(set(slugged_streaks))

    random_mineral = get_random_mineral()

    return render(request, 'main_app/index.html',
                  {'minerals': minerals_found,
                   'random_mineral': random_mineral,
                   'categories_list': categories_list,
                   'streaks_list': streaks_list,
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

    raw_categories = raw_values('category')
    slugged_categories = slug_em(raw_categories)
    categories_list = sorted(set(slugged_categories))

    raw_streaks = raw_values('streak')
    slugged_streaks = slug_em(raw_streaks)
    streaks_list = sorted(set(slugged_streaks))

    return render(request,
                  'main_app/mineral_detail.html',
                  {
                      'mineral': mineral,
                      'net_mineral_attributes': net_mineral_attributes,
                      'random_mineral': random_mineral,
                      'categories_list': categories_list,
                      'streaks_list': streaks_list,
                  }
                  )
