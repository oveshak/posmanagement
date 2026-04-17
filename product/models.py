from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum
from simple_history.models import HistoricalRecords

from globalapp.models import Common
from user.models import Branch, Users



# =========================
# BASIC / MASTER MODELS
# =========================

class Unit(Common):
    name = models.CharField(max_length=50, verbose_name="Unit Name")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Unit"
        verbose_name_plural = "Units"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(Common):
    name = models.CharField(max_length=100, verbose_name="Category Name")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Brand(Common):
    name = models.CharField(max_length=100, verbose_name="Brand Name")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Warranty(Common):
    DURATION_TYPES = (
        ("Days", "Days"),
        ("Months", "Months"),
        ("Years", "Years"),
    )

    name = models.CharField(max_length=100, verbose_name="Warranty Name")
    duration = models.IntegerField(verbose_name="Duration")
    duration_type = models.CharField(
        max_length=10,
        choices=DURATION_TYPES,
        verbose_name="Duration Type"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Warranty"
        verbose_name_plural = "Warranties"
        ordering = ["name"]

    def __str__(self):
        return self.name


# =========================
# PRODUCT
# =========================

class Product(Common):
    name = models.CharField(max_length=200, verbose_name="Product Name")
    sku = models.CharField(max_length=50, unique=True, verbose_name="Product SKU")

    unit_name = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Unit Name"
    )
    category_name = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Product Category"
    )
    brand_name = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Product Brand"
    )
    warranty_name = models.ForeignKey(
        Warranty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Product Warranty"
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name"]

    def __str__(self):
        return self.name


class VariationAttribute(Common):
    name = models.CharField(max_length=50, unique=True, verbose_name="Attribute Name")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Variation Attribute"
        verbose_name_plural = "Variation Attributes"
        ordering = ["order"]

    def __str__(self):
        return self.name


class unick(Common):
    key1 = models.CharField(max_length=100, unique=True, verbose_name="IMI-1")
    key2 = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="IMI-2")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Unique Key"
        verbose_name_plural = "Unique Keys"
        ordering = ["id"]

    def __str__(self):
        return f"{self.key1} - {self.key2 or ''}"


class Variation(Common):
    product_name = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variations",
        verbose_name="Product Name"
    )
    name = models.CharField(max_length=300, blank=True, verbose_name="Variation Name")
    sku_suffix = models.CharField(max_length=50, blank=True, verbose_name="SKU Suffix")

    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Sales Price")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantity")
    dealer_price = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Dealer Price")

    isunck = models.BooleanField(default=False, verbose_name="Has Unique Key")
    unickkey = models.ManyToManyField(
        unick,
        blank=True,
        related_name="variations",
        verbose_name="Unique Keys"
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Variation"
        verbose_name_plural = "Variations"
        ordering = ["id"]

    def __str__(self):
        return f"{self.product_name.name} - {self.name}"


# =========================
# STOCK
# =========================

class BranchProductStock(Common):
    product_name = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="branch_product_stocks",
        verbose_name="Product Name"
    )
    product_variation = models.ForeignKey(
        Variation,
        on_delete=models.CASCADE,
        related_name="branch_stocks",
        verbose_name="Product Variation"
    )
    stock_branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="branch_product_stocks",
        verbose_name="Stock Branch"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantity")
    unickkey = models.ManyToManyField(
        unick,
        blank=True,
        related_name="branch_product_stocks",
        verbose_name="Unique Keys"
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Branch Product Stock"
        verbose_name_plural = "Branch Product Stocks"
        ordering = ["id"]
        unique_together = ("product_variation", "stock_branch")

    def clean(self):
        if self.product_variation_id and self.product_name_id:
            if self.product_variation.product_name_id != self.product_name_id:
                raise ValidationError({
                    "product_variation": "Variation does not belong to product"
                })

        if self.product_variation_id:
            total = BranchProductStock.objects.filter(
                product_variation=self.product_variation
            ).exclude(pk=self.pk).aggregate(t=Sum("quantity"))["t"] or 0

            if total + (self.quantity or 0) > self.product_variation.quantity:
                raise ValidationError({
                    "quantity": "Branch stock exceeds variation stock"
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} - {self.product_variation} ({self.stock_branch})"


# =========================
# PURCHASE
# =========================
class Supplier(Common):
    name = models.CharField(max_length=200, verbose_name="Supplier Name")
    contact_number = models.CharField(max_length=20, blank=True, verbose_name="Contact Number")
    email = models.EmailField(blank=True, verbose_name="Email")
    address = models.TextField(blank=True, verbose_name="Address")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        ordering = ["name"]

    def __str__(self):
        return self.name

class PurchaseItem(Common):
    purchase_product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Product"
    )
    purchase_product_variation = models.ForeignKey(
        Variation,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Variation"
    )
    unickkey = models.ManyToManyField(
        unick,
        blank=True,
        verbose_name="Unique Identifiers"
    )
    qty = models.PositiveIntegerField(verbose_name="Quantity")
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Unit Price",
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Purchase Item"
        verbose_name_plural = "Purchase Items"
        ordering = ["-id"]

    def clean(self):
        if self.purchase_product_variation_id and self.purchase_product_id:
            if self.purchase_product_variation.product_name_id != self.purchase_product_id:
                raise ValidationError({
                    "purchase_product_variation": "Variation does not belong to selected product."
                })

        if self.qty <= 0:
            raise ValidationError({"qty": "Quantity must be greater than 0."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.purchase_product} - {self.purchase_product_variation} ({self.qty})"


class Purchase(Common):
    supplier_name = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        related_name="purchases",
        verbose_name="Supplier"
    )
    purchaseitem = models.ManyToManyField(
        PurchaseItem,
        blank=True,
        verbose_name="Purchase Items"
    )
    purchase_date = models.DateField(verbose_name="Purchase Date")
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Total Amount")
    purchase_status = models.CharField(max_length=20, verbose_name="Purchase Status")
    vendor_cheque_details = models.TextField(blank=True, null=True, verbose_name="Vendor Cheque Details")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"
        ordering = ["-purchase_date"]

    def __str__(self):
        return f"Purchase #{self.id} - {self.supplier_name}"


class PurchaseReturn(Common):
    purchase_name = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="returns",
        verbose_name="Purchase"
    )
    return_date = models.DateField(verbose_name="Return Date")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Purchase Return"
        verbose_name_plural = "Purchase Returns"
        ordering = ["-return_date"]

    def __str__(self):
        return f"Return - {self.purchase_name}"


