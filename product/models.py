from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum
from decimal import Decimal
from simple_history.models import HistoricalRecords

from globalapp.models import Common
from user.models import Branch, Users


TAX_TYPES = (
    ("exclusive", "Exclusive"),
    ("inclusive", "Inclusive"),
)



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


class SubCategory(Common):
    name = models.CharField(max_length=100, verbose_name="Subcategory Name")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Category",
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"
        ordering = ["category__name", "name"]
        unique_together = [["category", "name"]]

    def __str__(self):
        return f"{self.category} / {self.name}"


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


class VatRate(Common):
    name = models.CharField(max_length=100, unique=True, verbose_name="VAT Name")
    rate_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="VAT Rate (%)")
    tax_type = models.CharField(
        max_length=20,
        choices=TAX_TYPES,
        default="exclusive",
        verbose_name="Tax Type",
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "VAT Rate"
        verbose_name_plural = "VAT Rates"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.rate_percent}%)"


# =========================
# PRODUCT
# =========================

class Product(Common):
    BARCODE_TYPES = (
        ("code128", "Code 128"),
        ("code39", "Code 39"),
        ("ean13", "EAN-13"),
        ("upc", "UPC"),
    )

    TAX_TYPES = TAX_TYPES

    PRODUCT_TYPES = (
        ("single", "Single"),
        ("variable", "Variation"),
        ("combo", "Combo"),
    )

    name = models.CharField(max_length=200, verbose_name="Product Name")
    sku = models.CharField(max_length=50, unique=True, verbose_name="Product SKU")
    barcode_type = models.CharField(
        max_length=20,
        choices=BARCODE_TYPES,
        default="code128",
        verbose_name="Barcode Type",
    )

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
    subcategory_name = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Product Subcategory"
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
    business_location = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products_business_location",
        verbose_name="Business Location",
    )
    manage_stock = models.BooleanField(default=False, verbose_name="Manage Stock")
    product_description = models.TextField(blank=True, null=True, verbose_name="Product Description")
    product_image = models.ImageField(upload_to="products/images/", blank=True, null=True, verbose_name="Product Image")
    product_brochure = models.FileField(upload_to="products/brochures/", blank=True, null=True, verbose_name="Product Brochure")

    enable_imei_or_serial = models.BooleanField(
        default=False,
        verbose_name="Enable Description, IMEI or Serial Number",
    )
    not_for_selling = models.BooleanField(default=False, verbose_name="Not For Selling")
    weight = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, verbose_name="Weight (kg)")
    service_time_minutes = models.PositiveIntegerField(blank=True, null=True, verbose_name="Service Staff Time (minutes)")
    disable_woocommerce_sync = models.BooleanField(default=False, verbose_name="Disable WooCommerce Sync")
    low_stock_alert_quantity = models.PositiveIntegerField(blank=True, null=True, verbose_name="Low Stock Alert Quantity")

    vat_rate = models.ForeignKey(
        VatRate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="VAT Rate",
    )

    applicable_tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Applicable Tax (%)")
    selling_price_tax_type = models.CharField(
        max_length=20,
        choices=TAX_TYPES,
        default="exclusive",
        verbose_name="Selling Price Tax Type",
    )
    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPES,
        default="single",
        verbose_name="Product Type",
    )
    default_purchase_price_exc_tax = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Default Purchase Price (Exc. Tax)",
    )
    default_purchase_price_inc_tax = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Default Purchase Price (Inc. Tax)",
    )
    margin_percent = models.DecimalField(max_digits=6, decimal_places=2, default=25, verbose_name="Margin (%)")
    default_selling_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Default Selling Price",
    )
    single_stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Single Product Quantity")
    single_imei_numbers = models.TextField(blank=True, null=True, verbose_name="Single Product IMEI Numbers")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name"]

    @staticmethod
    def _parse_imei_lines(raw_value):
        if not raw_value:
            return []
        return [line.strip() for line in str(raw_value).splitlines() if line.strip()]

    def clean(self):
        if self.subcategory_name and self.category_name:
            if self.subcategory_name.category_id != self.category_name_id:
                raise ValidationError({
                    "subcategory_name": "Selected subcategory does not belong to selected category."
                })

        if self.subcategory_name and not self.category_name:
            self.category_name = self.subcategory_name.category

        if self.vat_rate:
            self.applicable_tax_percent = self.vat_rate.rate_percent
            self.selling_price_tax_type = self.vat_rate.tax_type

        if self.manage_stock and not self.low_stock_alert_quantity:
            raise ValidationError({
                "low_stock_alert_quantity": "Low stock alert quantity is required when manage stock is enabled."
            })

        if self.default_purchase_price_exc_tax is not None:
            tax_rate = self.applicable_tax_percent or Decimal("0")
            calculated_inc_tax = self.default_purchase_price_exc_tax * (Decimal("1") + (tax_rate / Decimal("100")))
            if self.default_purchase_price_inc_tax in (None, Decimal("0")):
                self.default_purchase_price_inc_tax = calculated_inc_tax.quantize(Decimal("0.01"))

            margin = self.margin_percent or Decimal("0")
            calculated_selling_exc = self.default_purchase_price_exc_tax * (Decimal("1") + (margin / Decimal("100")))
            if self.selling_price_tax_type == "inclusive":
                calculated_selling = calculated_selling_exc * (Decimal("1") + (tax_rate / Decimal("100")))
            else:
                calculated_selling = calculated_selling_exc

            if self.default_selling_price in (None, Decimal("0")):
                self.default_selling_price = calculated_selling.quantize(Decimal("0.01"))

        if self.product_type == "single" and self.enable_imei_or_serial:
            imei_lines = self._parse_imei_lines(self.single_imei_numbers)
            if self.single_stock_quantity and len(imei_lines) != self.single_stock_quantity:
                raise ValidationError({
                    "single_imei_numbers": "IMEI count must match Single Product Quantity."
                })

            if len(set(imei_lines)) != len(imei_lines):
                raise ValidationError({
                    "single_imei_numbers": "Duplicate IMEI numbers are not allowed."
                })

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


