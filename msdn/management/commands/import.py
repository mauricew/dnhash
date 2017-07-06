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

        # English is number one!
        en = Language()
        en.code = 'en'
        en.name = 'English'
        en.save()

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
        imported_file_ids = []

        for file_listing_fname in [os.path.join(os.path.abspath(FAMILY_DATA_DIR), f) for f in os.listdir(FAMILY_DATA_DIR)]:
            with open(file_listing_fname) as file_listing_file:
                j_files = json.load(file_listing_file)

                for file in j_files:
                    if file['FileId'] in imported_file_ids:
                        continue

                    file_obj = File()
                    file_obj.id = file['FileId']
                    file_obj.file_name = file['FileName']
                    file_obj.description = file['Description']
                    file_obj.notes = file['Notes']
                    file_obj.product_family_id = file['ProductFamilyId']
                    file_obj.product_key_required = file['IsProductKeyRequired']
                    file_obj.sha1_hash = file['Sha1Hash']

                    if file['Languages'] and len(file['Languages']) == 1:
                        lang_code = file['LanguageCodes'][0]
                        lang = Language.objects.filter(code=lang_code)
                        if not lang:
                            new_lang = Language()
                            new_lang.code = file['LanguageCodes'][0]
                            new_lang.name = file['Languages'][0]
                            new_lang.save()
                            file_obj.language = new_lang
                        else:
                            file_obj.language = lang[0]

                    date_str = re.findall(r'\d+', file['PostedDate'])
                    if len(date_str) > 0:
                        file_obj.posted_date = datetime.fromtimestamp(int(date_str[0]) / 1000, timezone.utc)

                    size = file['Size'][:-3]
                    file_obj.size = size

                    files.append(file_obj)
                    imported_file_ids.append(file_obj.id)

        File.objects.bulk_create(files)