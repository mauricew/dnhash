import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Max, Count

# Create your views here.
from .models import File, Language, ProductGroup, ProductFamily


def index(request):
    latest_files = File.objects.order_by("-posted_date")[:10]
    latest_updated_families = ProductFamily.objects \
        .annotate(last_posted_date=Max('file__posted_date')) \
        .order_by('-last_posted_date')[:10]

    groups = ProductGroup.objects.order_by("name")
    total_count = File.objects.count()

    fcu_banner_expiration_date = datetime.date(2017, 11, 10)
    show_fcu_banner = datetime.date.today() < fcu_banner_expiration_date

    context = {
        'show_fcu_banner': show_fcu_banner,
        'latest_files': latest_files,
        'latest_updated_families': latest_updated_families,
        'groups': groups, 'total_count': total_count,
    }
    return render(request, 'msdn/index.html', context)


def about(request):
    return render(request, 'msdn/about.html')


def browse_groups(request):
    groups = ProductGroup.objects.annotate(Count('productfamily')).order_by("name")

    context = {'groups': groups}
    return render(request, 'msdn/group_list.html', context)


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


def search_by_hash(request):
    hash_start = request.GET.get('hash_start')
    if not hash_start:
        files_matching = []
    else:
        files_matching = File.objects.filter(sha1_hash__startswith=hash_start)

    if len(files_matching) == 1:
        return redirect('file_detail', files_matching[0].id)

    context = {'search_results': files_matching}
    return render(request, 'msdn/search_result.html', context)