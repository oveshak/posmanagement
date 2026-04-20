# # # from django import forms
# # # from django.forms import inlineformset_factory



# # # from .models import (
# # #     Product,
# # #     Variation,
# # #     unick,
# # #     PurchaseItem,
# # #     Purchase,
# # #     PurchaseReturn,
# # #     StockTransfer,
# # #     StockTransferLine,
# # #     StockAdjustment,
# # #     VendorCheque,
# # #     RepairRequest,
# # # )


# # # class DateInput(forms.DateInput):
# # #     input_type = "date"


# # # class PurchaseItemForm(forms.ModelForm):
# # #     class Meta:
# # #         model = PurchaseItem
# # #         fields = [
# # #             "purchase_product",
# # #             "purchase_product_variation",
# # #             "unickkey",
# # #             "qty",
# # #             "unit_price",
# # #         ]
# # #         widgets = {
# # #             "purchase_product": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# # #             "purchase_product_variation": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# # #             "unickkey": forms.SelectMultiple(attrs={"class": "form-select js-enhanced-multiselect"}),
# # #             "qty": forms.NumberInput(attrs={"class": "form-input"}),
# # #             "unit_price": forms.NumberInput(attrs={"class": "form-input", "step": "0.01"}),
# # #         }

# # #     def clean(self):
# # #         cleaned = super().clean()
# # #         product = cleaned.get("purchase_product")
# # #         variation = cleaned.get("purchase_product_variation")
# # #         qty = cleaned.get("qty")

# # #         if variation and product and variation.product_name_id != product.id:
# # #             self.add_error("purchase_product_variation", "Variation does not belong to selected product.")

# # #         if qty is not None and qty <= 0:
# # #             self.add_error("qty", "Quantity must be greater than 0.")

# # #         return cleaned


# # # class PurchaseForm(forms.ModelForm):
# # #     class Meta:
# # #         model = Purchase
# # #         fields = [
# # #             "supplier_name",
# # #             "purchase_date",
# # #             "total_amount",
# # #             "purchase_status",
# # #             "vendor_cheque_details",
# # #         ]
# # #         widgets = {
# # #             "supplier_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# # #             "purchase_date": DateInput(attrs={"class": "form-input"}),
# # #             "total_amount": forms.NumberInput(attrs={"class": "form-input", "step": "0.01"}),
# # #             "purchase_status": forms.TextInput(attrs={"class": "form-input"}),
# # #             "vendor_cheque_details": forms.Textarea(attrs={"class": "form-textarea", "rows": 3}),
# # #         }


# # # class PurchaseReturnForm(forms.ModelForm):
# # #     class Meta:
# # #         model = PurchaseReturn
# # #         fields = ["purchase_name", "return_date"]
# # #         widgets = {
# # #             "purchase_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# # #             "return_date": DateInput(attrs={"class": "form-input"}),
# # #         }


# # # class StockTransferForm(forms.ModelForm):
# # #     class Meta:
# # #         model = StockTransfer
# # #         fields = [
# # #             "from_branch_name",
# # #             "to_branch_name",
# # #             "transfer_date",
# # #             "stc_status",
# # #         ]
# # #         widgets = {
# # #             "from_branch_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# # #             "to_branch_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# # #             "transfer_date": DateInput(attrs={"class": "form-input"}),
# # #             "stc_status": forms.TextInput(attrs={"class": "form-input"}),
# # #         }


# # # class StockTransferLineForm(forms.ModelForm):
# # #     class Meta:
# # #         model = StockTransferLine
# # #         fields = [
# # #             "product",
# # #             "variation",
# # #             "quantity",
# # #             "unickkeys",
# # #         ]
# # #         widgets = {
# # #             "product": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# # #             "variation": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# # #             "quantity": forms.NumberInput(attrs={"class": "form-input"}),
# # #             "unickkeys": forms.SelectMultiple(attrs={"class": "form-select js-enhanced-multiselect"}),
# # #         }

# # #     def clean(self):
# # #         cleaned = super().clean()
# # #         product = cleaned.get("product")
# # #         variation = cleaned.get("variation")
# # #         quantity = cleaned.get("quantity")

# # #         if variation and product and variation.product_name_id != product.id:
# # #             self.add_error("variation", "Variation does not belong to selected product.")

# # #         if quantity is not None and quantity <= 0:
# # #             self.add_error("quantity", "Quantity must be greater than 0.")

# # #         return cleaned


# # # StockTransferLineFormSet = inlineformset_factory(
# # #     StockTransfer,
# # #     StockTransferLine,
# # #     form=StockTransferLineForm,
# # #     extra=1,
# # #     can_delete=True,
# # # )


# # # class StockAdjustmentForm(forms.ModelForm):
# # #     class Meta:
# # #         model = StockAdjustment
# # #         fields = [
# # #             "branch_name",
# # #             "product_name",
# # #             "quantity_adjusted",
# # #             "reason",
# # #         ]
# # #         widgets = {
# # #             "branch_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# # #             "product_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# # #             "quantity_adjusted": forms.NumberInput(attrs={"class": "form-input"}),
# # #             "reason": forms.Textarea(attrs={"class": "form-textarea", "rows": 3}),
# # #         }


# # # class VendorChequeForm(forms.ModelForm):
# # #     class Meta:
# # #         model = VendorCheque
# # #         fields = [
# # #             "cheque_number",
# # #             "vendor_name",
# # #             "issue_date",
# # #             "amount",
# # #             "vndcq_status",
# # #         ]
# # #         widgets = {
# # #             "cheque_number": forms.TextInput(attrs={"class": "form-input"}),
# # #             "vendor_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# # #             "issue_date": DateInput(attrs={"class": "form-input"}),
# # #             "amount": forms.NumberInput(attrs={"class": "form-input", "step": "0.01"}),
# # #             "vndcq_status": forms.TextInput(attrs={"class": "form-input"}),
# # #         }


