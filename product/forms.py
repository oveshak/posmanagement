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





















from django import forms
from django.forms import inlineformset_factory

from user.models import Branch
from .models import (
    Unit,
    Category,
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

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "sku",
            "unit_name",
            "category_name",
            "brand_name",
            "warranty_name",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "sku": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "unit_name": forms.Select(attrs={"class": COMMON_SELECT}),
            "category_name": forms.Select(attrs={"class": COMMON_SELECT}),
            "brand_name": forms.Select(attrs={"class": COMMON_SELECT}),
            "warranty_name": forms.Select(attrs={"class": COMMON_SELECT}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        related_map = {
            "unit_name": "unit",
            "category_name": "category",
            "brand_name": "brand",
            "warranty_name": "warranty",
        }

        for field_name, model_name in related_map.items():
            field = self.fields[field_name]
            field.widget.attrs["data_related_model"] = model_name
            field.widget.attrs["data_parent_field"] = field_name
            field.widget.attrs["can_add_related"] = True
            field.widget.attrs["can_change_related"] = True

            value = self.initial.get(field_name) or getattr(self.instance, f"{field_name}_id", "")
            field.widget.attrs["data-selected-value"] = str(value or "")


class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = [
            "name",
            "sku_suffix",
            "price",
            "quantity",
            "dealer_price",
            "isunck",
            "unickkey",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "sku_suffix": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "price": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01"}),
            "quantity": forms.NumberInput(attrs={"class": COMMON_INPUT}),
            "dealer_price": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01"}),
            "isunck": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"}),
            "unickkey": forms.SelectMultiple(attrs={"class": COMMON_MULTI}),
        }

    def clean(self):
        cleaned = super().clean()
        isunck = cleaned.get("isunck")
        unickkeys = cleaned.get("unickkey")

        if isunck and not unickkeys and not cleaned.get("DELETE", False):
            self.add_error("unickkey", "Unique key required when 'Has Unique Key' is checked.")
        return cleaned


VariationFormSet = inlineformset_factory(
    Product,
    Variation,
    form=VariationForm,
    extra=1,
    can_delete=True,
)


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": COMMON_INPUT})}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": COMMON_INPUT})}


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": COMMON_INPUT})}


class WarrantyForm(forms.ModelForm):
    class Meta:
        model = Warranty
        fields = ["name", "duration", "duration_type"]
        widgets = {
            "name": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "duration": forms.NumberInput(attrs={"class": COMMON_INPUT}),
            "duration_type": forms.Select(attrs={"class": COMMON_SELECT}),
        }


class UnickForm(forms.ModelForm):
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



class VariationQuickForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = [
            "product_name",
            "name",
            "sku_suffix",
            "price",
            "quantity",
            "dealer_price",
            "isunck",
            "unickkey",
        ]
        widgets = {
            "product_name": forms.Select(attrs={"class": COMMON_SELECT}),
            "name": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "sku_suffix": forms.TextInput(attrs={"class": COMMON_INPUT}),
            "price": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01"}),
            "quantity": forms.NumberInput(attrs={"class": COMMON_INPUT}),
            "dealer_price": forms.NumberInput(attrs={"class": COMMON_INPUT, "step": "0.01"}),
            "isunck": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"}),
            "unickkey": forms.SelectMultiple(attrs={"class": COMMON_MULTI}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    def clean(self):
        cleaned = super().clean()
        isunck = cleaned.get("isunck")
        unickkeys = cleaned.get("unickkey")

        if isunck and not unickkeys:
            self.add_error("unickkey", "Unique key required when 'Has Unique Key' is checked.")
        return cleaned



class BranchProductStockForm(forms.ModelForm):
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
        super().__init__(*args, **kwargs)

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

    def clean(self):
        cleaned = super().clean()
        product = cleaned.get("product_name")
        variation = cleaned.get("product_variation")

        if variation and product and variation.product_name_id != product.id:
            self.add_error("product_variation", "Variation does not belong to selected product.")
        return cleaned

