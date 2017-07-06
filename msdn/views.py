from django.shortcuts import render, get_object_or_404
from django.db.models import Max

# Create your views here.
from .models import File, ProductGroup, ProductFamily


def index(request):
    latest_files = File.objects.order_by("-posted_date")[:10]
    groups = ProductGroup.objects.order_by("name")

    context = {'latest_files': latest_files, 'groups': groups}
    return render(request, 'msdn/index.html', context)

def about(request):
    return render(request, 'msdn/about.html')


def browse_groups(request):
    groups = ProductGroup.objects.order_by("name")

    context = {'groups': groups}
    return render(request, 'msdn/group_list.html', context)


def group_detail(request, group_id):
    group = get_object_or_404(ProductGroup, pk=group_id)
    families = ProductFamily.objects.filter(group_id=group_id).order_by("name")

    context = {'group': group, 'families': families}
    return render(request, 'msdn/group_detail.html', context)


def family_detail(request, family_id):
    family = get_object_or_404(ProductFamily, pk=family_id)
    files = File.objects.filter(product_family_id= family.id).order_by("-posted_date")

    context = {'family': family, 'files': files}
    return render(request, 'msdn/family_detail.html', context)


def file_detail(request, file_id):
    file_obj = get_object_or_404(File, pk=file_id)

    context = {'file': file_obj}
    return render(request, 'msdn/file_detail.html', context)