# =========================
# STOCK TRANSFER
# =========================

class StockTransfer(Common):
    from_branch_name = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="sent_transfers",
        verbose_name="From Branch"
    )
    to_branch_name = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="received_transfers",
        verbose_name="To Branch"
    )
    transfer_date = models.DateField(verbose_name="Transfer Date")
    stc_status = models.CharField(max_length=20, default="draft", verbose_name="Status")
    is_applied = models.BooleanField(default=False, editable=False)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Stock Transfer"
        verbose_name_plural = "Stock Transfers"
        ordering = ["-transfer_date", "-id"]

    def clean(self):
        if self.from_branch_name_id and self.to_branch_name_id:
            if self.from_branch_name_id == self.to_branch_name_id:
                raise ValidationError("From branch এবং To branch একই হতে পারবে না।")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.from_branch_name} → {self.to_branch_name} ({self.transfer_date})"


class StockTransferLine(models.Model):
    transfer = models.ForeignKey(
        StockTransfer,
        on_delete=models.CASCADE,
        related_name="lines"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    unickkeys = models.ManyToManyField(unick, blank=True)

    class Meta:
        verbose_name = "Stock Transfer Line"
        verbose_name_plural = "Stock Transfer Lines"
        ordering = ["-id"]

    def clean(self):
        if self.variation_id and self.product_id:
            if self.variation.product_name_id != self.product_id:
                raise ValidationError({
                    "variation": "Variation does not belong to product"
                })
        if self.quantity <= 0:
            raise ValidationError({
                "quantity": "Quantity must be > 0"
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} / {self.variation} x {self.quantity}"


# =========================
# STOCK ADJUSTMENT
# =========================

class StockAdjustment(Common):
    branch_name = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name="Branch"
    )
    product_name = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Product"
    )
    quantity_adjusted = models.IntegerField(verbose_name="Quantity Adjusted")
    reason = models.TextField(verbose_name="Reason")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Stock Adjustment"
        verbose_name_plural = "Stock Adjustments"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.product_name} ({self.quantity_adjusted})"


# =========================
# VENDOR CHEQUE
# =========================

class VendorCheque(Common):
    cheque_number = models.CharField(max_length=100, verbose_name="Cheque Number")
    vendor_name = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Vendor Name"
    )
    issue_date = models.DateField(verbose_name="Issue Date")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Amount")
    vndcq_status = models.CharField(max_length=20, verbose_name="Status")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Vendor Cheque"
        verbose_name_plural = "Vendor Cheques"
        ordering = ["-issue_date"]

    def __str__(self):
        return f"{self.cheque_number} - {self.vendor_name}"


# =========================
# REPAIR REQUEST
# =========================

class RepairRequest(Common):
    product_name = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Product"
    )
    customer_name = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Customer Name"
    )
    branch_name = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name="Branch"
    )
    requested_by_user_name = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Requested By"
    )
    request_date = models.DateField(verbose_name="Request Date")
    repair_status = models.CharField(max_length=20, verbose_name="Repair Status")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Repair Request"
        verbose_name_plural = "Repair Requests"
        ordering = ["-request_date"]

    def __str__(self):
        return f"{self.product_name} - {self.repair_status}"