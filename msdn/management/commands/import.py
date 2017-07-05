import json, os, sys, re
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "msdnhash.settings")

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from msdn.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        DATA_DIR = os.path.join(BASE_DIR, 'data')
        FAMILY_DATA_DIR = os.path.join(DATA_DIR, 'families')

        categories = []

        with open(os.path.join(DATA_DIR, 'categories.json')) as cat_file:
            j_categories = json.load(cat_file)

            for c in j_categories:
                if c['ProductGroupId'] != 65: # New Products
                    cat_obj = ProductGroup()
                    cat_obj.id = c['ProductGroupId']
                    cat_obj.name = c['Name']
                    categories.append(cat_obj)

        ProductGroup.objects.bulk_create(categories)

        families = []

        with open(os.path.join(DATA_DIR, 'families.json')) as family_file:
            j_families = json.load(family_file)

            for fam in j_families:
                fam_obj = ProductFamily()
                fam_obj.id = fam['ProductFamilyId']
                fam_obj.name = fam['Title']
                fam_obj.group_id = fam['ProductGroupId']
                families.append(fam_obj)

        ProductFamily.objects.bulk_create(families)

        files = []

        # There are 3 files that overlap categories at the moment.
        # Quicker & easier to check them here.
        duped = {14547: False, 37002: False, 36987: False}

        for file_listing_fname in [os.path.join(os.path.abspath(FAMILY_DATA_DIR), f) for f in os.listdir(FAMILY_DATA_DIR)]:
            with open(file_listing_fname) as file_listing_file:
                j_files = json.load(file_listing_file)

                for file in j_files:
                    if file['FileId'] in duped:
                        if not duped[file['FileId']]:
                            duped[file['FileId']] = True
                        else:
                            continue
                    file_obj = File()
                    file_obj.id = file['FileId']
                    file_obj.file_name = file['FileName']
                    file_obj.description = file['Description']
                    file_obj.notes = file['Notes']
                    file_obj.product_family_id = file['ProductFamilyId']
                    file_obj.product_key_required = file['IsProductKeyRequired']
                    file_obj.sha1_hash = file['Sha1Hash']


                    date_str = re.findall(r'\d+', file['PostedDate'])
                    if len(date_str) > 0:
                        file_obj.posted_date = datetime.fromtimestamp(int(date_str[0]) / 1000, timezone.utc)

                    size = file['Size'][:-3]
                    file_obj.size = size
                    files.append(file_obj)

        File.objects.bulk_create(files)