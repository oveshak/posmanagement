import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "managements.settings")
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from user.models import CustomerGroup
from user.views import related_object_modal
import re

User = get_user_model()
factory = RequestFactory()
user = User.objects.filter(id=1).first()

def test_cg(cg_id_or_obj):
    if isinstance(cg_id_or_obj, int):
        cg = CustomerGroup.objects.get(id=cg_id_or_obj)
    else:
        cg = cg_id_or_obj
    
    print(f"--- CustomerGroup ID: {cg.id}, Area: {cg.area} ---")
    request = factory.get(f"/related_object_modal/customergroup/{cg.id}/")
    request.user = user
    
    # Based on grep, the signature might be (request, model_name, pk=None)
    response = related_object_modal(request, "customergroup", cg.id)
    html = response.content.decode("utf-8")
    
    select_match = re.search(r"<select[^>]+name=\"area\"[^>]*>.*?</select>", html, re.DOTALL)
    if select_match:
        select_tag = select_match.group(0)
        option_match = re.search(r"<option[^>]+selected[^>]*>.*?</option>", select_tag)
        if not option_match:
             option_match = re.search(r"<option.*?>.*?</option>", select_tag)
             
        print(re.search(r"<select[^>]+name=\"area\"[^>]*>", select_tag).group(0))
        if option_match:
            print(option_match.group(0).strip())
    else:
        print("Area select not found")

try:
    test_cg(32)
except Exception as e:
    print(f"Error testing ID 32: {e}")

cg_with_area = CustomerGroup.objects.exclude(area__isnull=True).first()
if cg_with_area:
    test_cg(cg_with_area)
else:
    print("No CustomerGroup with area found")