class VariationAttributeValue(Common):
    attribute = models.ForeignKey(
        VariationAttribute,
        on_delete=models.CASCADE,
        related_name="values",
        verbose_name="Variation Attribute",
    )
    value = models.CharField(max_length=100, verbose_name="Attribute Value")
    value_code = models.CharField(max_length=30, blank=True, verbose_name="Value Code")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Variation Attribute Value"
        verbose_name_plural = "Variation Attribute Values"
        ordering = ["attribute__order", "order", "value"]
        unique_together = [["attribute", "value"]]

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


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
    variation_image = models.ImageField(
        upload_to="products/variations/",
        blank=True,
        null=True,
        verbose_name="Variation Image",
    )

    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Sales Price")
    selling_price_inc_tax = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Selling Price (Inc. Tax)",
    )
    purchase_price_exc_tax = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Purchase Price (Exc. Tax)",
    )
    purchase_price_inc_tax = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Purchase Price (Inc. Tax)",
    )
    vat_rate = models.ForeignKey(
        VatRate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="variations",
        verbose_name="VAT Rate",
    )
    applicable_tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Applicable Tax (%)")
    selling_price_tax_type = models.CharField(
        max_length=20,
        choices=Product.TAX_TYPES,
        default="exclusive",
        verbose_name="Selling Price Tax Type",
    )
    margin_percent = models.DecimalField(max_digits=6, decimal_places=2, default=25, verbose_name="Margin (%)")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantity")
    dealer_price = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Dealer Price")

    isunck = models.BooleanField(default=False, verbose_name="Has Unique Key")
    unickkey = models.ManyToManyField(
        unick,
        blank=True,
        related_name="variations",
        verbose_name="Unique Keys"
    )
    attribute_values = models.ManyToManyField(
        VariationAttributeValue,
        blank=True,
        related_name="variations",
        verbose_name="Attribute Values",
    )
    imei_numbers = models.TextField(blank=True, null=True, verbose_name="IMEI Numbers")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Variation"
        verbose_name_plural = "Variations"
        ordering = ["id"]

    @staticmethod
    def _parse_imei_lines(raw_value):
        if not raw_value:
            return []
        return [line.strip() for line in str(raw_value).splitlines() if line.strip()]

    def clean(self):
        if self.vat_rate:
            self.applicable_tax_percent = self.vat_rate.rate_percent
            self.selling_price_tax_type = self.vat_rate.tax_type

        tax_rate = self.applicable_tax_percent or Decimal("0")
        tax_multiplier = Decimal("1") + (tax_rate / Decimal("100"))

        if self.purchase_price_exc_tax is not None:
            purchase_inc = self.purchase_price_exc_tax * tax_multiplier
            if self.purchase_price_inc_tax in (None, Decimal("0")):
                self.purchase_price_inc_tax = purchase_inc.quantize(Decimal("0.01"))

            margin = self.margin_percent or Decimal("0")
            default_selling_exc = self.purchase_price_exc_tax * (Decimal("1") + (margin / Decimal("100")))

            if self.selling_price_tax_type == "inclusive":
                if self.selling_price_inc_tax in (None, Decimal("0")):
                    if self.price not in (None, Decimal("0")):
                        self.selling_price_inc_tax = (self.price * tax_multiplier).quantize(Decimal("0.01"))
                    else:
                        self.selling_price_inc_tax = (default_selling_exc * tax_multiplier).quantize(Decimal("0.01"))

                if self.selling_price_inc_tax is not None:
                    if tax_multiplier != Decimal("0"):
                        self.price = (self.selling_price_inc_tax / tax_multiplier).quantize(Decimal("0.01"))
                    else:
                        self.price = self.selling_price_inc_tax.quantize(Decimal("0.01"))
            else:
                if self.price in (None, Decimal("0")):
                    self.price = default_selling_exc.quantize(Decimal("0.01"))

        if self.price is not None and self.selling_price_inc_tax in (None, Decimal("0")):
            selling_inc = self.price * tax_multiplier
            if self.selling_price_inc_tax in (None, Decimal("0")):
                self.selling_price_inc_tax = selling_inc.quantize(Decimal("0.01"))

        if self.isunck:
            imei_lines = self._parse_imei_lines(self.imei_numbers)
            if self.quantity and len(imei_lines) != self.quantity:
                raise ValidationError({
                    "imei_numbers": "IMEI count must match variation quantity when unique/IMEI is enabled."
                })

            if len(set(imei_lines)) != len(imei_lines):
                raise ValidationError({
                    "imei_numbers": "Duplicate IMEI numbers are not allowed for a variation."
                })

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