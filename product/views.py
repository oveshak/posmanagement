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
# #     PurchaseReturnForm,
# #     StockTransferForm,
# #     StockTransferLineFormSet,
# #     StockAdjustmentForm,
# #     VendorChequeForm,
# #     RepairRequestForm,
# # )
# # from .models import (
# #     Product,
# #     Variation,
# #     unick,
# #     PurchaseItem,
# #     Purchase,
# #     PurchaseReturn,
# #     StockTransfer,
# #     StockTransferLine,
# #     StockAdjustment,
# #     VendorCheque,
# #     RepairRequest,
# # )


# # class HtmxListMixin:
# #     partial_template_name = None

# #     def get_template_names(self):
# #         if self.request.headers.get("HX-Request") == "true" and self.partial_template_name:
# #             return [self.partial_template_name]
# #         return [self.template_name]


# # class BaseNoTemplateDeleteView(LoginRequiredMixin, View):
# #     model = None
# #     success_url = None
# #     success_message = "Deleted successfully."

# #     def post(self, request, pk, *args, **kwargs):
# #         obj = get_object_or_404(self.model, pk=pk)
# #         label = str(obj)
# #         obj.delete()

# #         log_activity(request, "delete", f"Deleted {label}")
# #         messages.success(request, self.success_message)

# #         if is_htmx(request):
# #             return htmx_trigger_response({
# #                 "crud:deleted": {
# #                     "message": self.success_message,
# #                     "refreshList": True,
# #                 }
# #             })

# #         return redirect(self.success_url)


# # # ---------------- PURCHASE ----------------

# # class PurchaseListView(LoginRequiredMixin, HtmxListMixin, ListView):
# #     model = Purchase
# #     template_name = "products/purchase_list.html"
# #     partial_template_name = "products/partials/purchase_list_content.html"
# #     context_object_name = "purchases"
# #     paginate_by = 20

# #     def get_queryset(self):
# #         qs = Purchase.objects.select_related("supplier_name").prefetch_related("purchaseitem").order_by("-purchase_date", "-id")
# #         search = self.request.GET.get("search", "").strip()
# #         status = self.request.GET.get("purchase_status", "").strip()

# #         if search:
# #             qs = qs.filter(
# #                 Q(supplier_name__name__icontains=search) |
# #                 Q(vendor_cheque_details__icontains=search)
# #             )
# #         if status:
# #             qs = qs.filter(purchase_status__icontains=status)

# #         return qs

# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         context["selected_search"] = self.request.GET.get("search", "").strip()
# #         context["selected_status"] = self.request.GET.get("purchase_status", "").strip()
# #         return context


# # class PurchaseCreateView(LoginRequiredMixin, View):
# #     template_name = "products/purchase_form.html"
# #     success_url = reverse_lazy("purchase_list")

# #     def get(self, request, *args, **kwargs):
# #         context = {
# #             "form": PurchaseForm(),
# #             "item_form": PurchaseItemForm(),
# #             "items": [],
# #             "object": None,
# #         }
# #         return render(request, self.template_name, context)

# #     @transaction.atomic
# #     def post(self, request, *args, **kwargs):
# #         form = PurchaseForm(request.POST)
# #         item_ids = request.POST.getlist("purchaseitem_ids")
# #         items = PurchaseItem.objects.filter(id__in=item_ids)

# #         if form.is_valid():
# #             purchase = form.save()
# #             purchase.purchaseitem.set(items)

# #             total = sum([(item.unit_price or Decimal("0")) * item.qty for item in items], Decimal("0"))
# #             purchase.total_amount = total
# #             purchase.save(update_fields=["total_amount"])

# #             log_activity(request, "create", f"Created purchase #{purchase.id}")
# #             messages.success(request, "Purchase created successfully.")
# #             return redirect(self.success_url)

# #         context = {
# #             "form": form,
# #             "item_form": PurchaseItemForm(),
# #             "items": items,
# #             "object": None,
# #         }
# #         return render(request, self.template_name, context)


# # class PurchaseUpdateView(LoginRequiredMixin, View):
# #     template_name = "products/purchase_form.html"
# #     success_url = reverse_lazy("purchase_list")

# #     def get_object(self, pk):
# #         return get_object_or_404(Purchase.objects.prefetch_related("purchaseitem"), pk=pk)

# #     def get(self, request, pk, *args, **kwargs):
# #         obj = self.get_object(pk)
# #         context = {
# #             "form": PurchaseForm(instance=obj),
# #             "item_form": PurchaseItemForm(),
# #             "items": obj.purchaseitem.all(),
# #             "object": obj,
# #         }
# #         return render(request, self.template_name, context)

# #     @transaction.atomic
# #     def post(self, request, pk, *args, **kwargs):
# #         obj = self.get_object(pk)
# #         form = PurchaseForm(request.POST, instance=obj)
# #         item_ids = request.POST.getlist("purchaseitem_ids")
# #         items = PurchaseItem.objects.filter(id__in=item_ids)

# #         if form.is_valid():
# #             purchase = form.save()
# #             purchase.purchaseitem.set(items)

