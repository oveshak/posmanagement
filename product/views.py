# # from decimal import Decimal

# # from django.contrib import messages
# # from django.contrib.auth.mixins import LoginRequiredMixin
# # from django.db import transaction
# # from django.db.models import Q, Prefetch
# # from django.http import HttpResponse, HttpResponseForbidden
# # from django.shortcuts import get_object_or_404, redirect, render
# # from django.urls import reverse_lazy
# # from django.views import View
# # from django.views.generic import ListView

# # from user.models import Branch, Users
# # from user.utils import log_activity
# # from user.views import htmx_trigger_response, is_htmx



# # from .forms import (
# #     PurchaseForm,
# #     PurchaseItemForm,
# #     StockTransferForm,

# #     StockAdjustmentForm,
# #     VendorChequeForm,

# # from .models import (
# #     Product,
# #     Variation,
# #     unick,
# #     PurchaseItem,
# #     Purchase,
# #     PurchaseReturn,
# #     StockTransfer,
# #     StockTransferLine,

# #     VendorCheque,
# #     RepairRequest,


# #     def get_template_names(self):
# #         if self.request.headers.get("HX-Request") == "true" and self.partial_template_name:
# #             return [self.partial_template_name]
# #         return [self.template_name]
# #         obj.delete()


# #         messages.success(request, self.success_message)

# #         if is_htmx(request):
# #             return htmx_trigger_response({
# #                 "crud:deleted": {
# #                     "message": self.success_message,
# #                     "refreshList": True,
# #                 }

# #         return redirect(self.success_url)


# # # ---------------- PURCHASE RETURN ----------------

# # class PurchaseReturnListView(LoginRequiredMixin, HtmxListMixin, ListView):
# #     model = PurchaseReturn
# #     template_name = "products/purchase_return_list.html"
# #     partial_template_name = "products/partials/purchase_return_list_content.html"
# #     context_object_name = "returns"

# #     def get_queryset(self):
# #         qs = PurchaseReturn.objects.select_related("purchase_name").order_by("-return_date", "-id")
# #         search = self.request.GET.get("search", "").strip()
# #         if search:
# #             qs = qs.filter(purchase_name__supplier_name__name__icontains=search)
# #         return qs

# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         context["selected_search"] = self.request.GET.get("search", "").strip()
# #         return context


# # class PurchaseReturnCreateView(LoginRequiredMixin, View):
# #     template_name = "products/simple_form.html"
# #     success_url = reverse_lazy("purchase_return_list")

# #     def get(self, request, *args, **kwargs):
# #         return render(request, self.template_name, {"form": PurchaseReturnForm(), "title": "Create Purchase Return", "object": None})

# #     def post(self, request, *args, **kwargs):
# #         form = PurchaseReturnForm(request.POST)
# #         if form.is_valid():
# #             obj = form.save()
# #             log_activity(request, "create", f"Created purchase return #{obj.id}")
# #             messages.success(request, "Purchase return created successfully.")
# #             return redirect(self.success_url)
# #         return render(request, self.template_name, {"form": form, "title": "Create Purchase Return", "object": None})


# # class PurchaseReturnUpdateView(LoginRequiredMixin, View):
# #     template_name = "products/simple_form.html"
# #     success_url = reverse_lazy("purchase_return_list")

# #     def get_object(self, pk):
# #         return get_object_or_404(PurchaseReturn, pk=pk)

# #     def get(self, request, pk, *args, **kwargs):
# #         obj = self.get_object(pk)
# #         return render(request, self.template_name, {"form": PurchaseReturnForm(instance=obj), "title": "Update Purchase Return", "object": obj})

# #     def post(self, request, pk, *args, **kwargs):
# #         obj = self.get_object(pk)
# #         form = PurchaseReturnForm(request.POST, instance=obj)
# #         if form.is_valid():
# #             obj = form.save()
# #             log_activity(request, "update", f"Updated purchase return #{obj.id}")
# #             messages.success(request, "Purchase return updated successfully.")
# #             return redirect(self.success_url)
# #         return render(request, self.template_name, {"form": form, "title": "Update Purchase Return", "object": obj})


# # class PurchaseReturnDeleteView(BaseNoTemplateDeleteView):
# #     model = PurchaseReturn
# #     success_url = reverse_lazy("purchase_return_list")
# #     success_message = "Purchase return deleted successfully."


# # # ---------------- STOCK TRANSFER ----------------

# # class StockTransferListView(LoginRequiredMixin, HtmxListMixin, ListView):
# #     model = StockTransfer
# #     template_name = "products/stock_transfer_list.html"
# #     partial_template_name = "products/partials/stock_transfer_list_content.html"
# #     context_object_name = "transfers"

# #     def get_queryset(self):
# #         qs = StockTransfer.objects.select_related("from_branch_name", "to_branch_name").prefetch_related("lines").order_by("-transfer_date", "-id")
# #         search = self.request.GET.get("search", "").strip()
# #         status = self.request.GET.get("stc_status", "").strip()

# #         if search:
# #             qs = qs.filter(
# #                 Q(from_branch_name__name__icontains=search) |
# #                 Q(to_branch_name__name__icontains=search)
# #             )
# #         if status:
# #             qs = qs.filter(stc_status__icontains=status)

# #         return qs

# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         context["selected_search"] = self.request.GET.get("search", "").strip()
# #         context["selected_status"] = self.request.GET.get("stc_status", "").strip()
# #         return context


# # class StockTransferCreateView(LoginRequiredMixin, View):
# #     template_name = "products/stock_transfer_form.html"
# #     success_url = reverse_lazy("stock_transfer_list")

# #     def get(self, request, *args, **kwargs):
# #         form = StockTransferForm()
# #         formset = StockTransferLineFormSet()
# #         return render(request, self.template_name, {"form": form, "formset": formset, "object": None})

# #     @transaction.atomic
# #     def post(self, request, *args, **kwargs):
# #         form = StockTransferForm(request.POST)
# #         formset = StockTransferLineFormSet(request.POST)

# #         if form.is_valid() and formset.is_valid():
# #             obj = form.save()
# #             formset.instance = obj
# #             formset.save()

# #             log_activity(request, "create", f"Created stock transfer #{obj.id}")
# #             messages.success(request, "Stock transfer created successfully.")
# #             return redirect(self.success_url)

# #         return render(request, self.template_name, {"form": form, "formset": formset, "object": None})


# # class StockTransferUpdateView(LoginRequiredMixin, View):
# #     template_name = "products/stock_transfer_form.html"
# #     success_url = reverse_lazy("stock_transfer_list")

# #     def get_object(self, pk):
# #         return get_object_or_404(StockTransfer, pk=pk)

# #     def get(self, request, pk, *args, **kwargs):
# #         obj = self.get_object(pk)
# #         form = StockTransferForm(instance=obj)
# #         formset = StockTransferLineFormSet(instance=obj)
# #         return render(request, self.template_name, {"form": form, "formset": formset, "object": obj})

# #     @transaction.atomic
# #     def post(self, request, pk, *args, **kwargs):
# #         obj = self.get_object(pk)
# #         form = StockTransferForm(request.POST, instance=obj)
# #         formset = StockTransferLineFormSet(request.POST, instance=obj)

# #         if form.is_valid() and formset.is_valid():
# #             obj = form.save()
# #             formset.save()

# #             log_activity(request, "update", f"Updated stock transfer #{obj.id}")
# #             messages.success(request, "Stock transfer updated successfully.")
# #             return redirect(self.success_url)

# #         return render(request, self.template_name, {"form": form, "formset": formset, "object": obj})


# # class StockTransferDeleteView(BaseNoTemplateDeleteView):
# #     model = StockTransfer
# #     success_url = reverse_lazy("stock_transfer_list")
# #     success_message = "Stock transfer deleted successfully."


# # # ---------------- STOCK ADJUSTMENT ----------------

# # class StockAdjustmentListView(LoginRequiredMixin, HtmxListMixin, ListView):
# #     model = StockAdjustment
# #     template_name = "products/stock_adjustment_list.html"
# #     partial_template_name = "products/partials/stock_adjustment_list_content.html"
# #     context_object_name = "adjustments"

# #     def get_queryset(self):
# #         qs = StockAdjustment.objects.select_related("branch_name", "product_name").order_by("-id")
# #         search = self.request.GET.get("search", "").strip()
# #         if search:
# #             qs = qs.filter(
# #                 Q(branch_name__name__icontains=search) |
# #                 Q(product_name__name__icontains=search) |
# #                 Q(reason__icontains=search)
# #             )
# #         return qs

# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         context["selected_search"] = self.request.GET.get("search", "").strip()
# #         return context


# # class StockAdjustmentCreateView(LoginRequiredMixin, View):
# #     template_name = "products/simple_form.html"
# #     success_url = reverse_lazy("stock_adjustment_list")

# #     def get(self, request, *args, **kwargs):
# #         return render(request, self.template_name, {"form": StockAdjustmentForm(), "title": "Create Stock Adjustment", "object": None})

# #     def post(self, request, *args, **kwargs):
# #         form = StockAdjustmentForm(request.POST)
# #         if form.is_valid():
# #             obj = form.save()
# #             log_activity(request, "create", f"Created stock adjustment #{obj.id}")
# #             messages.success(request, "Stock adjustment created successfully.")
# #             return redirect(self.success_url)
# #         return render(request, self.template_name, {"form": form, "title": "Create Stock Adjustment", "object": None})


# # class StockAdjustmentUpdateView(LoginRequiredMixin, View):
# #     template_name = "products/simple_form.html"
# #     success_url = reverse_lazy("stock_adjustment_list")

# #     def get_object(self, pk):
# #         return get_object_or_404(StockAdjustment, pk=pk)

# #     def get(self, request, pk, *args, **kwargs):
# #         obj = self.get_object(pk)
# #         return render(request, self.template_name, {"form": StockAdjustmentForm(instance=obj), "title": "Update Stock Adjustment", "object": obj})

# #     def post(self, request, pk, *args, **kwargs):
# #         obj = self.get_object(pk)
# #         form = StockAdjustmentForm(request.POST, instance=obj)
# #         if form.is_valid():
# #             obj = form.save()
# #             log_activity(request, "update", f"Updated stock adjustment #{obj.id}")
# #             messages.success(request, "Stock adjustment updated successfully.")
# #             return redirect(self.success_url)
# #         return render(request, self.template_name, {"form": form, "title": "Update Stock Adjustment", "object": obj})


# # class StockAdjustmentDeleteView(BaseNoTemplateDeleteView):
# #     model = StockAdjustment
# #     success_url = reverse_lazy("stock_adjustment_list")
# #     success_message = "Stock adjustment deleted successfully."


