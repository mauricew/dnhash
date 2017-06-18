import json, os, time
import requests
from . import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
FAMILY_DATA_DIR = os.path.join(DATA_DIR, 'families')

URL_BASE = "https://msdn.microsoft.com/subscriptions/json"
PAGE_SIZE = 100
DELAY_PER_FAMILY = 0.4


def get_categories():
    r = requests.get(URL_BASE + "/GetProductCategories?brand=MSDN&localeCode=en-us")
    return r.json()


def get_families(category_id):
    r = requests.get(URL_BASE + "/GetProductFamiliesForCategory?brand=MSDN&categoryId=%d" % category_id)
    return r.json()


def get_files(family_id, page_num = 0):
    payload = {
        'Brand': "MSDN",
        'ProductFamilyId': family_id,
        'PageSize': PAGE_SIZE,
        'PageIndex': page_num,
        'Architectures': '',
        'Languages': "en,ar,bg,cn,cs,da,de,el,es,et,fi,fr,he,hk,hr,hu,it,ja,ko,lt,lv,nl,no,pl,pp,pt,ro,ru,sk,sl,sr,sv,th,tr,uk"
    }
    r = requests.post(URL_BASE + "/GetFileSearchResult", payload)
    return r.json()


def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(FAMILY_DATA_DIR):
        os.makedirs(FAMILY_DATA_DIR)

    base_categories = get_categories()
    cf = open(os.path.join(DATA_DIR, 'categories.json'), 'w')
    cf.write(json.dumps(base_categories))
    cf.close()

    families = []
    ff = open(os.path.join(DATA_DIR, 'families.json'), 'w')

    for cat in base_categories:
        if cat['Name'] != ' New Products':
            group_id = cat['ProductGroupId']
            print(cat['Name'] + ": ")

            cur_group_families = get_families(group_id)

            for f in cur_group_families:
                # Fix for the API returning zero for ProductGroupId
                f['ProductGroupId'] = group_id
                fam_id = f['ProductFamilyId']
                #print("Dumping %s" % f['Title'])
                #prf = open(os.path.join(FAMILY_DATA_DIR, '%d.json' % fam_id), 'w')

                # page_num = 0
                # fam_files = []
                #
                # while True:
                #     family_file_search = get_files(fam_id, page_num)
                #     fam_files_curpage = family_file_search['Files']
                #     fam_files = fam_files + fam_files_curpage
                #
                #     if not family_file_search['Files'] or family_file_search['TotalResults'] < PAGE_SIZE:
                #         break
                #     page_num += 1
                #
                # prf.write(json.dumps(fam_files))
                # prf.close()
                # fam_files = []
                # time.sleep(DELAY_PER_FAMILY)

            families += cur_group_families

    ff.write(json.dumps(families))
    ff.close()


main()