# #             total = sum([(item.unit_price or Decimal("0")) * item.qty for item in items], Decimal("0"))
# #             purchase.total_amount = total
# #             purchase.save(update_fields=["total_amount"])

# #             log_activity(request, "update", f"Updated purchase #{purchase.id}")
# #             messages.success(request, "Purchase updated successfully.")
# #             return redirect(self.success_url)

# #         context = {
# #             "form": form,
# #             "item_form": PurchaseItemForm(),
# #             "items": items,
# #             "object": obj,
# #         }
# #         return render(request, self.template_name, context)


# # class PurchaseDeleteView(BaseNoTemplateDeleteView):
# #     model = Purchase
# #     success_url = reverse_lazy("purchase_list")
# #     success_message = "Purchase deleted successfully."


# # class PurchaseItemQuickCreateView(LoginRequiredMixin, View):
# #     template_name = "products/modals/purchase_item_form.html"

# #     def get(self, request, *args, **kwargs):
# #         return render(request, self.template_name, {"form": PurchaseItemForm(), "object": None})

# #     def post(self, request, *args, **kwargs):
# #         form = PurchaseItemForm(request.POST)
# #         if form.is_valid():
# #             obj = form.save()
# #             return htmx_trigger_response({
# #                 "purchase:item-saved": {
# #                     "id": obj.id,
# #                     "product": str(obj.purchase_product) if obj.purchase_product else "",
# #                     "variation": str(obj.purchase_product_variation) if obj.purchase_product_variation else "",
# #                     "qty": obj.qty,
# #                     "unit_price": str(obj.unit_price),
# #                     "message": "Purchase item saved successfully.",
# #                 }
# #             })
# #         return render(request, self.template_name, {"form": form, "object": None})


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



from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
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
    Brand,
    Warranty,
    Product,
    Variation,
    unick,
    BranchProductStock,
)
from .forms import (
    ProductForm,
    VariationForm,
    VariationFormSet,
    UnitForm,
    CategoryForm,
    BrandForm,
    VariationQuickForm,
    WarrantyForm,
    UnickForm,
    BranchProductStockForm,
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
            "unit_name", "category_name", "brand_name", "warranty_name"
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
        brand_id = self.request.GET.get("brand", "").strip()

        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(sku__icontains=search) |
                Q(category_name__name__icontains=search) |
                Q(brand_name__name__icontains=search)
            )

        if category_id:
            qs = qs.filter(category_name_id=category_id)

        if brand_id:
            qs = qs.filter(brand_name_id=brand_id)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_qs = self.get_queryset()
        context["categories"] = Category.objects.filter(products__in=base_qs).distinct().order_by("name")
        context["brands"] = Brand.objects.filter(products__in=base_qs).distinct().order_by("name")
        context["selected_search"] = self.request.GET.get("search", "").strip()
        context["selected_category"] = self.request.GET.get("category", "").strip()
        context["selected_brand"] = self.request.GET.get("brand", "").strip()
        return context


class ProductCreateView(LoginRequiredMixin, View):
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product:product_list")

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "form": ProductForm(),
            "formset": VariationFormSet(prefix="variations"),
            "object": None,
        })

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)
        formset = VariationFormSet(request.POST, prefix="variations")

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
            "form": ProductForm(instance=obj),
            "formset": VariationFormSet(instance=obj, prefix="variations"),
            "object": obj,
        })

    @transaction.atomic
    def post(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        form = ProductForm(request.POST, instance=obj)
        formset = VariationFormSet(request.POST, instance=obj, prefix="variations")

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
            "object": obj,
        })


class ProductDeleteView(BaseNoTemplateDeleteView):
    model = Product
    success_url = reverse_lazy("product:product_list")
    success_message = "Product deleted successfully."


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
        "unit": {"model": Unit, "form": UnitForm},
        "category": {"model": Category, "form": CategoryForm},
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
        try:
            form = form_class(instance=instance, request=request)
        except TypeError:
            form = form_class(instance=instance)

    return render(request, "common/related_modal_form.html", {
        "form": form,
        "title": f"{'Update' if instance else 'Create'} {model_name.title()}",
        "instance": instance,
        "model_name": model_name,
        "parent_field": parent_field,
        "post_url": request.path,
        "form_partial_template": "user/model_form.html",
    })



# optional helper for variation filter by product
@login_required
@require_GET
def ajax_variations_by_product(request):
    product_id = request.GET.get("product_id", "").strip()
    qs = Variation.objects.all().order_by("name", "id")

    scope = get_user_scope(request.user)
    allowed_branch_ids = list(scope["branches"].values_list("id", flat=True))
    if not is_global_user(request.user):
        if allowed_branch_ids:
            qs = qs.filter(branch_stocks__stock_branch_id__in=allowed_branch_ids)
        else:
            qs = qs.none()

    if product_id:
        qs = qs.filter(product_name_id=product_id)

    return JsonResponse({
        "results": [{"id": obj.pk, "text": str(obj)} for obj in qs]
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