# # # ---------------- VENDOR CHEQUE ----------------

# # class VendorChequeListView(LoginRequiredMixin, HtmxListMixin, ListView):
# #     model = VendorCheque
# #     template_name = "products/vendor_cheque_list.html"
# #     partial_template_name = "products/partials/vendor_cheque_list_content.html"
# #     context_object_name = "cheques"

# #     def get_queryset(self):
# #         qs = VendorCheque.objects.select_related("vendor_name").order_by("-issue_date", "-id")
# #         search = self.request.GET.get("search", "").strip()
# #         status = self.request.GET.get("vndcq_status", "").strip()

# #         if search:
# #             qs = qs.filter(
# #                 Q(cheque_number__icontains=search) |
# #                 Q(vendor_name__name__icontains=search)
# #             )
# #         if status:
# #             qs = qs.filter(vndcq_status__icontains=status)

# #         return qs

# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         context["selected_search"] = self.request.GET.get("search", "").strip()
# #         context["selected_status"] = self.request.GET.get("vndcq_status", "").strip()
# #         return context


# # class VendorChequeCreateView(LoginRequiredMixin, View):
# #     template_name = "products/simple_form.html"
# #     success_url = reverse_lazy("vendor_cheque_list")

# #     def get(self, request, *args, **kwargs):
# #         return render(request, self.template_name, {"form": VendorChequeForm(), "title": "Create Vendor Cheque", "object": None})

# #     def post(self, request, *args, **kwargs):
# #         form = VendorChequeForm(request.POST)
# #         if form.is_valid():
# #             obj = form.save()
# #             log_activity(request, "create", f"Created vendor cheque #{obj.id}")
# #             messages.success(request, "Vendor cheque created successfully.")
# #             return redirect(self.success_url)
# #         return render(request, self.template_name, {"form": form, "title": "Create Vendor Cheque", "object": None})


# # class VendorChequeUpdateView(LoginRequiredMixin, View):
# #     template_name = "products/simple_form.html"
# #     success_url = reverse_lazy("vendor_cheque_list")

# #     def get_object(self, pk):
# #         return get_object_or_404(VendorCheque, pk=pk)

# #     def get(self, request, pk, *args, **kwargs):
# #         obj = self.get_object(pk)
# #         return render(request, self.template_name, {"form": VendorChequeForm(instance=obj), "title": "Update Vendor Cheque", "object": obj})

# #     def post(self, request, pk, *args, **kwargs):
# #         obj = self.get_object(pk)
# #         form = VendorChequeForm(request.POST, instance=obj)
# #         if form.is_valid():
# #             obj = form.save()
# #             log_activity(request, "update", f"Updated vendor cheque #{obj.id}")
# #             messages.success(request, "Vendor cheque updated successfully.")
# #             return redirect(self.success_url)
# #         return render(request, self.template_name, {"form": form, "title": "Update Vendor Cheque", "object": obj})


# # class VendorChequeDeleteView(BaseNoTemplateDeleteView):
# #     model = VendorCheque
# #     success_url = reverse_lazy("vendor_cheque_list")
# #     success_message = "Vendor cheque deleted successfully."


# # # ---------------- REPAIR REQUEST ----------------

# # class RepairRequestListView(LoginRequiredMixin, HtmxListMixin, ListView):
# #     model = RepairRequest
# #     template_name = "products/repair_request_list.html"
# #     partial_template_name = "products/partials/repair_request_list_content.html"
# #     context_object_name = "repairs"

# #     def get_queryset(self):
# #         qs = RepairRequest.objects.select_related(
# #             "product_name", "customer_name", "branch_name", "requested_by_user_name"
# #         ).order_by("-request_date", "-id")

# #         search = self.request.GET.get("search", "").strip()
# #         status = self.request.GET.get("repair_status", "").strip()

# #         if search:
# #             qs = qs.filter(
# #                 Q(product_name__name__icontains=search) |
# #                 Q(customer_name__name__icontains=search) |
# #                 Q(branch_name__name__icontains=search) |
# #                 Q(notes__icontains=search)
# #             )
# #         if status:
# #             qs = qs.filter(repair_status__icontains=status)

# #         return qs

# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         context["selected_search"] = self.request.GET.get("search", "").strip()
# #         context["selected_status"] = self.request.GET.get("repair_status", "").strip()
# #         return context


# # class RepairRequestCreateView(LoginRequiredMixin, View):
# #     template_name = "products/simple_form.html"
# #     success_url = reverse_lazy("repair_request_list")

# #     def get(self, request, *args, **kwargs):
# #         return render(request, self.template_name, {"form": RepairRequestForm(), "title": "Create Repair Request", "object": None})

# #     def post(self, request, *args, **kwargs):
# #         form = RepairRequestForm(request.POST)
# #         if form.is_valid():
# #             obj = form.save()
# #             log_activity(request, "create", f"Created repair request #{obj.id}")
# #             messages.success(request, "Repair request created successfully.")
# #             return redirect(self.success_url)
# #         return render(request, self.template_name, {"form": form, "title": "Create Repair Request", "object": None})


# # class RepairRequestUpdateView(LoginRequiredMixin, View):
# #     template_name = "products/simple_form.html"
# #     success_url = reverse_lazy("repair_request_list")

# #     def get_object(self, pk):
# #         return get_object_or_404(RepairRequest, pk=pk)

# #     def get(self, request, pk, *args, **kwargs):
# #         obj = self.get_object(pk)
# #         return render(request, self.template_name, {"form": RepairRequestForm(instance=obj), "title": "Update Repair Request", "object": obj})

# #     def post(self, request, pk, *args, **kwargs):
# #         obj = self.get_object(pk)
# #         form = RepairRequestForm(request.POST, instance=obj)
# #         if form.is_valid():
# #             obj = form.save()
# #             log_activity(request, "update", f"Updated repair request #{obj.id}")
# #             messages.success(request, "Repair request updated successfully.")
# #             return redirect(self.success_url)
# #         return render(request, self.template_name, {"form": form, "title": "Update Repair Request", "object": obj})


# # class RepairRequestDeleteView(BaseNoTemplateDeleteView):
# #     model = RepairRequest
# #     success_url = reverse_lazy("repair_request_list")
# #     success_message = "Repair request deleted successfully."


# # from django.http import JsonResponse
# # from django.views.decorators.http import require_GET, require_http_methods
# # from django.contrib.auth.decorators import login_required

# # from .forms import SupplierForm, ProductForm, VariationForm, UnickForm
# # from .models import Supplier


# # def compact_option(obj):
# #     if hasattr(obj, "name") and obj.name:
# #         text = obj.name
# #     elif hasattr(obj, "key1") and obj.key1:
# #         text = f"{obj.key1} - {obj.key2 or ''}"
# #     else:
# #         text = str(obj)
# #     return {"id": obj.pk, "text": text}


# # @login_required
# # @require_GET
# # def ajax_variations_by_product(request):
# #     product_id = request.GET.get("product_id", "").strip()
# #     qs = Variation.objects.all().order_by("name", "id")

# #     if product_id:
# #         qs = qs.filter(product_name_id=product_id)

# #     return JsonResponse({
# #         "results": [compact_option(obj) for obj in qs]
# #     })


# # @login_required
# # @require_GET
# # def ajax_unick_by_variation(request):
# #     variation_id = request.GET.get("variation_id", "").strip()
# #     qs = unick.objects.none()

# #     if variation_id:
# #         variation = Variation.objects.filter(pk=variation_id).prefetch_related("unickkey").first()
# #         if variation:
# #             qs = variation.unickkey.all().order_by("id")

# #     return JsonResponse({
# #         "results": [compact_option(obj) for obj in qs]
# #     })


# # @login_required
# # @require_http_methods(["GET", "POST"])
# # def related_object_modal(request, model_name, pk=None):
# #     model_name = (model_name or "").lower().strip()

# #     MODEL_CONFIG = {
# #         "supplier": {
# #             "model": Supplier,
# #             "form": SupplierForm,
# #         },
# #         "product": {
# #             "model": Product,
# #             "form": ProductForm,
# #         },
# #         "variation": {
# #             "model": Variation,
# #             "form": VariationForm,
# #         },
# #         "unick": {
# #             "model": unick,
# #             "form": UnickForm,
# #         },
# #         "branch": {
# #             "model": Branch,
# #             "form": None,  # branch app-er form use korle ekhane import dite hobe
# #         },
# #         "user": {
# #             "model": Users,
# #             "form": None,  # user app-er quick form use korle import dite hobe
# #         },
# #     }

# #     if model_name not in MODEL_CONFIG:
# #         return HttpResponse("Invalid related model.", status=400)

# #     config = MODEL_CONFIG[model_name]
# #     model_class = config["model"]
# #     form_class = config["form"]

# #     if form_class is None:
# #         return HttpResponse(f"{model_name} modal form not configured yet.", status=400)

# #     instance = get_object_or_404(model_class, pk=pk) if pk else None
# #     parent_field = request.GET.get("parent_field") or request.POST.get("_parent_field", "")

# #     if request.method == "POST":
# #         form = form_class(request.POST, instance=instance)
# #         if form.is_valid():
# #             obj = form.save()
# #             return htmx_trigger_response({
# #                 "related:saved": {
# #                     "parentField": parent_field,
# #                     "option": {
# #                         "id": obj.pk,
# #                         "text": str(obj),
# #                     },
# #                     "message": f"{model_name.title()} saved successfully."
# #                 }
# #             })
# #     else:
# #         form = form_class(instance=instance)

# #     context = {
# #         "form": form,
# #         "title": model_name.title(),
# #         "object": instance,
# #         "parent_field": parent_field,
# #         "post_url": request.path,
# #     }
# #     return render(request, "products/modals/related_simple_form.html", context)


# from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.db import transaction
# from django.db.models import Q
# from django.http import HttpResponse, HttpResponseForbidden
# from django.shortcuts import get_object_or_404, redirect, render
# from django.urls import reverse_lazy
# from django.views import View
# from django.views.generic import ListView
# from django.http import JsonResponse
# from django.views.decorators.http import require_http_methods
# from django.contrib.auth.decorators import login_required

# from user.utils import log_activity
# from user.views import is_htmx, htmx_trigger_response

# from .models import Unit, Category, Brand, Warranty, Product, Variation, unick
# from .forms import (
#     ProductForm,
#     VariationFormSet,
#     UnitForm,
#     CategoryForm,
#     BrandForm,
#     WarrantyForm,
#     UnickForm,
# )