# # # class RepairRequestForm(forms.ModelForm):
# # #     class Meta:
# # #         model = RepairRequest
# # #         fields = [
# # #             "product_name",
# # #             "customer_name",
# # #             "branch_name",
# # #             "requested_by_user_name",
# # #             "request_date",
# # #             "repair_status",
# # #             "notes",
# # #         ]
# # #         widgets = {
# # #             "product_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# # #             "customer_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# # #             "branch_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# # #             "requested_by_user_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# # #             "request_date": DateInput(attrs={"class": "form-input"}),
# # #             "repair_status": forms.TextInput(attrs={"class": "form-input"}),
# # #             "notes": forms.Textarea(attrs={"class": "form-textarea", "rows": 3}),
# # #         }

# # from django import forms
# # from django.forms import inlineformset_factory

# # from user.models import Branch, Users
# # from .models import (
# #     Unit, Category, Brand, Warranty,
# #     Product, Variation, unick, Supplier,
# #     PurchaseItem, Purchase, PurchaseReturn,
# #     StockTransfer, StockTransferLine,
# #     StockAdjustment, VendorCheque, RepairRequest,
# # )


# # class DateInput(forms.DateInput):
# #     input_type = "date"


# # class SupplierForm(forms.ModelForm):
# #     class Meta:
# #         model = Supplier
# #         fields = ["name", "contact_number", "email", "address"]
# #         widgets = {
# #             "name": forms.TextInput(attrs={"class": "form-input"}),
# #             "contact_number": forms.TextInput(attrs={"class": "form-input"}),
# #             "email": forms.EmailInput(attrs={"class": "form-input"}),
# #             "address": forms.Textarea(attrs={"class": "form-textarea", "rows": 3}),
# #         }


# # class ProductForm(forms.ModelForm):
# #     class Meta:
# #         model = Product
# #         fields = ["name", "sku", "unit_name", "category_name", "brand_name", "warranty_name"]
# #         widgets = {
# #             "name": forms.TextInput(attrs={"class": "form-input"}),
# #             "sku": forms.TextInput(attrs={"class": "form-input"}),
# #             "unit_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "category_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "brand_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "warranty_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #         }


# # class VariationForm(forms.ModelForm):
# #     class Meta:
# #         model = Variation
# #         fields = ["product_name", "name", "sku_suffix", "price", "quantity", "dealer_price", "isunck", "unickkey"]
# #         widgets = {
# #             "product_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "name": forms.TextInput(attrs={"class": "form-input"}),
# #             "sku_suffix": forms.TextInput(attrs={"class": "form-input"}),
# #             "price": forms.NumberInput(attrs={"class": "form-input", "step": "0.01"}),
# #             "quantity": forms.NumberInput(attrs={"class": "form-input"}),
# #             "dealer_price": forms.NumberInput(attrs={"class": "form-input", "step": "0.01"}),
# #             "unickkey": forms.SelectMultiple(attrs={"class": "form-select js-enhanced-multiselect"}),
# #         }


# # class UnickForm(forms.ModelForm):
# #     class Meta:
# #         model = unick
# #         fields = ["key1", "key2"]
# #         widgets = {
# #             "key1": forms.TextInput(attrs={"class": "form-input"}),
# #             "key2": forms.TextInput(attrs={"class": "form-input"}),
# #         }


# # class PurchaseItemForm(forms.ModelForm):
# #     class Meta:
# #         model = PurchaseItem
# #         fields = [
# #             "purchase_product",
# #             "purchase_product_variation",
# #             "unickkey",
# #             "qty",
# #             "unit_price",
# #         ]
# #         widgets = {
# #             "purchase_product": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "purchase_product_variation": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "unickkey": forms.SelectMultiple(attrs={"class": "form-select js-enhanced-multiselect"}),
# #             "qty": forms.NumberInput(attrs={"class": "form-input"}),
# #             "unit_price": forms.NumberInput(attrs={"class": "form-input", "step": "0.01"}),
# #         }

# #     def clean(self):
# #         cleaned = super().clean()
# #         product = cleaned.get("purchase_product")
# #         variation = cleaned.get("purchase_product_variation")
# #         qty = cleaned.get("qty")

# #         if variation and product and variation.product_name_id != product.id:
# #             self.add_error("purchase_product_variation", "Variation does not belong to selected product.")

# #         if qty is not None and qty <= 0:
# #             self.add_error("qty", "Quantity must be greater than 0.")

# #         return cleaned


# # class PurchaseForm(forms.ModelForm):
# #     class Meta:
# #         model = Purchase
# #         fields = [
# #             "supplier_name",
# #             "purchase_date",
# #             "total_amount",
# #             "purchase_status",
# #             "vendor_cheque_details",
# #         ]
# #         widgets = {
# #             "supplier_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "purchase_date": DateInput(attrs={"class": "form-input"}),
# #             "total_amount": forms.NumberInput(attrs={"class": "form-input", "step": "0.01"}),
# #             "purchase_status": forms.TextInput(attrs={"class": "form-input"}),
# #             "vendor_cheque_details": forms.Textarea(attrs={"class": "form-textarea", "rows": 3}),
# #         }


# # class PurchaseReturnForm(forms.ModelForm):
# #     class Meta:
# #         model = PurchaseReturn
# #         fields = ["purchase_name", "return_date"]
# #         widgets = {
# #             "purchase_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "return_date": DateInput(attrs={"class": "form-input"}),
# #         }


# # class StockTransferForm(forms.ModelForm):
# #     class Meta:
# #         model = StockTransfer
# #         fields = [
# #             "from_branch_name",
# #             "to_branch_name",
# #             "transfer_date",
# #             "stc_status",
# #         ]
# #         widgets = {
# #             "from_branch_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "to_branch_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "transfer_date": DateInput(attrs={"class": "form-input"}),
# #             "stc_status": forms.TextInput(attrs={"class": "form-input"}),
# #         }


