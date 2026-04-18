# # from django.urls import path
# # from .views import (
# #     PurchaseListView, PurchaseCreateView, PurchaseUpdateView, PurchaseDeleteView, PurchaseItemQuickCreateView,
# #     PurchaseReturnListView, PurchaseReturnCreateView, PurchaseReturnUpdateView, PurchaseReturnDeleteView,
# #     StockTransferListView, StockTransferCreateView, StockTransferUpdateView, StockTransferDeleteView,
# #     StockAdjustmentListView, StockAdjustmentCreateView, StockAdjustmentUpdateView, StockAdjustmentDeleteView,
# #     VendorChequeListView, VendorChequeCreateView, VendorChequeUpdateView, VendorChequeDeleteView,
# #     RepairRequestListView, RepairRequestCreateView, RepairRequestUpdateView, RepairRequestDeleteView,
# # )
# # from .views import (
# #     ajax_variations_by_product,
# #     ajax_unick_by_variation,
# #     related_object_modal,
# # )

# # urlpatterns = [
# #     path("purchases/", PurchaseListView.as_view(), name="purchase_list"),
# #     path("purchases/create/", PurchaseCreateView.as_view(), name="purchase_create"),
# #     path("purchases/<int:pk>/edit/", PurchaseUpdateView.as_view(), name="purchase_update"),
# #     path("purchases/<int:pk>/delete/", PurchaseDeleteView.as_view(), name="purchase_delete"),
# #     path("purchases/items/create/", PurchaseItemQuickCreateView.as_view(), name="purchase_item_quick_create"),

# #     path("purchase-returns/", PurchaseReturnListView.as_view(), name="purchase_return_list"),
# #     path("purchase-returns/create/", PurchaseReturnCreateView.as_view(), name="purchase_return_create"),
# #     path("purchase-returns/<int:pk>/edit/", PurchaseReturnUpdateView.as_view(), name="purchase_return_update"),
# #     path("purchase-returns/<int:pk>/delete/", PurchaseReturnDeleteView.as_view(), name="purchase_return_delete"),

# #     path("stock-transfers/", StockTransferListView.as_view(), name="stock_transfer_list"),
# #     path("stock-transfers/create/", StockTransferCreateView.as_view(), name="stock_transfer_create"),
# #     path("stock-transfers/<int:pk>/edit/", StockTransferUpdateView.as_view(), name="stock_transfer_update"),
# #     path("stock-transfers/<int:pk>/delete/", StockTransferDeleteView.as_view(), name="stock_transfer_delete"),

# #     path("stock-adjustments/", StockAdjustmentListView.as_view(), name="stock_adjustment_list"),
# #     path("stock-adjustments/create/", StockAdjustmentCreateView.as_view(), name="stock_adjustment_create"),
# #     path("stock-adjustments/<int:pk>/edit/", StockAdjustmentUpdateView.as_view(), name="stock_adjustment_update"),
# #     path("stock-adjustments/<int:pk>/delete/", StockAdjustmentDeleteView.as_view(), name="stock_adjustment_delete"),

# #     path("vendor-cheques/", VendorChequeListView.as_view(), name="vendor_cheque_list"),
# #     path("vendor-cheques/create/", VendorChequeCreateView.as_view(), name="vendor_cheque_create"),
# #     path("vendor-cheques/<int:pk>/edit/", VendorChequeUpdateView.as_view(), name="vendor_cheque_update"),
# #     path("vendor-cheques/<int:pk>/delete/", VendorChequeDeleteView.as_view(), name="vendor_cheque_delete"),

# #     path("repair-requests/", RepairRequestListView.as_view(), name="repair_request_list"),
# #     path("repair-requests/create/", RepairRequestCreateView.as_view(), name="repair_request_create"),
# #     path("repair-requests/<int:pk>/edit/", RepairRequestUpdateView.as_view(), name="repair_request_update"),
# #     path("repair-requests/<int:pk>/delete/", RepairRequestDeleteView.as_view(), name="repair_request_delete"),


# #     path("ajax/options/variations/", ajax_variations_by_product, name="ajax_variations_by_product"),
# #     path("ajax/options/unick/", ajax_unick_by_variation, name="ajax_unick_by_variation"),

# #     path("ajax/related/<str:model_name>/create/", related_object_modal, name="related_object_create"),
# #     path("ajax/related/<str:model_name>/<int:pk>/edit/", related_object_modal, name="related_object_edit"),
# # ]


# from django.urls import path
# from .views import (
#     ProductListView,
#     ProductCreateView,
#     ProductUpdateView,
#     ProductDeleteView,
#     related_object_modals,
# )

# urlpatterns = [
#     path("products/", ProductListView.as_view(), name="product_list"),
#     path("products/create/", ProductCreateView.as_view(), name="product_create"),
#     path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_update"),
#     path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),

#     path("ajax/related/<str:model_name>/create/", related_object_modals, name="related_object_create"),
#     path("ajax/related/<str:model_name>/<int:pk>/edit/", related_object_modals, name="related_object_edit"),
# ]


from django.urls import path
from .views import (
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    UnitListView,
    UnitCreateView,
    UnitUpdateView,
    UnitDeleteView,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    BrandListView,
    BrandCreateView,
    BrandUpdateView,
    BrandDeleteView,
    WarrantyListView,
    WarrantyCreateView,
    WarrantyUpdateView,
    WarrantyDeleteView,
    BranchStockListView,
    BranchStockCreateView,
    BranchStockUpdateView,
    BranchStockDeleteView,
    related_object_modal,
    ajax_variations_by_product,
    ajax_unick_by_variation,
)
app_name = "product"
urlpatterns = [
    path("units/", UnitListView.as_view(), name="unit_list"),
    path("units/create/", UnitCreateView.as_view(), name="unit_create"),
    path("units/<int:pk>/edit/", UnitUpdateView.as_view(), name="unit_update"),
    path("units/<int:pk>/delete/", UnitDeleteView.as_view(), name="unit_delete"),

    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/create/", CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category_update"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category_delete"),

    path("brands/", BrandListView.as_view(), name="brand_list"),
    path("brands/create/", BrandCreateView.as_view(), name="brand_create"),
    path("brands/<int:pk>/edit/", BrandUpdateView.as_view(), name="brand_update"),
    path("brands/<int:pk>/delete/", BrandDeleteView.as_view(), name="brand_delete"),

    path("warranties/", WarrantyListView.as_view(), name="warranty_list"),
    path("warranties/create/", WarrantyCreateView.as_view(), name="warranty_create"),
    path("warranties/<int:pk>/edit/", WarrantyUpdateView.as_view(), name="warranty_update"),
    path("warranties/<int:pk>/delete/", WarrantyDeleteView.as_view(), name="warranty_delete"),

    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),

    path("branch-stocks/", BranchStockListView.as_view(), name="branch_stock_list"),
    path("branch-stocks/create/", BranchStockCreateView.as_view(), name="branch_stock_create"),
    path("branch-stocks/<int:pk>/edit/", BranchStockUpdateView.as_view(), name="branch_stock_update"),
    path("branch-stocks/<int:pk>/delete/", BranchStockDeleteView.as_view(), name="branch_stock_delete"),

    path("ajax/related/<str:model_name>/create/", related_object_modal, name="related_object_create"),
    path("ajax/related/<str:model_name>/<int:pk>/edit/", related_object_modal, name="related_object_edit"),
    path("ajax/options/variations/", ajax_variations_by_product, name="ajax_variations_by_product"),
    path("ajax/options/unick/", ajax_unick_by_variation, name="ajax_unick_by_variation"),
]