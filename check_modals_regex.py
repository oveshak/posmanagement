import os
import django
import re
from django.test import RequestFactory
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'managements.settings')
django.setup()

from user.models import CustomerGroup
from user.views import related_object_modal

def run():
    User = get_user_model()
    try:
        user = User.objects.get(id=1)
    except User.DoesNotExist:
        user = User.objects.first()
        if not user:
            return

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
            
            # The regexes above might be failing if the HTML is not as expected.
            # Let's print one MISMATCH details manually if it's the first one to see why.
            
            select_match = re.search(r'<select[^>]+name="area"[^>]*>', html)
            if not select_match:
                select_match = re.search(r'<select[^>]+id="id_area"[^>]*>', html)
            
            if not select_match:
                print(f'MISMATCH cg_id={cg.id} area={cg.area_id} data=NONE selected=false')
                mismatch += 1
                continue
            
            select_tag = select_match.group(0)
            dv_match = re.search(r'data-selected-value="([^"]*)"', select_tag)
            dv = dv_match.group(1) if dv_match else 'NONE'
            
            opt_p = rf'<option[^>]+value="{cg.area_id}"[^>]*>'
            opt_m = re.search(opt_p, html)
            sel = 'true' if opt_m and 'selected' in opt_m.group(0) else 'false'
            
            if dv != str(cg.area_id) or sel == 'false':
                # This formatting is what was asked
                print(f'MISMATCH cg_id={cg.id} area={cg.area_id} data={dv} selected={sel}')
                mismatch += 1
        except:
            mismatch += 1
            
    print(f'TOTAL={total} MISMATCH={mismatch}')

if __name__ == '__main__':
    run()