# # class StockTransferLineForm(forms.ModelForm):
# #     class Meta:
# #         model = StockTransferLine
# #         fields = [
# #             "product",
# #             "variation",
# #             "quantity",
# #             "unickkeys",
# #         ]
# #         widgets = {
# #             "product": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "variation": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "quantity": forms.NumberInput(attrs={"class": "form-input"}),
# #             "unickkeys": forms.SelectMultiple(attrs={"class": "form-select js-enhanced-multiselect"}),
# #         }

# #     def clean(self):
# #         cleaned = super().clean()
# #         product = cleaned.get("product")
# #         variation = cleaned.get("variation")
# #         quantity = cleaned.get("quantity")

# #         if variation and product and variation.product_name_id != product.id:
# #             self.add_error("variation", "Variation does not belong to selected product.")

# #         if quantity is not None and quantity <= 0:
# #             self.add_error("quantity", "Quantity must be greater than 0.")

# #         return cleaned


# # StockTransferLineFormSet = inlineformset_factory(
# #     StockTransfer,
# #     StockTransferLine,
# #     form=StockTransferLineForm,
# #     extra=1,
# #     can_delete=True,
# # )


# # class StockAdjustmentForm(forms.ModelForm):
# #     class Meta:
# #         model = StockAdjustment
# #         fields = [
# #             "branch_name",
# #             "product_name",
# #             "quantity_adjusted",
# #             "reason",
# #         ]
# #         widgets = {
# #             "branch_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "product_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "quantity_adjusted": forms.NumberInput(attrs={"class": "form-input"}),
# #             "reason": forms.Textarea(attrs={"class": "form-textarea", "rows": 3}),
# #         }


# # class VendorChequeForm(forms.ModelForm):
# #     class Meta:
# #         model = VendorCheque
# #         fields = [
# #             "cheque_number",
# #             "vendor_name",
# #             "issue_date",
# #             "amount",
# #             "vndcq_status",
# #         ]
# #         widgets = {
# #             "cheque_number": forms.TextInput(attrs={"class": "form-input"}),
# #             "vendor_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "issue_date": DateInput(attrs={"class": "form-input"}),
# #             "amount": forms.NumberInput(attrs={"class": "form-input", "step": "0.01"}),
# #             "vndcq_status": forms.TextInput(attrs={"class": "form-input"}),
# #         }


# # class RepairRequestForm(forms.ModelForm):
# #     class Meta:
# #         model = RepairRequest
# #         fields = [
# #             "product_name",
# #             "customer_name",
# #             "branch_name",
# #             "requested_by_user_name",
# #             "request_date",
# #             "repair_status",
# #             "notes",
# #         ]
# #         widgets = {
# #             "product_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "customer_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "branch_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "requested_by_user_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
# #             "request_date": DateInput(attrs={"class": "form-input"}),
# #             "repair_status": forms.TextInput(attrs={"class": "form-input"}),
# #             "notes": forms.Textarea(attrs={"class": "form-textarea", "rows": 3}),
# #         }


# from django import forms
# from django.forms import inlineformset_factory