# class HtmxListMixin:
#     partial_template_name = None

#     def get_template_names(self):
#         if self.request.headers.get("HX-Request") == "true" and self.partial_template_name:
#             return [self.partial_template_name]
#         return [self.template_name]


# class BaseNoTemplateDeleteView(LoginRequiredMixin, View):
#     model = None
#     success_url = None
#     success_message = "Deleted successfully."

#     def post(self, request, pk, *args, **kwargs):
#         obj = get_object_or_404(self.model, pk=pk)
#         label = str(obj)
#         obj.delete()

#         log_activity(request, "delete", f"Deleted {label}")
#         messages.success(request, self.success_message)

#         if is_htmx(request):
#             return htmx_trigger_response({
#                 "crud:deleted": {
#                     "message": self.success_message,
#                     "refreshList": True,
#                 }
#             })

#         return redirect(self.success_url)


# class ProductListView(LoginRequiredMixin, HtmxListMixin, ListView):
#     model = Product
#     template_name = "products/product_list.html"
#     partial_template_name = "products/partials/product_list_content.html"
#     context_object_name = "products"
#     paginate_by = 20

#     def get_queryset(self):
#         qs = Product.objects.select_related(
#             "unit_name", "category_name", "brand_name", "warranty_name"
#         ).prefetch_related("variations").order_by("name")

#         search = self.request.GET.get("search", "").strip()
#         category_id = self.request.GET.get("category", "").strip()
#         brand_id = self.request.GET.get("brand", "").strip()

#         if search:
#             qs = qs.filter(
#                 Q(name__icontains=search) |
#                 Q(sku__icontains=search) |
#                 Q(category_name__name__icontains=search) |
#                 Q(brand_name__name__icontains=search)
#             )

#         if category_id:
#             qs = qs.filter(category_name_id=category_id)

#         if brand_id:
#             qs = qs.filter(brand_name_id=brand_id)

#         return qs.distinct()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["categories"] = Category.objects.order_by("name")
#         context["brands"] = Brand.objects.order_by("name")
#         context["selected_search"] = self.request.GET.get("search", "").strip()
#         context["selected_category"] = self.request.GET.get("category", "").strip()
#         context["selected_brand"] = self.request.GET.get("brand", "").strip()
#         return context


# class ProductCreateView(LoginRequiredMixin, View):
#     template_name = "products/product_form.html"
#     success_url = reverse_lazy("product_list")

#     def get(self, request, *args, **kwargs):
#         context = {
#             "form": ProductForm(),
#             "formset": VariationFormSet(prefix="variations"),
#             "object": None,
#         }
#         return render(request, self.template_name, context)

#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         form = ProductForm(request.POST)
#         formset = VariationFormSet(request.POST, prefix="variations")

#         if form.is_valid() and formset.is_valid():
#             product = form.save()
#             formset.instance = product
#             formset.save()

#             log_activity(request, "create", f"Created product {product.name}")
#             messages.success(request, "Product created successfully.")
#             return redirect(self.success_url)

#         context = {
#             "form": form,
#             "formset": formset,
#             "object": None,
#         }
#         return render(request, self.template_name, context)


# class ProductUpdateView(LoginRequiredMixin, View):
#     template_name = "products/product_form.html"
#     success_url = reverse_lazy("product_list")

#     def get_object(self, pk):
#         return get_object_or_404(Product.objects.prefetch_related("variations__unickkey"), pk=pk)

#     def get(self, request, pk, *args, **kwargs):
#         obj = self.get_object(pk)
#         context = {
#             "form": ProductForm(instance=obj),
#             "formset": VariationFormSet(instance=obj, prefix="variations"),
#             "object": obj,
#         }
#         return render(request, self.template_name, context)

#     @transaction.atomic
#     def post(self, request, pk, *args, **kwargs):
#         obj = self.get_object(pk)
#         form = ProductForm(request.POST, instance=obj)
#         formset = VariationFormSet(request.POST, instance=obj, prefix="variations")

#         if form.is_valid() and formset.is_valid():
#             product = form.save()
#             formset.save()

#             log_activity(request, "update", f"Updated product {product.name}")
#             messages.success(request, "Product updated successfully.")
#             return redirect(self.success_url)

#         context = {
#             "form": form,
#             "formset": formset,
#             "object": obj,
#         }
#         return render(request, self.template_name, context)


# class ProductDeleteView(BaseNoTemplateDeleteView):
#     model = Product
#     success_url = reverse_lazy("product_list")
#     success_message = "Product deleted successfully."


# # ---------- Related modal support ----------

# def compact_option(obj):
#     if hasattr(obj, "name") and obj.name:
#         text = obj.name
#     elif hasattr(obj, "key1") and obj.key1:
#         text = f"{obj.key1} - {obj.key2 or ''}"
#     else:
#         text = str(obj)
#     return {"id": obj.pk, "text": text}


# @login_required
# @require_http_methods(["GET", "POST"])
# def related_object_modals(request, model_name, pk=None):
#     model_name = (model_name or "").lower().strip()

#     MODEL_CONFIG = {
#         "unit": {"model": Unit, "form": UnitForm},
#         "category": {"model": Category, "form": CategoryForm},
#         "brand": {"model": Brand, "form": BrandForm},
#         "warranty": {"model": Warranty, "form": WarrantyForm},
#         "unick": {"model": unick, "form": UnickForm},
#     }

#     if model_name not in MODEL_CONFIG:
#         return HttpResponse("Invalid related model.", status=400)

#     config = MODEL_CONFIG[model_name]
#     model_class = config["model"]
#     form_class = config["form"]

#     instance = get_object_or_404(model_class, pk=pk) if pk else None
#     parent_field = request.GET.get("parent_field") or request.POST.get("_parent_field", "")

#     if request.method == "POST":
#         form = form_class(request.POST, instance=instance)
#         if form.is_valid():
#             obj = form.save()
#             return htmx_trigger_response({
#                 "related:saved": {
#                     "parentField": parent_field,
#                     "option": {
#                         "id": obj.pk,
#                         "text": str(obj),
#                     },
#                     "message": f"{model_name.title()} saved successfully."
#                 }
#             })
#     else:
#         form = form_class(instance=instance)

#     context = {
#         "form": form,
#         "title": model_name.title(),
#         "object": instance,
#         "parent_field": parent_field,
#         "post_url": request.path,
#     }
#     return render(request, "products/modals/related_simple_form.html", context)



import json
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.db.models import Q, Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_GET, require_http_methods
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from user.forms import BranchQuickForm
from user.forms import BranchQuickForm
from user.models import Branch, Users
from user.scope import get_user_scope, is_global_user
from user.utils import build_form_changes, log_activity
from user.views import is_htmx, htmx_trigger_response

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
    Purchase,
    PurchaseItem,
    Supplier,
)
from .forms import (
    ProductForm,
    VariationForm,
    VariationFormSet,
    UnitForm,
    CategoryForm,
    SubCategoryForm,
    VatRateForm,
    VariationAttributeForm,
    VariationAttributeValueForm,
    BrandForm,
    VariationQuickForm,
    WarrantyForm,
    UnickForm,
    BranchProductStockForm,
    PurchaseForm,
    PurchaseItemForm,
    SupplierForm,
)


class HtmxListMixin:
    partial_template_name = None

    def get_template_names(self):
        if self.request.headers.get("HX-Request") == "true" and self.partial_template_name:
            return [self.partial_template_name]
        return [self.template_name]


class BaseNoTemplateDeleteView(LoginRequiredMixin, View):
    model = None
    success_url = None
    success_message = "Deleted successfully."

    def post(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=pk)
        label = str(obj)
        obj.delete()

        log_activity(request, "delete", f"Deleted {label}", obj=obj)
        messages.success(request, self.success_message)

        if is_htmx(request):
            return htmx_trigger_response({
                "crud:deleted": {
                    "message": self.success_message,
                    "refreshList": True,
                }
            })

        return redirect(self.success_url)


# ---------------- PRODUCT CRUD ----------------

class ProductListView(LoginRequiredMixin, HtmxListMixin, ListView):
    model = Product
    template_name = "products/product_list.html"
    partial_template_name = "products/partials/product_list_content.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        qs = Product.objects.select_related(
            "unit_name", "category_name", "subcategory_name", "brand_name", "warranty_name", "business_location"
        ).prefetch_related("variations").order_by("name")

        scope = get_user_scope(self.request.user)
        allowed_branch_ids = list(scope["branches"].values_list("id", flat=True))
        if not is_global_user(self.request.user) and allowed_branch_ids:
            qs = qs.filter(
                Q(branch_product_stocks__stock_branch_id__in=allowed_branch_ids)
                | Q(branch_product_stocks__isnull=True)
            )

        search = self.request.GET.get("search", "").strip()
        category_id = self.request.GET.get("category", "").strip()
        subcategory_id = self.request.GET.get("subcategory", "").strip()
        brand_id = self.request.GET.get("brand", "").strip()

        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(sku__icontains=search) |
                Q(category_name__name__icontains=search) |
                Q(subcategory_name__name__icontains=search) |
                Q(brand_name__name__icontains=search)
            )

        if category_id:
            qs = qs.filter(category_name_id=category_id)

        if subcategory_id:
            qs = qs.filter(subcategory_name_id=subcategory_id)

        if brand_id:
            qs = qs.filter(brand_name_id=brand_id)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_qs = self.get_queryset()
        context["categories"] = Category.objects.filter(products__in=base_qs).distinct().order_by("name")
        selected_category = self.request.GET.get("category", "").strip()
        sub_qs = SubCategory.objects.filter(products__in=base_qs).select_related("category").distinct()
        if selected_category:
            sub_qs = sub_qs.filter(category_id=selected_category)
        context["subcategories"] = sub_qs.order_by("category__name", "name")
        context["brands"] = Brand.objects.filter(products__in=base_qs).distinct().order_by("name")
        context["selected_search"] = self.request.GET.get("search", "").strip()
        context["selected_category"] = selected_category
        context["selected_subcategory"] = self.request.GET.get("subcategory", "").strip()
        context["selected_brand"] = self.request.GET.get("brand", "").strip()
        return context


class ProductCreateView(LoginRequiredMixin, View):
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product:product_list")

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "form": ProductForm(request=request),
            "formset": VariationFormSet(prefix="variations"),
            "variation_attributes": VariationAttribute.objects.order_by("order", "name"),
            "object": None,
        })

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES, request=request)
        formset = VariationFormSet(request.POST, request.FILES, prefix="variations")

        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()

            log_activity(request, "create", f"Created product {product.name}", obj=product)
            messages.success(request, "Product created successfully.")
            return redirect(self.success_url)

        return render(request, self.template_name, {
            "form": form,
            "formset": formset,
            "variation_attributes": VariationAttribute.objects.order_by("order", "name"),
            "object": None,
        })


