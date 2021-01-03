import datetime
import string
import json
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Max, Count, Q
from django.contrib import messages

# Create your views here.
from .models import File, Language, ProductGroup, ProductFamily


def index(request):
    latest_files = File.objects.order_by("-posted_date")[:10]
    latest_updated_families = ProductFamily.objects \
        .annotate(last_posted_date=Max('file__posted_date')) \
        .order_by('-last_posted_date')[:10]

    groups = ProductGroup.objects.order_by("name")
    total_count = File.objects.count()

    try:
        msg_file = open(os.path.dirname(__file__) + '/data/messages.json')
        # Input file should be an array of strings
        msgs = json.loads(msg_file.read())
        for msg in msgs:
            messages.add_message(request, messages.INFO, msg, extra_tags='safe')
    except Exception as e:
        # No messages
        pass

    context = {
        'latest_files': latest_files,
        'latest_updated_families': latest_updated_families,
        'groups': groups, 'total_count': total_count,
    }
    return render(request, 'msdn/index.html', context)


def about(request):
    return render(request, 'msdn/about.html')


def browse_groups(request):
    groups = ProductGroup.objects.annotate(Count('productfamily')).order_by("name")
    all_family_count = ProductFamily.objects.count()

    context = {'groups': groups, 'all_family_count': all_family_count}
    return render(request, 'msdn/group_list.html', context)


def family_list(request):
    start_letter = request.GET.get('start_letter')
    if start_letter:
        first_letter = start_letter[0]
    else:
        first_letter = 'a'

    families = ProductFamily.objects \
        .prefetch_related('group') \
        .annotate(Count('file')) \
        .order_by('name')

    if first_letter == '#':
        families = families.exclude(name__regex=r'^[A-Za-z]')
    else:
        families = families.filter(name__istartswith=first_letter)

    all_letters = '#' + string.ascii_lowercase

    context = {'families': families, 'first_letter': first_letter, 'all_letters': all_letters}
    return render(request, 'msdn/family_list.html', context)

def group_detail(request, group_id):
    group = get_object_or_404(ProductGroup, pk=group_id)
    families = ProductFamily.objects.filter(group_id=group_id) \
        .annotate(Count('file'), Max('file__posted_date')) \
        .order_by("name")

    context = {'group': group, 'families': families}
    return render(request, 'msdn/group_detail.html', context)


def family_detail(request, family_id):
    family = get_object_or_404(ProductFamily, pk=family_id)
    files = File.objects.filter(product_family_id= family.id).order_by("-posted_date", "description")
    file_languages = Language.objects.filter(file__product_family_id= family.id).order_by('name').distinct()

    lang = request.GET.get('lang')
    if lang:
        files = files.filter(language__code=lang)

    context = {
        'family': family,
        'files': files,
        'file_languages': file_languages,
        'selected_language': lang,
    }
    return render(request, 'msdn/family_detail.html', context)


def file_detail(request, file_id):
    file_obj = get_object_or_404(File, pk=file_id)

    context = {'file': file_obj}
    return render(request, 'msdn/file_detail.html', context)


def search_result(request):
    query = request.GET.get('q')
    min_query_length = 2
    if not query:
        return render(request, 'msdn/search_result.html')
    elif len(query) < min_query_length:
        return render(request, 'msdn/search_result.html', {
            'query': query,
            'too_short': True,
            'min_length': min_query_length})
    else:
        products_matching = ProductFamily.objects \
            .filter(name__icontains=query) \
            .annotate(Count('file')) \
            .order_by('name')

        files_matching = File.objects.filter(
            Q(sha1_hash__istartswith=query) |
            Q(file_name__icontains=query) |
            Q(description__icontains=query)
        )

    if len(files_matching) == 1:
        return redirect('file_detail', files_matching[0].id)

    too_many_files = files_matching.count() > 100
    too_many_products = products_matching.count() > 20

    context = {'file_results': files_matching[:100],
               'product_results': products_matching[:20],
               'too_many_file_results': too_many_files,
               'too_many_product_results': too_many_products,
               'query': query
               }
    return render(request, 'msdn/search_result.html', context)