# from .models import (
#     Unit,
#     Category,
#     Brand,
#     Warranty,
#     Product,
#     Variation,
#     unick,
# )


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = [
#             "name",
#             "sku",
#             "unit_name",
#             "category_name",
#             "brand_name",
#             "warranty_name",
#         ]
#         widgets = {
#             "name": forms.TextInput(attrs={"class": "form-input"}),
#             "sku": forms.TextInput(attrs={"class": "form-input"}),
#             "unit_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
#             "category_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
#             "brand_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
#             "warranty_name": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
#         }


# class VariationForm(forms.ModelForm):
#     class Meta:
#         model = Variation
#         fields = [
#             "name",
#             "sku_suffix",
#             "price",
#             "quantity",
#             "dealer_price",
#             "isunck",
#             "unickkey",
#         ]
#         widgets = {
#             "name": forms.TextInput(attrs={"class": "form-input"}),
#             "sku_suffix": forms.TextInput(attrs={"class": "form-input"}),
#             "price": forms.NumberInput(attrs={"class": "form-input", "step": "0.01"}),
#             "quantity": forms.NumberInput(attrs={"class": "form-input"}),
#             "dealer_price": forms.NumberInput(attrs={"class": "form-input", "step": "0.01"}),
#             "isunck": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
#             "unickkey": forms.SelectMultiple(attrs={"class": "form-select js-enhanced-multiselect"}),
#         }

#     def clean(self):
#         cleaned = super().clean()
#         isunck = cleaned.get("isunck")
#         unickkeys = cleaned.get("unickkey")

#         if isunck and not unickkeys:
#             self.add_error("unickkey", "Unique key required when 'Has Unique Key' is checked.")

#         return cleaned


# VariationFormSet = inlineformset_factory(
#     Product,
#     Variation,
#     form=VariationForm,
#     extra=1,
#     can_delete=True,
# )


# class UnitForm(forms.ModelForm):
#     class Meta:
#         model = Unit
#         fields = ["name"]
#         widgets = {
#             "name": forms.TextInput(attrs={"class": "form-input"}),
#         }


# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ["name"]
#         widgets = {
#             "name": forms.TextInput(attrs={"class": "form-input"}),
#         }


# class BrandForm(forms.ModelForm):
#     class Meta:
#         model = Brand
#         fields = ["name"]
#         widgets = {
#             "name": forms.TextInput(attrs={"class": "form-input"}),
#         }


# class WarrantyForm(forms.ModelForm):
#     class Meta:
#         model = Warranty
#         fields = ["name", "duration", "duration_type"]
#         widgets = {
#             "name": forms.TextInput(attrs={"class": "form-input"}),
#             "duration": forms.NumberInput(attrs={"class": "form-input"}),
#             "duration_type": forms.Select(attrs={"class": "form-select js-enhanced-select"}),
#         }


# class UnickForm(forms.ModelForm):
#     class Meta:
#         model = unick
#         fields = ["key1", "key2"]
#         widgets = {
#             "key1": forms.TextInput(attrs={"class": "form-input"}),
#             "key2": forms.TextInput(attrs={"class": "form-input"}),
#         }





















from decimal import Decimal

from django import forms
from django.forms import inlineformset_factory
from django.db.models import Q
from ckeditor.widgets import CKEditorWidget

from user.models import Branch
from user.scope import get_user_scope
from .models import (
    Unit,
    Category,
    SubCategory,
    VatRate,
    VariationAttribute,
    VariationAttributeValue,
    Brand,
    Warranty,
    Product,
    Variation,
    unick,
    BranchProductStock,
)


class DateInput(forms.DateInput):
    input_type = "date"


COMMON_INPUT = "w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-900 dark:text-white"
COMMON_SELECT = "w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-900 dark:text-white js-enhanced-select"
COMMON_MULTI = "w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-900 dark:text-white js-enhanced-multiselect"
COMMON_TEXTAREA = "w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-900 dark:text-white"


class ProductStyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_selected_state()

    def _get_selected_ids_for_field(self, name, field):
        if isinstance(field, forms.ModelMultipleChoiceField):
            if self.is_bound:
                raw_values = self.data.getlist(name)
                return [str(v).strip() for v in raw_values if str(v).strip()]

            initial_value = self.initial.get(name, None)
            if initial_value is not None:
                if hasattr(initial_value, "values_list"):
                    return [str(v) for v in initial_value.values_list("pk", flat=True)]
                if isinstance(initial_value, (str, int)):
                    selected = str(initial_value).strip()
                    return [selected] if selected else []
                return [str(getattr(v, "pk", v)).strip() for v in initial_value if str(getattr(v, "pk", v)).strip()]

            if getattr(self, "instance", None) and getattr(self.instance, "pk", None):
                manager = getattr(self.instance, name, None)
                if manager is not None and hasattr(manager, "values_list"):
                    return [str(v) for v in manager.values_list("pk", flat=True)]

            return []

        if isinstance(field, forms.ModelChoiceField):
            if self.is_bound:
                raw_value = self.data.get(name, "")
                selected = str(raw_value).strip()
                return [selected] if selected else []

            initial_value = self.initial.get(name, None)
            if hasattr(initial_value, "pk"):
                return [str(initial_value.pk)]
            if initial_value not in (None, ""):
                selected = str(initial_value).strip()
                return [selected] if selected else []

            if getattr(self, "instance", None):
                selected = str(getattr(self.instance, f"{name}_id", "") or "").strip()
                return [selected] if selected else []

        return []

    def _merge_queryset_with_ids(self, queryset, selected_ids):
        target_model = getattr(queryset, "model", None)
        if queryset is None or target_model is None:
            return queryset

        if selected_ids is None:
            return queryset

        if not isinstance(selected_ids, (list, tuple, set)):
            selected_ids = [selected_ids]

        clean_ids = [str(pk).strip() for pk in selected_ids if str(pk).strip()]
        if not clean_ids:
            return queryset

        return target_model.objects.filter(
            Q(pk__in=queryset.values_list("pk", flat=True)) | Q(pk__in=clean_ids)
        ).distinct()

    def apply_selected_state(self):
        for name, field in self.fields.items():
            if not isinstance(field, (forms.ModelChoiceField, forms.ModelMultipleChoiceField)):
                continue

            queryset = getattr(field, "queryset", None)
            if queryset is not None:
                selected_ids = self._get_selected_ids_for_field(name, field)
                if selected_ids:
                    field.queryset = self._merge_queryset_with_ids(queryset, selected_ids)

            selected_ids = self._get_selected_ids_for_field(name, field)
            if isinstance(field, forms.ModelMultipleChoiceField):
                field.widget.attrs["data-selected-value"] = ",".join(selected_ids)
            else:
                field.widget.attrs["data-selected-value"] = selected_ids[0] if selected_ids else ""


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = [
#             "name",
#             "sku",
#             "unit_name",
#             "category_name",
#             "brand_name",
#             "warranty_name",
#         ]
#         widgets = {
#             "name": forms.TextInput(attrs={"class": COMMON_INPUT}),
#             "sku": forms.TextInput(attrs={"class": COMMON_INPUT}),
#             "unit_name": forms.Select(attrs={"class": COMMON_SELECT}),
#             "category_name": forms.Select(attrs={"class": COMMON_SELECT}),
#             "brand_name": forms.Select(attrs={"class": COMMON_SELECT}),
#             "warranty_name": forms.Select(attrs={"class": COMMON_SELECT}),
#         }

class ProductForm(ProductStyledModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "sku",
            "barcode_type",
            "unit_name",
            "category_name",
            "subcategory_name",
            "brand_name",
            "warranty_name",
            "business_location",
            "manage_stock",
            "low_stock_alert_quantity",
            "product_description",
            "product_image",
            "product_brochure",
            "enable_imei_or_serial",
            "not_for_selling",
            "weight",
            "service_time_minutes",
            "disable_woocommerce_sync",
            "vat_rate",
            "applicable_tax_percent",
            "selling_price_tax_type",
            "product_type",
            "default_purchase_price_exc_tax",
            "default_purchase_price_inc_tax",
            "margin_percent",
            "default_selling_price",
            "single_stock_quantity",
            "single_imei_numbers",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "sku": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "barcode_type": forms.Select(attrs={"class": COMMON_SELECT}),
            "unit_name": forms.Select(attrs={"class": COMMON_SELECT}),
            "category_name": forms.Select(attrs={"class": COMMON_SELECT}),
            "subcategory_name": forms.Select(attrs={"class": COMMON_SELECT}),
            "brand_name": forms.Select(attrs={"class": COMMON_SELECT}),
            "warranty_name": forms.Select(attrs={"class": COMMON_SELECT}),
            "business_location": forms.Select(attrs={"class": COMMON_SELECT}),
            "manage_stock": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"}),
            "low_stock_alert_quantity": forms.NumberInput(attrs={"class": COMMON_INPUT, "min": "1"}),
            "product_description": CKEditorWidget(attrs={"class": COMMON_TEXTAREA}),
            "product_image": forms.ClearableFileInput(attrs={"class": COMMON_INPUT}),
            "product_brochure": forms.ClearableFileInput(attrs={"class": COMMON_INPUT}),
            "enable_imei_or_serial": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"}),
            "not_for_selling": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"}),
            "weight": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.001", "min": "0"}),
            "service_time_minutes": forms.NumberInput(attrs={"class": COMMON_INPUT, "min": "0"}),
            "disable_woocommerce_sync": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"}),
            "vat_rate": forms.Select(attrs={"class": COMMON_SELECT}),
            "applicable_tax_percent": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01", "min": "0"}),
            "selling_price_tax_type": forms.Select(attrs={"class": COMMON_SELECT}),
            "product_type": forms.Select(attrs={"class": COMMON_SELECT}),
            "default_purchase_price_exc_tax": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01", "min": "0"}),
            "default_purchase_price_inc_tax": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01", "min": "0", "readonly": "readonly"}),
            "margin_percent": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01"}),
            "default_selling_price": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01", "min": "0", "readonly": "readonly"}),
            "single_stock_quantity": forms.NumberInput(attrs={"class": COMMON_INPUT, "min": "0"}),
            "single_imei_numbers": forms.Textarea(attrs={"class": f"{COMMON_TEXTAREA} hidden js-single-imei-storage", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        if request and request.user.is_authenticated:
            scope = get_user_scope(request.user)
            self.fields["business_location"].queryset = scope["branches"]
        else:
            self.fields["business_location"].queryset = Branch.objects.order_by("name")

        self.fields["vat_rate"].queryset = VatRate.objects.order_by("name")

        if self.is_bound:
            selected_category_id = str(self.data.get("category_name", "") or "").strip()
            selected_subcategory_id = str(self.data.get("subcategory_name", "") or "").strip()
        else:
            selected_category_id = str(getattr(self.instance, "category_name_id", "") or "").strip()
            selected_subcategory_id = str(getattr(self.instance, "subcategory_name_id", "") or "").strip()

        subcategory_qs = SubCategory.objects.select_related("category").order_by("category__name", "name")
        if selected_category_id:
            subcategory_qs = subcategory_qs.filter(category_id=selected_category_id)
        if selected_subcategory_id:
            subcategory_qs = self._merge_queryset_with_ids(subcategory_qs, [selected_subcategory_id])
        self.fields["subcategory_name"].queryset = subcategory_qs

        related_map = {
            "unit_name": "unit",
            "category_name": "category",
            "subcategory_name": "subcategory",
            "brand_name": "brand",
            "warranty_name": "warranty",
            "business_location": "branch",
            "vat_rate": "vat_rate",
        }

        for field_name, model_name in related_map.items():
            field = self.fields[field_name]
            field.widget.attrs["data_related_model"] = model_name
            field.widget.attrs["data_parent_field"] = field_name
            field.widget.attrs["can_add_related"] = True
            field.widget.attrs["can_change_related"] = True
            field.widget.attrs.setdefault("data-force-search", "1")
            field.widget.attrs.setdefault("data-hide-value-prefix", "1")

            if self.is_bound:
                value = self.data.get(field_name, "")
            else:
                value = self.initial.get(field_name) or getattr(self.instance, f"{field_name}_id", "")
            field.widget.attrs["data-selected-value"] = str(value or "")

        self.fields["subcategory_name"].widget.attrs["data-placeholder"] = "Search subcategory"
        self.fields["subcategory_name"].widget.attrs["data-parent-category-field"] = "category_name"
        self.apply_selected_state()

    def clean(self):
        cleaned = super().clean()
        manage_stock = cleaned.get("manage_stock")
        low_stock_alert_quantity = cleaned.get("low_stock_alert_quantity")

        if manage_stock and not low_stock_alert_quantity:
            self.add_error("low_stock_alert_quantity", "Low stock alert quantity is required when manage stock is enabled.")

        return cleaned


class VariationForm(ProductStyledModelForm):
    class Meta:
        model = Variation
        fields = [
            "name",
            "sku_suffix",
            "variation_image",
            "price",
            "selling_price_inc_tax",
            "purchase_price_exc_tax",
            "purchase_price_inc_tax",
            "vat_rate",
            "applicable_tax_percent",
            "selling_price_tax_type",
            "margin_percent",
            "quantity",
            "dealer_price",
            "isunck",
            "attribute_values",
            "imei_numbers",
            "unickkey",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "sku_suffix": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "variation_image": forms.ClearableFileInput(attrs={"class": COMMON_INPUT}),
            "price": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01"}),
            "selling_price_inc_tax": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01", "readonly": "readonly"}),
            "purchase_price_exc_tax": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01"}),
            "purchase_price_inc_tax": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01", "readonly": "readonly"}),
            "vat_rate": forms.Select(attrs={"class": COMMON_SELECT}),
            "applicable_tax_percent": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01", "min": "0"}),
            "selling_price_tax_type": forms.Select(attrs={"class": COMMON_SELECT}),
            "margin_percent": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01"}),
            "quantity": forms.NumberInput(attrs={"class": COMMON_INPUT}),
            "dealer_price": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01"}),
            "isunck": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"}),
            "attribute_values": forms.SelectMultiple(attrs={"class": f"{COMMON_MULTI} hidden variation-attribute-values", "data-no-enhance": "1"}),
            "imei_numbers": forms.Textarea(attrs={"class": f"{COMMON_TEXTAREA} hidden variation-imei-storage", "rows": 2}),
            "unickkey": forms.SelectMultiple(attrs={"class": COMMON_MULTI, "data-force-search": "1", "data-hide-value-prefix": "1", "data-placeholder": "Search unique keys"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in (
            "price",
            "dealer_price",
            "quantity",
            "applicable_tax_percent",
            "margin_percent",
            "selling_price_tax_type",
        ):
            if field_name in self.fields:
                self.fields[field_name].required = False

        if not self.is_bound and not getattr(self.instance, "pk", None):
            default_initials = {
                "price": "0.00",
                "dealer_price": "0.00",
                "quantity": "0",
            }
            for field_name, default_value in default_initials.items():
                if field_name in self.fields:
                    self.initial.setdefault(field_name, default_value)

        self.fields["vat_rate"].queryset = VatRate.objects.order_by("name")
        self.fields["vat_rate"].widget.attrs["data_related_model"] = "vat_rate"
        self.fields["vat_rate"].widget.attrs["data_parent_field"] = "vat_rate"
        self.fields["vat_rate"].widget.attrs["can_add_related"] = True
        self.fields["vat_rate"].widget.attrs["can_change_related"] = True

        if self.is_bound:
            selected_vat = str(self.data.get("vat_rate", "") or "")
        else:
            selected_vat = str(getattr(self.instance, "vat_rate_id", "") or "")

        self.fields["vat_rate"].widget.attrs["data-selected-value"] = selected_vat
        self.apply_selected_state()

    def clean(self):
        cleaned = super().clean()

        if cleaned.get("price") in (None, ""):
            cleaned["price"] = Decimal("0.00")
        if cleaned.get("dealer_price") in (None, ""):
            cleaned["dealer_price"] = Decimal("0.00")
        if cleaned.get("quantity") in (None, ""):
            cleaned["quantity"] = 0
        if cleaned.get("applicable_tax_percent") in (None, ""):
            cleaned["applicable_tax_percent"] = Decimal("0.00")
        if cleaned.get("margin_percent") in (None, ""):
            cleaned["margin_percent"] = Decimal("25.00")
        if cleaned.get("selling_price_tax_type") in (None, ""):
            cleaned["selling_price_tax_type"] = "exclusive"

        isunck = cleaned.get("isunck")
        unickkeys = cleaned.get("unickkey")
        quantity = cleaned.get("quantity") or 0
        imei_numbers = cleaned.get("imei_numbers") or ""
        imei_lines = [line.strip() for line in str(imei_numbers).splitlines() if line.strip()]

        if isunck and not cleaned.get("DELETE", False):
            unick_count = len(unickkeys) if unickkeys else 0
            if unick_count != quantity:
                self.add_error("unickkey", "Unique key count must match variation quantity.")

            if quantity and imei_lines and len(imei_lines) != quantity:
                self.add_error("imei_numbers", "IMEI count must match variation quantity.")

            if len(set(imei_lines)) != len(imei_lines):
                self.add_error("imei_numbers", "Duplicate IMEI numbers are not allowed.")

        return cleaned


VariationFormSet = inlineformset_factory(
    Product,
    Variation,
    form=VariationForm,
    extra=0,
    can_delete=True,
)


class VariationAttributeForm(ProductStyledModelForm):
    class Meta:
        model = VariationAttribute
        fields = ["name", "order"]
        widgets = {
            "name": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "order": forms.NumberInput(attrs={"class": COMMON_INPUT, "min": "0"}),
        }


class VariationAttributeValueForm(ProductStyledModelForm):
    class Meta:
        model = VariationAttributeValue
        fields = ["attribute", "value", "value_code", "order"]
        widgets = {
            "attribute": forms.Select(attrs={"class": COMMON_SELECT}),
            "value": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "value_code": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "order": forms.NumberInput(attrs={"class": COMMON_INPUT, "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["attribute"].queryset = VariationAttribute.objects.order_by("order", "name")
        self.fields["attribute"].widget.attrs["data_related_model"] = "variation_attribute"
        self.fields["attribute"].widget.attrs["data_parent_field"] = "attribute"
        self.fields["attribute"].widget.attrs["can_add_related"] = True
        self.fields["attribute"].widget.attrs["can_change_related"] = True

        if self.is_bound:
            selected_attribute = str(self.data.get("attribute", "") or "")
        else:
            selected_attribute = str(getattr(self.instance, "attribute_id", "") or "")

        self.fields["attribute"].widget.attrs["data-selected-value"] = selected_attribute


class VatRateForm(ProductStyledModelForm):
    class Meta:
        model = VatRate
        fields = ["name", "rate_percent", "tax_type"]
        widgets = {
            "name": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "rate_percent": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01", "min": "0"}),
            "tax_type": forms.Select(attrs={"class": COMMON_SELECT}),
        }


class UnitForm(ProductStyledModelForm):
    class Meta:
        model = Unit
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": COMMON_INPUT})}


class CategoryForm(ProductStyledModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": COMMON_INPUT})}


class SubCategoryForm(ProductStyledModelForm):
    class Meta:
        model = SubCategory
        fields = ["category", "name"]
        widgets = {
            "category": forms.Select(attrs={"class": COMMON_SELECT}),
            "name": forms.TextInput(attrs={"class": COMMON_INPUT}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = Category.objects.order_by("name")
        self.fields["category"].widget.attrs["data_related_model"] = "category"
        self.fields["category"].widget.attrs["data_parent_field"] = "category"
        self.fields["category"].widget.attrs["can_add_related"] = True
        self.fields["category"].widget.attrs["can_change_related"] = True

        if self.is_bound:
            selected_category = str(self.data.get("category", "") or "")
        else:
            selected_category = str(getattr(self.instance, "category_id", "") or "")

        self.fields["category"].widget.attrs["data-selected-value"] = selected_category


class BrandForm(ProductStyledModelForm):
    class Meta:
        model = Brand
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": COMMON_INPUT})}


class WarrantyForm(ProductStyledModelForm):
    class Meta:
        model = Warranty
        fields = ["name", "duration", "duration_type"]
        widgets = {
            "name": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "duration": forms.NumberInput(attrs={"class": COMMON_INPUT}),
            "duration_type": forms.Select(attrs={"class": COMMON_SELECT}),
        }


class UnickForm(ProductStyledModelForm):
    class Meta:
        model = unick
        fields = ["key1", "key2"]
        widgets = {
            "key1": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "key2": forms.TextInput(attrs={"class": COMMON_INPUT}),
        }


# class BranchProductStockForm(forms.ModelForm):
#     class Meta:
#         model = BranchProductStock
#         fields = [
#             "stock_branch",
#             "product_name",
#             "product_variation",
#             "quantity",
#             "unickkey",
#         ]
#         widgets = {
#             "stock_branch": forms.Select(attrs={"class": COMMON_SELECT}),
#             "product_name": forms.Select(attrs={"class": COMMON_SELECT}),
#             "product_variation": forms.Select(attrs={"class": COMMON_SELECT}),
#             "quantity": forms.NumberInput(attrs={"class": COMMON_INPUT}),
#             "unickkey": forms.SelectMultiple(attrs={"class": COMMON_MULTI}),
#         }
        

#     def clean(self):
#         cleaned = super().clean()
#         product = cleaned.get("product_name")
#         variation = cleaned.get("product_variation")

#         if variation and product and variation.product_name_id != product.id:
#             self.add_error("product_variation", "Variation does not belong to selected product.")
#         return cleaned



class VariationQuickForm(ProductStyledModelForm):
    class Meta:
        model = Variation
        fields = [
            "product_name",
            "name",
            "sku_suffix",
            "variation_image",
            "price",
            "selling_price_inc_tax",
            "purchase_price_exc_tax",
            "purchase_price_inc_tax",
            "vat_rate",
            "applicable_tax_percent",
            "selling_price_tax_type",
            "margin_percent",
            "quantity",
            "dealer_price",
            "isunck",
            "attribute_values",
            "imei_numbers",
            "unickkey",
        ]
        widgets = {
            "product_name": forms.Select(attrs={"class": COMMON_SELECT}),
            "name": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "sku_suffix": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "variation_image": forms.ClearableFileInput(attrs={"class": COMMON_INPUT}),
            "price": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01"}),
            "selling_price_inc_tax": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01", "readonly": "readonly"}),
            "purchase_price_exc_tax": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01"}),
            "purchase_price_inc_tax": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01", "readonly": "readonly"}),
            "vat_rate": forms.Select(attrs={"class": COMMON_SELECT}),
            "applicable_tax_percent": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01", "min": "0"}),
            "selling_price_tax_type": forms.Select(attrs={"class": COMMON_SELECT}),
            "margin_percent": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01"}),
            "quantity": forms.NumberInput(attrs={"class": COMMON_INPUT}),
            "dealer_price": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01"}),
            "isunck": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"}),
            "attribute_values": forms.SelectMultiple(attrs={"class": f"{COMMON_MULTI} hidden variation-attribute-values", "data-no-enhance": "1"}),
            "imei_numbers": forms.Textarea(attrs={"class": f"{COMMON_TEXTAREA} hidden variation-imei-storage", "rows": 2}),
            "unickkey": forms.SelectMultiple(attrs={"class": COMMON_MULTI, "data-force-search": "1", "data-hide-value-prefix": "1", "data-placeholder": "Search unique keys"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in (
            "price",
            "dealer_price",
            "quantity",
            "applicable_tax_percent",
            "margin_percent",
            "selling_price_tax_type",
        ):
            if field_name in self.fields:
                self.fields[field_name].required = False

        if not self.is_bound and not getattr(self.instance, "pk", None):
            default_initials = {
                "price": "0.00",
                "dealer_price": "0.00",
                "quantity": "0",
            }
            for field_name, default_value in default_initials.items():
                if field_name in self.fields:
                    self.initial.setdefault(field_name, default_value)

        self.fields["vat_rate"].queryset = VatRate.objects.order_by("name")
        self.fields["vat_rate"].widget.attrs["data_related_model"] = "vat_rate"
        self.fields["vat_rate"].widget.attrs["data_parent_field"] = "vat_rate"
        self.fields["vat_rate"].widget.attrs["can_add_related"] = True
        self.fields["vat_rate"].widget.attrs["can_change_related"] = True

        if self.is_bound:
            selected_vat = str(self.data.get("vat_rate", "") or "")
        else:
            selected_vat = str(getattr(self.instance, "vat_rate_id", "") or "")

        self.fields["vat_rate"].widget.attrs["data-selected-value"] = selected_vat

        self.fields["product_name"].widget.attrs["data_related_model"] = "product"
        self.fields["product_name"].widget.attrs["data_parent_field"] = "product_name"
        self.fields["product_name"].widget.attrs["can_add_related"] = True
        self.fields["product_name"].widget.attrs["can_change_related"] = True

        if self.is_bound:
            selected_product = self.data.get("product_name", "")
            selected_unicks = self.data.getlist("unickkey")
        else:
            selected_product = getattr(self.instance, "product_name_id", "") if self.instance.pk else ""
            selected_unicks = [str(v) for v in self.instance.unickkey.values_list("pk", flat=True)] if self.instance.pk else []

        self.fields["product_name"].widget.attrs["data-selected-value"] = str(selected_product or "")
        self.fields["unickkey"].widget.attrs["data_related_model"] = "unick"
        self.fields["unickkey"].widget.attrs["data_parent_field"] = "unickkey"
        self.fields["unickkey"].widget.attrs["can_add_related"] = True
        self.fields["unickkey"].widget.attrs["can_change_related"] = True
        self.fields["unickkey"].widget.attrs["data-selected-value"] = ",".join(selected_unicks)
        self.apply_selected_state()

    def clean(self):
        cleaned = super().clean()

        if cleaned.get("price") in (None, ""):
            cleaned["price"] = Decimal("0.00")
        if cleaned.get("dealer_price") in (None, ""):
            cleaned["dealer_price"] = Decimal("0.00")
        if cleaned.get("quantity") in (None, ""):
            cleaned["quantity"] = 0
        if cleaned.get("applicable_tax_percent") in (None, ""):
            cleaned["applicable_tax_percent"] = Decimal("0.00")
        if cleaned.get("margin_percent") in (None, ""):
            cleaned["margin_percent"] = Decimal("25.00")
        if cleaned.get("selling_price_tax_type") in (None, ""):
            cleaned["selling_price_tax_type"] = "exclusive"

        isunck = cleaned.get("isunck")
        unickkeys = cleaned.get("unickkey")
        quantity = cleaned.get("quantity") or 0
        imei_numbers = cleaned.get("imei_numbers") or ""
        imei_lines = [line.strip() for line in str(imei_numbers).splitlines() if line.strip()]

        if isunck:
            unick_count = len(unickkeys) if unickkeys else 0
            if unick_count != quantity:
                self.add_error("unickkey", "Unique key count must match variation quantity.")

            if quantity and imei_lines and len(imei_lines) != quantity:
                self.add_error("imei_numbers", "IMEI count must match variation quantity.")

            if len(set(imei_lines)) != len(imei_lines):
                self.add_error("imei_numbers", "Duplicate IMEI numbers are not allowed.")

        return cleaned



class BranchProductStockForm(ProductStyledModelForm):
    class Meta:
        model = BranchProductStock
        fields = [
            "stock_branch",
            "product_name",
            "product_variation",
            "quantity",
            "unickkey",
        ]
        widgets = {
            "stock_branch": forms.Select(attrs={"class": COMMON_SELECT}),
            "product_name": forms.Select(attrs={"class": COMMON_SELECT}),
            "product_variation": forms.Select(attrs={"class": COMMON_SELECT}),
            "quantity": forms.NumberInput(attrs={"class": COMMON_INPUT}),
            "unickkey": forms.SelectMultiple(attrs={"class": COMMON_MULTI}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        user = getattr(self.request, "user", None)
        scope = get_user_scope(user)
        self.fields["stock_branch"].queryset = scope["branches"].order_by("name")

        # related modal enabled fields
        related_map = {
            "stock_branch": "branch",
            "product_name": "product",
            "unickkey": "unick",
        }

        for field_name, model_name in related_map.items():
            field = self.fields[field_name]
            field.widget.attrs["data_related_model"] = model_name
            field.widget.attrs["data_parent_field"] = field_name
            field.widget.attrs["can_add_related"] = True
            field.widget.attrs["can_change_related"] = True

            if field_name == "unickkey":
                if self.is_bound:
                    selected_values = self.data.getlist(field_name)
                elif self.instance.pk:
                    selected_values = [str(v) for v in self.instance.unickkey.values_list("pk", flat=True)]
                else:
                    selected_values = []
                field.widget.attrs["data-selected-value"] = ",".join(selected_values)
            else:
                value = self.initial.get(field_name) or getattr(self.instance, f"{field_name}_id", "")
                field.widget.attrs["data-selected-value"] = str(value or "")

        # product_variation depends on product_name
        product_id = None
        if self.is_bound:
            product_id = self.data.get("product_name")
        elif self.instance.pk and self.instance.product_name_id:
            product_id = self.instance.product_name_id

        if product_id:
            self.fields["product_variation"].queryset = Variation.objects.filter(
                product_name_id=product_id
            ).order_by("name", "id")
        else:
            self.fields["product_variation"].queryset = Variation.objects.none()

        # selected variation
        if self.is_bound:
            variation_value = self.data.get("product_variation", "")
        else:
            variation_value = getattr(self.instance, "product_variation_id", "") if self.instance.pk else ""

        self.fields["product_variation"].widget.attrs["data-selected-value"] = str(variation_value or "")

        # optional:
        # product_variation icon only if variation modal route exists
        self.fields["product_variation"].widget.attrs["data_related_model"] = "variation"
        self.fields["product_variation"].widget.attrs["data_parent_field"] = "product_variation"
        self.fields["product_variation"].widget.attrs["can_add_related"] = True
        self.fields["product_variation"].widget.attrs["can_change_related"] = True

        # unick depends on variation
        variation_id = None
        if self.is_bound:
            variation_id = self.data.get("product_variation")
        elif self.instance.pk and self.instance.product_variation_id:
            variation_id = self.instance.product_variation_id

        if variation_id:
            variation = Variation.objects.filter(pk=variation_id).prefetch_related("unickkey").first()
            if variation:
                self.fields["unickkey"].queryset = variation.unickkey.all().order_by("id")
            else:
                self.fields["unickkey"].queryset = unick.objects.none()
        else:
            self.fields["unickkey"].queryset = unick.objects.none()

        # Re-apply selected state after dependent querysets are rebuilt.
        self.apply_selected_state()

    def clean(self):
        cleaned = super().clean()
        product = cleaned.get("product_name")
        variation = cleaned.get("product_variation")

        if variation and product and variation.product_name_id != product.id:
            self.add_error("product_variation", "Variation does not belong to selected product.")
        return cleaned

