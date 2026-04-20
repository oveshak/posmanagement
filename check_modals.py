import os
import django
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'managements.settings')
django.setup()

from user.models import CustomerGroup
from user.views import related_object_modal

def run():
    User = get_user_model()
    try:
        user = User.objects.get(id=1)
    except User.DoesNotExist:
        # Fallback to any user if id=1 doesnt exist for testing, 
        # but the prompt specifically says id=1.
        user = User.objects.first()
        if not user:
            print('No user found'); return

    factory = RequestFactory()
    groups = CustomerGroup.objects.filter(area_id__isnull=False)
    
    total = 0
    mismatch = 0
    
    for cg in groups:
        total += 1
        request = factory.get(f'/related-object-modal/CustomerGroup/{cg.id}/edit/')
        request.user = user
        try:
            response = related_object_modal(request, 'CustomerGroup', str(cg.id), 'edit')
            html = response.content.decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            select = soup.find('select', {'name': 'area'}) or soup.find('select', {'id': 'id_area'})
            
            if not select:
                print(f'MISMATCH cg_id={cg.id} area={cg.area_id} data=NONE selected=NONE')
                mismatch += 1
                continue
                
            data_selected = select.get('data-selected-value')
            option = select.find('option', {'value': str(cg.area_id)})
            is_selected = option.has_attr('selected') if option else False
            
            if str(data_selected) != str(cg.area_id) or not is_selected:
                print(f'MISMATCH cg_id={cg.id} area={cg.area_id} data={data_selected} selected={is_selected}')
                mismatch += 1
        except Exception as e:
            print(f'ERROR cg_id={cg.id}: {str(e)}')
            mismatch += 1
            
    print(f'TOTAL={total} MISMATCH={mismatch}')

if __name__ == '__main__':
    run()
