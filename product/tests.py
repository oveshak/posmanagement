from django import forms
from django.template.loader import render_to_string
from django.test import SimpleTestCase


class PurchaseTemplateRenderTests(SimpleTestCase):
    class PurchaseFormStub(forms.Form):
        supplier_name = forms.CharField()
        purchase_date = forms.CharField()
        total_amount = forms.CharField()
        purchase_status = forms.CharField()
        vendor_cheque_details = forms.CharField()

    def test_purchase_form_renders_without_purchase_urls(self):
        html = render_to_string(
            "products/purchase_form.html",
            {"form": self.PurchaseFormStub(), "items": [], "object": None},
        )

        self.assertIn('href="#"', html)
        self.assertIn("Add Item", html)
        self.assertIn("disabled", html)

    def test_purchase_item_modal_renders_without_quick_create_url(self):
        html = render_to_string(
            "products/modals/purchase_item_form.html",
            {"form": self.PurchaseFormStub(), "object": None},
        )

        self.assertIn('<form method="post"', html)
        self.assertNotIn("hx-post=", html)