class ProductUpdateView(LoginRequiredMixin, View):
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product:product_list")

    def get_object(self, pk):
        return get_object_or_404(
            Product.objects.prefetch_related("variations__unickkey"),
            pk=pk
        )

    def get(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        return render(request, self.template_name, {
            "form": ProductForm(instance=obj, request=request),
            "formset": VariationFormSet(instance=obj, prefix="variations"),
            "variation_attributes": VariationAttribute.objects.order_by("order", "name"),
            "object": obj,
        })

    @transaction.atomic
    def post(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        form = ProductForm(request.POST, request.FILES, instance=obj, request=request)
        formset = VariationFormSet(request.POST, request.FILES, instance=obj, prefix="variations")

        if form.is_valid() and formset.is_valid():
            changes = build_form_changes(form)
            product = form.save()
            formset.save()

            log_activity(
                request,
                "update",
                f"Updated product {product.name}",
                obj=product,
                changes=changes,
            )
            messages.success(request, "Product updated successfully.")
            return redirect(self.success_url)

        return render(request, self.template_name, {
            "form": form,
            "formset": formset,
            "variation_attributes": VariationAttribute.objects.order_by("order", "name"),
            "object": obj,
        })


class ProductDeleteView(BaseNoTemplateDeleteView):
    model = Product
    success_url = reverse_lazy("product:product_list")
    success_message = "Product deleted successfully."


class ProductDetailView(LoginRequiredMixin, View):
    template_name = "products/product_view.html"

    def get(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(
            Product.objects.select_related(
                "unit_name", "category_name", "subcategory_name", "brand_name", "warranty_name", "vat_rate"
            ).prefetch_related("variations__attribute_values__attribute", "variations__unickkey"),
            pk=pk,
        )
        return render(request, self.template_name, {"object": obj})


# ---------------- PURCHASE CRUD ----------------

def _to_decimal(value, default="0"):
    try:
        return Decimal(str(value or default).strip() or default)
    except (InvalidOperation, ValueError, AttributeError):
        return Decimal(default)


def _recalculate_purchase_totals(purchase):
    items = purchase.purchaseitem.all()
    sub_total = sum([_to_decimal(i.line_total or i.net_cost or (i.unit_price or 0) * (i.qty or 0)) for i in items], Decimal("0"))

    discount_amount = _to_decimal(purchase.discount_amount)
    if purchase.discount_type == "percent":
        discount_amount = (sub_total * discount_amount / Decimal("100")).quantize(Decimal("0.01"))

    taxable_base = max(sub_total - discount_amount, Decimal("0"))
    purchase_tax_amount = Decimal("0")
    if purchase.purchase_tax_rate_id:
        purchase_tax_amount = (taxable_base * _to_decimal(purchase.purchase_tax_rate.rate_percent) / Decimal("100")).quantize(Decimal("0.01"))

    other_charges = (
        _to_decimal(purchase.additional_shipping_charges)
        + _to_decimal(purchase.additional_expense_amount_1)
        + _to_decimal(purchase.additional_expense_amount_2)
        + _to_decimal(purchase.additional_expense_amount_3)
    )

    total_amount = taxable_base + purchase_tax_amount + other_charges
    payment_due = total_amount - (_to_decimal(purchase.advance_balance) + _to_decimal(purchase.payment_amount))

    purchase.purchase_tax_amount = purchase_tax_amount
    purchase.total_amount = total_amount.quantize(Decimal("0.01"))
    purchase.payment_due = payment_due.quantize(Decimal("0.01"))
    purchase.save(update_fields=["purchase_tax_amount", "total_amount", "payment_due"])

def _build_purchase_item_rows(request):
    product_ids = request.POST.getlist("item_product")
    variation_ids = request.POST.getlist("item_variation")
    qty_values = request.POST.getlist("item_qty")
    price_values = request.POST.getlist("item_unit_price")
    discount_values = request.POST.getlist("item_discount_percent")
    unit_tax_values = request.POST.getlist("item_tax_percent")
    unit_after_tax_values = request.POST.getlist("item_unit_cost_after_tax")
    subtotal_values = request.POST.getlist("item_subtotal")
    product_tax_values = request.POST.getlist("item_product_tax")
    net_cost_values = request.POST.getlist("item_net_cost")
    line_total_values = request.POST.getlist("item_line_total")
    margin_values = request.POST.getlist("item_margin_percent")
    selling_values = request.POST.getlist("item_selling_inc_tax")
    imei_values = request.POST.getlist("item_imei_or_serial")

    max_len = max(
        len(product_ids), len(variation_ids), len(qty_values), len(price_values),
        len(discount_values), len(unit_tax_values), len(unit_after_tax_values),
        len(subtotal_values), len(product_tax_values), len(net_cost_values),
        len(line_total_values), len(margin_values), len(selling_values), len(imei_values), 0,
    )
    rows = []
    errors = []

    for idx in range(max_len):
        product_id = (product_ids[idx] if idx < len(product_ids) else "").strip()
        variation_id = (variation_ids[idx] if idx < len(variation_ids) else "").strip()
        qty_raw = (qty_values[idx] if idx < len(qty_values) else "").strip()
        unit_price_raw = (price_values[idx] if idx < len(price_values) else "").strip()
        discount_raw = (discount_values[idx] if idx < len(discount_values) else "").strip()
        unit_tax_raw = (unit_tax_values[idx] if idx < len(unit_tax_values) else "").strip()
        unit_after_tax_raw = (unit_after_tax_values[idx] if idx < len(unit_after_tax_values) else "").strip()
        subtotal_raw = (subtotal_values[idx] if idx < len(subtotal_values) else "").strip()
        product_tax_raw = (product_tax_values[idx] if idx < len(product_tax_values) else "").strip()
        net_cost_raw = (net_cost_values[idx] if idx < len(net_cost_values) else "").strip()
        line_total_raw = (line_total_values[idx] if idx < len(line_total_values) else "").strip()
        margin_raw = (margin_values[idx] if idx < len(margin_values) else "").strip()
        selling_raw = (selling_values[idx] if idx < len(selling_values) else "").strip()
        imei_raw = (imei_values[idx] if idx < len(imei_values) else "").strip()

        if not any([product_id, variation_id, qty_raw, unit_price_raw]):
            continue

        if not product_id:
            errors.append(f"Row {idx + 1}: Product is required.")
            continue

        if not variation_id:
            errors.append(f"Row {idx + 1}: Variation is required.")
            continue

        product = Product.objects.filter(pk=product_id).first()
        variation = Variation.objects.filter(pk=variation_id).first()

        if not product:
            errors.append(f"Row {idx + 1}: Invalid product selected.")
            continue

        if not variation:
            errors.append(f"Row {idx + 1}: Invalid variation selected.")
            continue

        if variation.product_name_id != product.id:
            errors.append(f"Row {idx + 1}: Variation does not belong to selected product.")
            continue

        try:
            qty = int(qty_raw or "0")
        except ValueError:
            errors.append(f"Row {idx + 1}: Quantity must be a number.")
            continue

        unit_price = _to_decimal(unit_price_raw)
        if unit_price < 0:
            errors.append(f"Row {idx + 1}: Unit price must be numeric.")
            continue

        if qty <= 0:
            errors.append(f"Row {idx + 1}: Quantity must be greater than 0.")
            continue

        imei_enabled = bool(variation.isunck or product.enable_imei_or_serial)
        imei_entries = [x.strip() for x in imei_raw.replace(",", "\n").splitlines() if x.strip()]
        if imei_enabled:
            if len(set(imei_entries)) != len(imei_entries):
                errors.append(f"Row {idx + 1}: Duplicate IMEI/serial values found.")
                continue
            if imei_entries and len(imei_entries) != qty:
                errors.append(f"Row {idx + 1}: IMEI/serial count must match quantity.")
                continue

        discount_percent = _to_decimal(discount_raw)
        unit_tax_percent = _to_decimal(unit_tax_raw)
        unit_cost_after_tax = _to_decimal(unit_after_tax_raw)
        subtotal_before_tax = _to_decimal(subtotal_raw)
        product_tax_amount = _to_decimal(product_tax_raw)
        net_cost = _to_decimal(net_cost_raw)
        line_total = _to_decimal(line_total_raw)
        line_profit_margin_percent = _to_decimal(margin_raw)
        unit_selling_price_inc_tax = _to_decimal(selling_raw)

        if subtotal_before_tax <= 0:
            subtotal_before_tax = (unit_price * qty).quantize(Decimal("0.01"))

        if unit_cost_after_tax <= 0:
            unit_cost_after_tax = (unit_price * (Decimal("1") + unit_tax_percent / Decimal("100"))).quantize(Decimal("0.01"))

        if product_tax_amount <= 0:
            product_tax_amount = ((subtotal_before_tax - (subtotal_before_tax * discount_percent / Decimal("100"))) * unit_tax_percent / Decimal("100")).quantize(Decimal("0.01"))

        if net_cost <= 0:
            net_cost = (subtotal_before_tax - (subtotal_before_tax * discount_percent / Decimal("100")) + product_tax_amount).quantize(Decimal("0.01"))

        if line_total <= 0:
            line_total = net_cost

        rows.append(
            {
                "product": product,
                "variation": variation,
                "qty": qty,
                "unit_price": unit_price,
                "unit_cost_before_tax": unit_price,
                "discount_percent": discount_percent,
                "discount_amount": (subtotal_before_tax * discount_percent / Decimal("100")).quantize(Decimal("0.01")),
                "unit_cost_tax_percent": unit_tax_percent,
                "unit_cost_after_tax": unit_cost_after_tax,
                "subtotal_before_tax": subtotal_before_tax,
                "product_tax_amount": product_tax_amount,
                "net_cost": net_cost,
                "line_total": line_total,
                "line_profit_margin_percent": line_profit_margin_percent,
                "unit_selling_price_inc_tax": unit_selling_price_inc_tax,
                "imei_or_serials": "\n".join(imei_entries) if imei_entries else imei_raw,
            }
        )

    return rows, errors


def _build_item_rows_for_template(items):
    return [
        {
            "product_id": str(item.purchase_product_id or ""),
            "variation_id": str(item.purchase_product_variation_id or ""),
            "qty": str(item.qty or 1),
            "unit_price": str(item.unit_price or "0"),
            "discount_percent": str(item.discount_percent or "0"),
            "unit_tax_percent": str(item.unit_cost_tax_percent or "0"),
            "unit_cost_after_tax": str(item.unit_cost_after_tax or "0"),
            "subtotal": str(item.subtotal_before_tax or "0"),
            "product_tax": str(item.product_tax_amount or "0"),
            "net_cost": str(item.net_cost or "0"),
            "line_total": str(item.line_total or "0"),
            "margin_percent": str(item.line_profit_margin_percent or "0"),
            "selling_inc_tax": str(item.unit_selling_price_inc_tax or "0"),
            "imei_or_serial": str(item.imei_or_serials or ""),
        }
        for item in items
    ]

class PurchaseListView(LoginRequiredMixin, HtmxListMixin, ListView):
    model = Purchase
    template_name = "products/purchase_list.html"
    partial_template_name = "products/partials/purchase_list_content.html"
    context_object_name = "purchases"
    paginate_by = 20

    def get_queryset(self):
        qs = Purchase.objects.select_related("supplier_name").prefetch_related("purchaseitem").order_by("-purchase_date", "-id")
        search = self.request.GET.get("search", "").strip()
        status = self.request.GET.get("purchase_status", "").strip()

        if search:
            qs = qs.filter(
                Q(supplier_name__name__icontains=search) |
                Q(vendor_cheque_details__icontains=search)
            )
        if status:
            qs = qs.filter(purchase_status__icontains=status)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_search"] = self.request.GET.get("search", "").strip()
        context["selected_status"] = self.request.GET.get("purchase_status", "").strip()
        return context


class PurchaseDetailView(LoginRequiredMixin, View):
    template_name = "products/purchase_view.html"

    def get(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(Purchase.objects.select_related("supplier_name").prefetch_related("purchaseitem"), pk=pk)
        items = obj.purchaseitem.select_related("purchase_product", "purchase_product_variation")
        item_rows = []
        for item in items:
            line_total = (item.unit_price or Decimal("0")) * (item.qty or 0)
            item_rows.append({"item": item, "line_total": line_total})

        return render(request, self.template_name, {
            "object": obj,
            "items": items,
            "item_rows": item_rows,
            "items_total": sum([row["line_total"] for row in item_rows], Decimal("0")),
        })


class SupplierDetailView(LoginRequiredMixin, View):
    template_name = "products/supplier_view.html"

    def get(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(Supplier, pk=pk)
        purchases = Purchase.objects.filter(supplier_name=obj).prefetch_related("purchaseitem").order_by("-purchase_date", "-id")[:20]
        total_amount = sum([p.total_amount or Decimal("0") for p in purchases], Decimal("0"))
        return render(request, self.template_name, {
            "object": obj,
            "purchases": purchases,
            "total_amount": total_amount,
        })


class PurchaseCreateView(LoginRequiredMixin, View):
    template_name = "products/purchase_form.html"
    success_url = reverse_lazy("product:purchase_list")

    def get(self, request, *args, **kwargs):
        context = {
            "form": PurchaseForm(request=request),
            "items": [],
            "item_rows": [],
            "products": Product.objects.order_by("name"),
            "object": None,
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = PurchaseForm(request.POST, request.FILES, request=request)
        item_rows, row_errors = _build_purchase_item_rows(request)

        if form.is_valid() and not row_errors:
            purchase = form.save()
            created_items = []
            for row in item_rows:
                created_items.append(PurchaseItem.objects.create(
                    purchase_product=row["product"],
                    purchase_product_variation=row["variation"],
                    qty=row["qty"],
                    unit_price=row["unit_price"],
                    unit_cost_before_tax=row["unit_cost_before_tax"],
                    discount_percent=row["discount_percent"],
                    discount_amount=row["discount_amount"],
                    unit_cost_tax_percent=row["unit_cost_tax_percent"],
                    unit_cost_after_tax=row["unit_cost_after_tax"],
                    subtotal_before_tax=row["subtotal_before_tax"],
                    product_tax_amount=row["product_tax_amount"],
                    net_cost=row["net_cost"],
                    line_total=row["line_total"],
                    line_profit_margin_percent=row["line_profit_margin_percent"],
                    unit_selling_price_inc_tax=row["unit_selling_price_inc_tax"],
                    imei_or_serials=row["imei_or_serials"],
                ))

            purchase.purchaseitem.set(created_items)

            _recalculate_purchase_totals(purchase)

            log_activity(request, "create", f"Created purchase #{purchase.id}")
            messages.success(request, "Purchase created successfully.")
            return redirect(self.success_url)

        for error in row_errors:
            messages.error(request, error)

        context = {
            "form": form,
            "items": [],
            "item_rows": [
                {
                    "product_id": request.POST.getlist("item_product")[i] if i < len(request.POST.getlist("item_product")) else "",
                    "variation_id": request.POST.getlist("item_variation")[i] if i < len(request.POST.getlist("item_variation")) else "",
                    "qty": request.POST.getlist("item_qty")[i] if i < len(request.POST.getlist("item_qty")) else "",
                    "unit_price": request.POST.getlist("item_unit_price")[i] if i < len(request.POST.getlist("item_unit_price")) else "",
                    "discount_percent": request.POST.getlist("item_discount_percent")[i] if i < len(request.POST.getlist("item_discount_percent")) else "",
                    "unit_tax_percent": request.POST.getlist("item_tax_percent")[i] if i < len(request.POST.getlist("item_tax_percent")) else "",
                    "unit_cost_after_tax": request.POST.getlist("item_unit_cost_after_tax")[i] if i < len(request.POST.getlist("item_unit_cost_after_tax")) else "",
                    "subtotal": request.POST.getlist("item_subtotal")[i] if i < len(request.POST.getlist("item_subtotal")) else "",
                    "product_tax": request.POST.getlist("item_product_tax")[i] if i < len(request.POST.getlist("item_product_tax")) else "",
                    "net_cost": request.POST.getlist("item_net_cost")[i] if i < len(request.POST.getlist("item_net_cost")) else "",
                    "line_total": request.POST.getlist("item_line_total")[i] if i < len(request.POST.getlist("item_line_total")) else "",
                    "margin_percent": request.POST.getlist("item_margin_percent")[i] if i < len(request.POST.getlist("item_margin_percent")) else "",
                    "selling_inc_tax": request.POST.getlist("item_selling_inc_tax")[i] if i < len(request.POST.getlist("item_selling_inc_tax")) else "",
                    "imei_or_serial": request.POST.getlist("item_imei_or_serial")[i] if i < len(request.POST.getlist("item_imei_or_serial")) else "",
                }
                for i in range(max(
                    len(request.POST.getlist("item_product")),
                    len(request.POST.getlist("item_variation")),
                    len(request.POST.getlist("item_qty")),
                    len(request.POST.getlist("item_unit_price")),
                    len(request.POST.getlist("item_discount_percent")),
                    len(request.POST.getlist("item_tax_percent")),
                    len(request.POST.getlist("item_unit_cost_after_tax")),
                    len(request.POST.getlist("item_subtotal")),
                    len(request.POST.getlist("item_product_tax")),
                    len(request.POST.getlist("item_net_cost")),
                    len(request.POST.getlist("item_line_total")),
                    len(request.POST.getlist("item_margin_percent")),
                    len(request.POST.getlist("item_selling_inc_tax")),
                    len(request.POST.getlist("item_imei_or_serial")),
                    1,
                ))
            ],
            "products": Product.objects.order_by("name"),
            "object": None,
        }
        return render(request, self.template_name, context)


class PurchaseUpdateView(LoginRequiredMixin, View):
    template_name = "products/purchase_form.html"
    success_url = reverse_lazy("product:purchase_list")

    def get_object(self, pk):
        return get_object_or_404(Purchase.objects.prefetch_related("purchaseitem"), pk=pk)

    def get(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        context = {
            "form": PurchaseForm(instance=obj, request=request),
            "items": obj.purchaseitem.all(),
            "item_rows": _build_item_rows_for_template(obj.purchaseitem.all()),
            "products": Product.objects.order_by("name"),
            "object": obj,
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        form = PurchaseForm(request.POST, request.FILES, instance=obj, request=request)
        item_rows, row_errors = _build_purchase_item_rows(request)

        if form.is_valid() and not row_errors:
            purchase = form.save()
            old_items = list(purchase.purchaseitem.all())
            purchase.purchaseitem.clear()

            created_items = []
            for row in item_rows:
                created_items.append(PurchaseItem.objects.create(
                    purchase_product=row["product"],
                    purchase_product_variation=row["variation"],
                    qty=row["qty"],
                    unit_price=row["unit_price"],
                    unit_cost_before_tax=row["unit_cost_before_tax"],
                    discount_percent=row["discount_percent"],
                    discount_amount=row["discount_amount"],
                    unit_cost_tax_percent=row["unit_cost_tax_percent"],
                    unit_cost_after_tax=row["unit_cost_after_tax"],
                    subtotal_before_tax=row["subtotal_before_tax"],
                    product_tax_amount=row["product_tax_amount"],
                    net_cost=row["net_cost"],
                    line_total=row["line_total"],
                    line_profit_margin_percent=row["line_profit_margin_percent"],
                    unit_selling_price_inc_tax=row["unit_selling_price_inc_tax"],
                    imei_or_serials=row["imei_or_serials"],
                ))

            purchase.purchaseitem.set(created_items)

            for old_item in old_items:
                if not old_item.purchase_set.exists():
                    old_item.delete()

            _recalculate_purchase_totals(purchase)

            log_activity(request, "update", f"Updated purchase #{purchase.id}")
            messages.success(request, "Purchase updated successfully.")
            return redirect(self.success_url)

        for error in row_errors:
            messages.error(request, error)

        context = {
            "form": form,
            "items": obj.purchaseitem.all(),
            "item_rows": [
                {
                    "product_id": request.POST.getlist("item_product")[i] if i < len(request.POST.getlist("item_product")) else "",
                    "variation_id": request.POST.getlist("item_variation")[i] if i < len(request.POST.getlist("item_variation")) else "",
                    "qty": request.POST.getlist("item_qty")[i] if i < len(request.POST.getlist("item_qty")) else "",
                    "unit_price": request.POST.getlist("item_unit_price")[i] if i < len(request.POST.getlist("item_unit_price")) else "",
                    "discount_percent": request.POST.getlist("item_discount_percent")[i] if i < len(request.POST.getlist("item_discount_percent")) else "",
                    "unit_tax_percent": request.POST.getlist("item_tax_percent")[i] if i < len(request.POST.getlist("item_tax_percent")) else "",
                    "unit_cost_after_tax": request.POST.getlist("item_unit_cost_after_tax")[i] if i < len(request.POST.getlist("item_unit_cost_after_tax")) else "",
                    "subtotal": request.POST.getlist("item_subtotal")[i] if i < len(request.POST.getlist("item_subtotal")) else "",
                    "product_tax": request.POST.getlist("item_product_tax")[i] if i < len(request.POST.getlist("item_product_tax")) else "",
                    "net_cost": request.POST.getlist("item_net_cost")[i] if i < len(request.POST.getlist("item_net_cost")) else "",
                    "line_total": request.POST.getlist("item_line_total")[i] if i < len(request.POST.getlist("item_line_total")) else "",
                    "margin_percent": request.POST.getlist("item_margin_percent")[i] if i < len(request.POST.getlist("item_margin_percent")) else "",
                    "selling_inc_tax": request.POST.getlist("item_selling_inc_tax")[i] if i < len(request.POST.getlist("item_selling_inc_tax")) else "",
                    "imei_or_serial": request.POST.getlist("item_imei_or_serial")[i] if i < len(request.POST.getlist("item_imei_or_serial")) else "",
                }
                for i in range(max(
                    len(request.POST.getlist("item_product")),
                    len(request.POST.getlist("item_variation")),
                    len(request.POST.getlist("item_qty")),
                    len(request.POST.getlist("item_unit_price")),
                    len(request.POST.getlist("item_discount_percent")),
                    len(request.POST.getlist("item_tax_percent")),
                    len(request.POST.getlist("item_unit_cost_after_tax")),
                    len(request.POST.getlist("item_subtotal")),
                    len(request.POST.getlist("item_product_tax")),
                    len(request.POST.getlist("item_net_cost")),
                    len(request.POST.getlist("item_line_total")),
                    len(request.POST.getlist("item_margin_percent")),
                    len(request.POST.getlist("item_selling_inc_tax")),
                    len(request.POST.getlist("item_imei_or_serial")),
                    1,
                ))
            ],
            "products": Product.objects.order_by("name"),
            "object": obj,
        }
        return render(request, self.template_name, context)


class PurchaseDeleteView(BaseNoTemplateDeleteView):
    model = Purchase
    success_url = reverse_lazy("product:purchase_list")
    success_message = "Purchase deleted successfully."


# ---------------- BRANCH STOCK CRUD ----------------

class BranchStockListView(LoginRequiredMixin, HtmxListMixin, ListView):
    model = BranchProductStock
    template_name = "products/branch_stock_list.html"
    partial_template_name = "products/partials/branch_stock_list_content.html"
    context_object_name = "stocks"
    paginate_by = 20

    def get_queryset(self):
        qs = BranchProductStock.objects.select_related(
            "stock_branch",
            "product_name",
            "product_variation",
        ).prefetch_related("unickkey").order_by("-id")

        scope = get_user_scope(self.request.user)
        allowed_branch_ids = list(scope["branches"].values_list("id", flat=True))
        if not is_global_user(self.request.user):
            if allowed_branch_ids:
                qs = qs.filter(stock_branch_id__in=allowed_branch_ids)
            else:
                qs = qs.none()

        search = self.request.GET.get("search", "").strip()
        branch_id = self.request.GET.get("branch", "").strip()

        if search:
            qs = qs.filter(
                Q(stock_branch__name__icontains=search) |
                Q(product_name__name__icontains=search) |
                Q(product_variation__name__icontains=search)
            )

        if branch_id:
            qs = qs.filter(stock_branch_id=branch_id)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["branches"] = get_user_scope(self.request.user)["branches"].order_by("name")
        context["selected_search"] = self.request.GET.get("search", "").strip()
        context["selected_branch"] = self.request.GET.get("branch", "").strip()
        return context


class BranchStockCreateView(LoginRequiredMixin, View):
    template_name = "products/branch_stock_form.html"
    success_url = reverse_lazy("product:branch_stock_list")

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "form": BranchProductStockForm(request=request),
            "object": None,
        })

    def post(self, request, *args, **kwargs):
        form = BranchProductStockForm(request.POST, request=request)
        if form.is_valid():
            obj = form.save()
            log_activity(request, "create", f"Created branch stock {obj}", obj=obj)
            messages.success(request, "Branch stock created successfully.")
            return redirect(self.success_url)

        return render(request, self.template_name, {
            "form": form,
            "object": None,
        })


class BranchStockUpdateView(LoginRequiredMixin, View):
    template_name = "products/branch_stock_form.html"
    success_url = reverse_lazy("product:branch_stock_list")

    def get_object(self, pk):
        return get_object_or_404(BranchProductStock, pk=pk)

    def get(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        return render(request, self.template_name, {
            "form": BranchProductStockForm(instance=obj, request=request),
            "object": obj,
        })

    def post(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        form = BranchProductStockForm(request.POST, instance=obj, request=request)
        if form.is_valid():
            changes = build_form_changes(form)
            obj = form.save()
            log_activity(
                request,
                "update",
                f"Updated branch stock {obj}",
                obj=obj,
                changes=changes,
            )
            messages.success(request, "Branch stock updated successfully.")
            return redirect(self.success_url)

        return render(request, self.template_name, {
            "form": form,
            "object": obj,
        })


class BranchStockDeleteView(BaseNoTemplateDeleteView):
    model = BranchProductStock
    success_url = reverse_lazy("product:branch_stock_list")
    success_message = "Branch stock deleted successfully."


# ---------------- MASTER CRUD (UNIT/CATEGORY/BRAND/WARRANTY) ----------------

class MasterListBaseView(LoginRequiredMixin, HtmxListMixin, ListView):
    template_name = "products/master_list.html"
    partial_template_name = "products/partials/master_list_content.html"
    context_object_name = "items"
    paginate_by = 20

    page_title = "Masters"
    page_subtitle = "Manage master records"
    list_url_name = ""
    create_url_name = ""
    edit_url_name = ""
    delete_url_name = ""
    create_label = "Item"
    search_includes_duration = False
    show_parent_category = False

    def get_queryset(self):
        qs = self.model.objects.order_by("name")
        search = self.request.GET.get("search", "").strip()

        if search:
            if self.search_includes_duration:
                search_filter = (
                    Q(name__icontains=search)
                    | Q(duration_type__icontains=search)
                )
                if search.isdigit():
                    search_filter |= Q(duration=int(search))
                qs = qs.filter(search_filter)
            else:
                qs = qs.filter(name__icontains=search)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["page_subtitle"] = self.page_subtitle
        context["list_url_name"] = self.list_url_name
        context["create_url_name"] = self.create_url_name
        context["edit_url_name"] = self.edit_url_name
        context["delete_url_name"] = self.delete_url_name
        context["create_label"] = self.create_label
        context["selected_search"] = self.request.GET.get("search", "").strip()
        context["show_warranty_columns"] = self.search_includes_duration
        context["show_parent_category"] = self.show_parent_category
        return context


class MasterCreateBaseView(LoginRequiredMixin, View):
    form_class = None
    template_name = "products/simple_form.html"
    success_url = None
    object_label = "Item"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "form": self.form_class(),
            "object": None,
            "title": f"Create {self.object_label}",
            "cancel_url": self.success_url,
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save()
            log_activity(request, "create", f"Created {self.object_label} {obj}", obj=obj)
            messages.success(request, f"{self.object_label} created successfully.")
            return redirect(self.success_url)

        return render(request, self.template_name, {
            "form": form,
            "object": None,
            "title": f"Create {self.object_label}",
            "cancel_url": self.success_url,
        })


class MasterUpdateBaseView(LoginRequiredMixin, View):
    model = None
    form_class = None
    template_name = "products/simple_form.html"
    success_url = None
    object_label = "Item"

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        return render(request, self.template_name, {
            "form": self.form_class(instance=obj),
            "object": obj,
            "title": f"Update {self.object_label}",
            "cancel_url": self.success_url,
        })

    def post(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            changes = build_form_changes(form)
            obj = form.save()
            log_activity(
                request,
                "update",
                f"Updated {self.object_label} {obj}",
                obj=obj,
                changes=changes,
            )
            messages.success(request, f"{self.object_label} updated successfully.")
            return redirect(self.success_url)

        return render(request, self.template_name, {
            "form": form,
            "object": obj,
            "title": f"Update {self.object_label}",
            "cancel_url": self.success_url,
        })


class UnitListView(MasterListBaseView):
    model = Unit
    page_title = "Units"
    page_subtitle = "Manage product units"
    list_url_name = "product:unit_list"
    create_url_name = "product:unit_create"
    edit_url_name = "product:unit_update"
    delete_url_name = "product:unit_delete"
    create_label = "Unit"


class UnitCreateView(MasterCreateBaseView):
    form_class = UnitForm
    success_url = reverse_lazy("product:unit_list")
    object_label = "Unit"


class UnitUpdateView(MasterUpdateBaseView):
    model = Unit
    form_class = UnitForm
    success_url = reverse_lazy("product:unit_list")
    object_label = "Unit"


class UnitDeleteView(BaseNoTemplateDeleteView):
    model = Unit
    success_url = reverse_lazy("product:unit_list")
    success_message = "Unit deleted successfully."


class CategoryListView(MasterListBaseView):
    model = Category
    page_title = "Categories"
    page_subtitle = "Manage product categories"
    list_url_name = "product:category_list"
    create_url_name = "product:category_create"
    edit_url_name = "product:category_update"
    delete_url_name = "product:category_delete"
    create_label = "Category"


class CategoryCreateView(MasterCreateBaseView):
    form_class = CategoryForm
    success_url = reverse_lazy("product:category_list")
    object_label = "Category"


class CategoryUpdateView(MasterUpdateBaseView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("product:category_list")
    object_label = "Category"


class CategoryDeleteView(BaseNoTemplateDeleteView):
    model = Category
    success_url = reverse_lazy("product:category_list")
    success_message = "Category deleted successfully."


class SubCategoryListView(MasterListBaseView):
    model = SubCategory
    page_title = "Subcategories"
    page_subtitle = "Manage product subcategories"
    list_url_name = "product:subcategory_list"
    create_url_name = "product:subcategory_create"
    edit_url_name = "product:subcategory_update"
    delete_url_name = "product:subcategory_delete"
    create_label = "Subcategory"
    show_parent_category = True

    def get_queryset(self):
        qs = self.model.objects.select_related("category").order_by("category__name", "name")
        search = self.request.GET.get("search", "").strip()
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(category__name__icontains=search)
            )
        return qs


class SubCategoryCreateView(MasterCreateBaseView):
    form_class = SubCategoryForm
    success_url = reverse_lazy("product:subcategory_list")
    object_label = "Subcategory"


class SubCategoryUpdateView(MasterUpdateBaseView):
    model = SubCategory
    form_class = SubCategoryForm
    success_url = reverse_lazy("product:subcategory_list")
    object_label = "Subcategory"


class SubCategoryDeleteView(BaseNoTemplateDeleteView):
    model = SubCategory
    success_url = reverse_lazy("product:subcategory_list")
    success_message = "Subcategory deleted successfully."


class VariationAttributeListView(MasterListBaseView):
    model = VariationAttribute
    page_title = "Variation Attributes"
    page_subtitle = "Manage variation attribute groups like Color, RAM, ROM"
    list_url_name = "product:variation_attribute_list"
    create_url_name = "product:variation_attribute_create"
    edit_url_name = "product:variation_attribute_update"
    delete_url_name = "product:variation_attribute_delete"
    create_label = "Variation Attribute"


class VariationAttributeCreateView(MasterCreateBaseView):
    form_class = VariationAttributeForm
    success_url = reverse_lazy("product:variation_attribute_list")
    object_label = "Variation Attribute"


class VariationAttributeUpdateView(MasterUpdateBaseView):
    model = VariationAttribute
    form_class = VariationAttributeForm
    success_url = reverse_lazy("product:variation_attribute_list")
    object_label = "Variation Attribute"


class VariationAttributeDeleteView(BaseNoTemplateDeleteView):
    model = VariationAttribute
    success_url = reverse_lazy("product:variation_attribute_list")
    success_message = "Variation attribute deleted successfully."


class BrandListView(MasterListBaseView):
    model = Brand
    page_title = "Brands"
    page_subtitle = "Manage product brands"
    list_url_name = "product:brand_list"
    create_url_name = "product:brand_create"
    edit_url_name = "product:brand_update"
    delete_url_name = "product:brand_delete"
    create_label = "Brand"


class BrandCreateView(MasterCreateBaseView):
    form_class = BrandForm
    success_url = reverse_lazy("product:brand_list")
    object_label = "Brand"


class BrandUpdateView(MasterUpdateBaseView):
    model = Brand
    form_class = BrandForm
    success_url = reverse_lazy("product:brand_list")
    object_label = "Brand"


class BrandDeleteView(BaseNoTemplateDeleteView):
    model = Brand
    success_url = reverse_lazy("product:brand_list")
    success_message = "Brand deleted successfully."


class WarrantyListView(MasterListBaseView):
    model = Warranty
    page_title = "Warranties"
    page_subtitle = "Manage product warranties"
    list_url_name = "product:warranty_list"
    create_url_name = "product:warranty_create"
    edit_url_name = "product:warranty_update"
    delete_url_name = "product:warranty_delete"
    create_label = "Warranty"
    search_includes_duration = True


class WarrantyCreateView(MasterCreateBaseView):
    form_class = WarrantyForm
    success_url = reverse_lazy("product:warranty_list")
    object_label = "Warranty"


class WarrantyUpdateView(MasterUpdateBaseView):
    model = Warranty
    form_class = WarrantyForm
    success_url = reverse_lazy("product:warranty_list")
    object_label = "Warranty"


class WarrantyDeleteView(BaseNoTemplateDeleteView):
    model = Warranty
    success_url = reverse_lazy("product:warranty_list")
    success_message = "Warranty deleted successfully."


class VatRateListView(MasterListBaseView):
    model = VatRate
    page_title = "VAT Rates"
    page_subtitle = "Manage VAT models and rates"
    list_url_name = "product:vat_rate_list"
    create_url_name = "product:vat_rate_create"
    edit_url_name = "product:vat_rate_update"
    delete_url_name = "product:vat_rate_delete"
    create_label = "VAT Rate"


class VatRateCreateView(MasterCreateBaseView):
    form_class = VatRateForm
    success_url = reverse_lazy("product:vat_rate_list")
    object_label = "VAT Rate"


class VatRateUpdateView(MasterUpdateBaseView):
    model = VatRate
    form_class = VatRateForm
    success_url = reverse_lazy("product:vat_rate_list")
    object_label = "VAT Rate"


class VatRateDeleteView(BaseNoTemplateDeleteView):
    model = VatRate
    success_url = reverse_lazy("product:vat_rate_list")
    success_message = "VAT Rate deleted successfully."


# ---------------- RELATED MODAL ----------------

# @login_required
# @require_http_methods(["GET", "POST"])
# def related_object_modal(request, model_name, pk=None):
#     model_name = (model_name or "").lower().strip()

#     MODEL_CONFIG = {
#         "unit": {"model": Unit, "form": UnitForm},
#         "category": {"model": Category, "form": CategoryForm},
#         "brand": {"model": Brand, "form": BrandForm},
#         "warranty": {"model": Warranty, "form": WarrantyForm},
#         "unick": {"model": unick, "form": UnickForm},
#         "branch": {"model": Branch, "form": BranchQuickForm},
#     }

#     config = MODEL_CONFIG.get(model_name)
#     if not config:
#         return HttpResponse("Invalid model", status=400)

#     model_cls = config["model"]
#     form_cls = config["form"]
#     instance = get_object_or_404(model_cls, pk=pk) if pk else None
#     parent_field = request.GET.get("parent_field") or request.POST.get("_parent_field", "")

#     if request.method == "POST":
#         try:
#             form = form_cls(request.POST, instance=instance, request=request)
#         except TypeError:
#             form = form_cls(request.POST, instance=instance)

#         if form.is_valid():
#             obj = form.save()

#             action_label = "Updated" if instance else "Created"
#             log_activity(request, "update" if instance else "create", f"{action_label} {obj}")

#             # HTMX / AJAX হলে সবসময় trigger পাঠাও
#             if request.headers.get("HX-Request") == "true" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
#                 return htmx_trigger_response({
#                     "related:saved": {
#                         "parentField": parent_field,
#                         "option": {
#                             "id": obj.pk,
#                             "text": str(obj),
#                         },
#                         "message": f"{action_label} successfully.",
#                     }
#                 })

#             messages.success(request, f"{action_label} successfully.")
#             return redirect("product:product_list")
#     else:
#         try:
#             form = form_cls(instance=instance, request=request)
#         except TypeError:
#             form = form_cls(instance=instance)

#     return render(request, "common/related_modal_form.html", {
#         "form": form,
#         "title": f"{'Update' if instance else 'Create'} {model_name.title()}",
#         "instance": instance,
#         "model_name": model_name,
#         "parent_field": parent_field,
#         "post_url": request.path,
#         "form_partial_template": "user/model_form.html",
#     })



# @login_required
# @require_http_methods(["GET", "POST"])
# def related_object_modal(request, model_name, pk=None):
#     model_name = (model_name or "").lower().strip()

#     MODEL_CONFIG = {
#         # "supplier": {
#         #     "model": Supplier,
#         #     "form": SupplierForm,
#         # },
#         "variation": {"model": Variation, "form": VariationQuickForm},
#         "product": {
#             "model": Product,
#             "form": ProductForm,
#         },
#         "variation": {
#             "model": Variation,
#             "form": VariationForm,
#         },
#         "unick": {
#             "model": unick,
#             "form": UnickForm,
#         },
#         "unit": {"model": Unit, "form": UnitForm},
#         "category": {"model": Category, "form": CategoryForm},
#         "brand": {"model": Brand, "form": BrandForm},
#         "warranty": {"model": Warranty, "form": WarrantyForm},
#         "unick": {"model": unick, "form": UnickForm},
#         "branch": {"model": Branch, "form": BranchQuickForm},
#         "user": {
#             "model": Users,
#             "form": None,  # user app-er quick form use korle import dite hobe
#         },
#     }

#     if model_name not in MODEL_CONFIG:
#         return HttpResponse("Invalid related model.", status=400)

#     config = MODEL_CONFIG[model_name]
#     model_class = config["model"]
#     form_class = config["form"]

#     if form_class is None:
#         return HttpResponse(f"{model_name} modal form not configured yet.", status=400)

#     instance = get_object_or_404(model_class, pk=pk) if pk else None
#     parent_field = request.GET.get("parent_field") or request.POST.get("_parent_field", "")

#     if request.method == "POST":
#         form = form_class(request.POST, instance=instance)
#         if form.is_valid():
#             obj = form.save()
#             return htmx_trigger_response({
#                 "related:saved": {
#                     "parentField": parent_field,
#                     "option": {
#                         "id": obj.pk,
#                         "text": str(obj),
#                     },
#                     "message": f"{model_name.title()} saved successfully."
#                 }
#             })
#     else:
#         try:
#             form = form_class(instance=instance, request=request)
#         except TypeError:
#             form = form_class(instance=instance)

#     return render(request, "common/related_modal_form.html", {
#         "form": form,
#         "title": f"{'Update' if instance else 'Create'} {model_name.title()}",
#         "instance": instance,
#         "model_name": model_name,
#         "parent_field": parent_field,
#         "post_url": request.path,
#         "form_partial_template": "user/model_form.html",
#     })



@login_required
@require_http_methods(["GET", "POST"])
def related_object_modal(request, model_name, pk=None):
    model_name = (model_name or "").lower().strip()

    MODEL_CONFIG = {
        "product": {"model": Product, "form": ProductForm},
        "variation": {"model": Variation, "form": VariationQuickForm},
        "unick": {"model": unick, "form": UnickForm},
        "supplier": {"model": Supplier, "form": SupplierForm},
        "unit": {"model": Unit, "form": UnitForm},
        "category": {"model": Category, "form": CategoryForm},
        "subcategory": {"model": SubCategory, "form": SubCategoryForm},
        "vat_rate": {"model": VatRate, "form": VatRateForm},
        "variation_attribute": {"model": VariationAttribute, "form": VariationAttributeForm},
        "variation_attribute_value": {"model": VariationAttributeValue, "form": VariationAttributeValueForm},
        "brand": {"model": Brand, "form": BrandForm},
        "warranty": {"model": Warranty, "form": WarrantyForm},
        "branch": {"model": Branch, "form": BranchQuickForm},
    }

    if model_name not in MODEL_CONFIG:
        return HttpResponse("Invalid related model.", status=400)

    config = MODEL_CONFIG[model_name]
    model_class = config["model"]
    form_class = config["form"]

    instance = get_object_or_404(model_class, pk=pk) if pk else None
    parent_field = request.GET.get("parent_field") or request.POST.get("_parent_field", "")
    category_id = request.GET.get("category_id", "").strip() or request.POST.get("category", "").strip()
    attribute_id = request.GET.get("attribute_id", "").strip() or request.POST.get("attribute", "").strip()

    if request.method == "POST":
        try:
            form = form_class(request.POST, request.FILES, instance=instance, request=request)
        except TypeError:
            try:
                form = form_class(request.POST, request.FILES, instance=instance)
            except TypeError:
                form = form_class(request.POST, instance=instance)

        if form.is_valid():
            changes = build_form_changes(form) if instance else {}
            obj = form.save()

            action = "update" if instance else "create"
            action_text = "Updated" if instance else "Created"
            log_activity(
                request,
                action,
                f"{action_text} {obj}",
                obj=obj,
                changes=changes,
            )

            return htmx_trigger_response({
                "related:saved": {
                    "parentField": parent_field,
                    "option": {
                        "id": obj.pk,
                        "text": str(obj),
                    },
                    "message": f"{model_name.title()} saved successfully."
                }
            })
    else:
        initial = None
        if model_name == "subcategory" and category_id and not instance:
            initial = {"category": category_id}
        if model_name == "variation_attribute_value" and attribute_id and not instance:
            initial = {"attribute": attribute_id}

        try:
            form = form_class(instance=instance, request=request, initial=initial)
        except TypeError:
            form = form_class(instance=instance, initial=initial)

    return render(request, "common/related_modal_form.html", {
        "form": form,
        "title": f"{'Update' if instance else 'Create'} {model_name.title()}",
        "instance": instance,
        "model_name": model_name,
        "parent_field": parent_field,
        "post_url": request.path,
        "form_partial_template": "user/model_form.html",
    })


@login_required
@require_GET
def ajax_subcategories_by_category(request):
    category_id = request.GET.get("category_id", "").strip()
    qs = SubCategory.objects.select_related("category").order_by("category__name", "name")

    if category_id:
        qs = qs.filter(category_id=category_id)

    return JsonResponse({
        "results": [{"id": obj.pk, "text": obj.name} for obj in qs]
    })


@login_required
@require_GET
def ajax_attribute_values_by_attribute(request):
    attribute_id = request.GET.get("attribute_id", "").strip()
    qs = VariationAttributeValue.objects.select_related("attribute").order_by("attribute__order", "order", "value")

    if attribute_id:
        qs = qs.filter(attribute_id=attribute_id)

    return JsonResponse({
        "results": [
            {
                "id": obj.pk,
                "text": obj.value,
                "code": obj.value_code or "",
                "attribute": obj.attribute.name,
            }
            for obj in qs
        ]
    })


@login_required
@require_GET
def ajax_vat_rate_detail(request):
    vat_id = request.GET.get("vat_id", "").strip()
    if not vat_id:
        return JsonResponse({
            "id": "",
            "rate_percent": "0",
            "tax_type": "exclusive",
        })

    vat = VatRate.objects.filter(pk=vat_id).first()
    if not vat:
        return JsonResponse({
            "id": "",
            "rate_percent": "0",
            "tax_type": "exclusive",
        })

    return JsonResponse({
        "id": vat.pk,
        "rate_percent": str(vat.rate_percent),
        "tax_type": vat.tax_type,
    })



# optional helper for variation filter by product
@login_required
@require_GET
def ajax_variations_by_product(request):
    product_id = request.GET.get("product_id", "").strip()
    qs = Variation.objects.select_related("product_name").all().order_by("name", "id")

    scope = get_user_scope(request.user)
    allowed_branch_ids = list(scope["branches"].values_list("id", flat=True))
    if not is_global_user(request.user):
        if allowed_branch_ids:
            scoped_qs = qs.filter(branch_stocks__stock_branch_id__in=allowed_branch_ids).distinct()
            # Fallback: if no branch-stock mapped variation exists, keep unscoped variations
            # so purchase row variation selection still works.
            if scoped_qs.exists():
                qs = scoped_qs
        else:
            qs = qs.none()

    if product_id:
        qs = qs.filter(product_name_id=product_id)

    return JsonResponse({
        "results": [
            {
                "id": obj.pk,
                "text": str(obj),
                "name": obj.name,
                "sku": f"{obj.product_name.sku}-{obj.sku_suffix}" if obj.sku_suffix else obj.product_name.sku,
                "purchase_price_exc_tax": float(obj.purchase_price_exc_tax or 0),
                "purchase_price_inc_tax": float(obj.purchase_price_inc_tax or 0),
                "margin_percent": float(obj.margin_percent or 0),
                "selling_price_inc_tax": float(obj.selling_price_inc_tax or 0),
                "applicable_tax_percent": float(obj.applicable_tax_percent or 0),
                "qty": int(obj.quantity or 0),
                "imei_enabled": bool(obj.isunck or (obj.product_name and obj.product_name.enable_imei_or_serial)),
            }
            for obj in qs
        ]
    })


@login_required
@require_GET
def ajax_unick_by_variation(request):
    variation_id = request.GET.get("variation_id", "").strip()
    qs = unick.objects.none()

    if variation_id:
        variation_qs = Variation.objects.filter(pk=variation_id)
        scope = get_user_scope(request.user)
        allowed_branch_ids = list(scope["branches"].values_list("id", flat=True))
        if not is_global_user(request.user):
            if allowed_branch_ids:
                variation_qs = variation_qs.filter(branch_stocks__stock_branch_id__in=allowed_branch_ids)
            else:
                variation_qs = Variation.objects.none()

        variation = variation_qs.prefetch_related("unickkey").first()
        if variation:
            qs = variation.unickkey.all().order_by("id")

    return JsonResponse({
        "results": [{"id": obj.pk, "text": str(obj)} for obj in qs]
    })


@login_required
@require_http_methods(["POST"])
def ajax_resolve_unick_from_scanner(request):
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({
            "results": [],
            "unmatched": [],
            "error": "Invalid JSON payload.",
        }, status=400)

    raw_tokens = payload.get("tokens", [])
    create_missing = bool(payload.get("create_missing", True))

    if isinstance(raw_tokens, str):
        raw_tokens = [chunk.strip() for chunk in raw_tokens.replace("\r", "\n").replace(",", "\n").split("\n")]
    elif not isinstance(raw_tokens, list):
        raw_tokens = []

    distinct_tokens = []
    seen_tokens = set()
    for token in raw_tokens[:300]:
        cleaned = str(token or "").strip()
        if not cleaned:
            continue
        fingerprint = cleaned.lower()
        if fingerprint in seen_tokens:
            continue
        seen_tokens.add(fingerprint)
        distinct_tokens.append(cleaned)

    resolved = []
    unmatched = []
    seen_ids = set()

    for token in distinct_tokens:
        matched_obj = unick.objects.filter(
            Q(key1__iexact=token) | Q(key2__iexact=token)
        ).order_by("id").first()

        if not matched_obj and create_missing:
            if len(token) > 100:
                unmatched.append(token)
                continue

            try:
                matched_obj = unick.objects.create(key1=token)
            except IntegrityError:
                matched_obj = unick.objects.filter(
                    Q(key1__iexact=token) | Q(key2__iexact=token)
                ).order_by("id").first()

        if not matched_obj:
            unmatched.append(token)
            continue

        if matched_obj.pk in seen_ids:
            continue
        seen_ids.add(matched_obj.pk)
        resolved.append({
            "id": matched_obj.pk,
            "text": str(matched_obj),
            "key1": matched_obj.key1,
            "key2": matched_obj.key2 or "",
        })

    return JsonResponse({
        "results": resolved,
        "unmatched": unmatched,
    })


@login_required
@require_GET
def ajax_search_purchase_products(request):
    """Search products and variation details for purchase UI."""
    query = request.GET.get("q", "").strip()

    qs = Product.objects.select_related(
        "unit_name", "category_name", "subcategory_name", "brand_name", "vat_rate"
    ).prefetch_related("variations").order_by("name", "id")

    scope = get_user_scope(request.user)
    allowed_branch_ids = list(scope["branches"].values_list("id", flat=True))
    if not is_global_user(request.user):
        if allowed_branch_ids:
            scoped_qs = qs.filter(
                Q(branch_product_stocks__stock_branch_id__in=allowed_branch_ids)
            ).distinct()
            # Fallback: if branch stock table is not populated yet, still allow searching
            # products for purchase entry.
            if scoped_qs.exists():
                qs = scoped_qs
        else:
            qs = qs.none()

    if query:
        qs = qs.filter(
            Q(name__icontains=query)
            | Q(sku__icontains=query)
            | Q(variations__name__icontains=query)
            | Q(variations__sku_suffix__icontains=query)
            | Q(category_name__name__icontains=query)
        ).distinct()

    results = []
    for product in qs[:50]:
        variations_data = []
        for variation in product.variations.all():
            variations_data.append(
                {
                    "id": variation.pk,
                    "name": variation.name,
                    "text": f"{variation.name} ({f'{product.sku}-{variation.sku_suffix}' if variation.sku_suffix else product.sku})",
                    "sku": f"{product.sku}-{variation.sku_suffix}" if variation.sku_suffix else product.sku,
                    "purchase_price_exc_tax": float(variation.purchase_price_exc_tax or 0),
                    "purchase_price_inc_tax": float(variation.purchase_price_inc_tax or 0),
                    "margin_percent": float(variation.margin_percent or 0),
                    "selling_price_exc_tax": float(variation.price or 0),
                    "selling_price_inc_tax": float(variation.selling_price_inc_tax or 0),
                    "selling_price_tax_type": variation.selling_price_tax_type or "exclusive",
                    "applicable_tax_percent": float(variation.applicable_tax_percent or 0),
                    "qty": int(variation.quantity or 0),
                    "imei_enabled": bool(variation.isunck or product.enable_imei_or_serial),
                }
            )

        results.append(
            {
                "id": product.pk,
                "name": product.name,
                "sku": product.sku,
                "category": product.category_name.name if product.category_name else "",
                "subcategory": product.subcategory_name.name if product.subcategory_name else "",
                "brand": product.brand_name.name if product.brand_name else "",
                "unit": product.unit_name.name if product.unit_name else "",
                "vat_rate": float(product.vat_rate.rate_percent) if product.vat_rate else 0,
                "vat_tax_type": product.vat_rate.tax_type if product.vat_rate else "exclusive",
                "default_purchase_price_exc_tax": float(product.default_purchase_price_exc_tax or 0),
                "default_purchase_price_inc_tax": float(product.default_purchase_price_inc_tax or 0),
                "default_selling_price": float(product.default_selling_price or 0),
                "manage_stock": bool(product.manage_stock),
                "enable_imei_or_serial": bool(product.enable_imei_or_serial),
                "variations": variations_data,
            }
        )

    return JsonResponse({"results": results})