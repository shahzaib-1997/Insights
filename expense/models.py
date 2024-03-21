from django.db import models
from accounts.models import Account, Tax
from companydetails.models import Currency, Company


class ExpenseAccount(models.Model):
    account_type = models.CharField(
        max_length=20,
        null=True,
        choices=[
            ("Cost of sales", "Cost of sales"),
            ("Expenses", "Expenses"),
            ("Other expense", "Other expense"),
        ],
    )
    detail_type = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    is_sub_account = models.BooleanField(default=False)
    parent_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    default_tax_code = models.ForeignKey(Tax, on_delete=models.CASCADE, null=True)

    @property
    def available_detail_types(self):
        # Define a mapping between account_type and corresponding detail_types
        detail_type_mapping = {
            "Cost of sales": [
                "Cost of labour - COS",
                "Freight and delivery - COS",
                "Equipment rental - COS",
                "Other costs of sales - COS",
                "Supplies and materials - COS",
            ],
            "Expenses": [
                "Advertising/Promotional",
                "Amortisation expense",
                "Auto",
                "Bad debts",
                "Bank charges",
                "Charitable Contributions",
                "Commissions and fees",
                "Cost of Labour",
                "Dues and subscriptions",
                "Equipment rental",
                "Finance costs",
                "Income tax expense",
                "Insurance - Disability",
                "Insurance - General",
                "Insurance - Liability",
                "Interest paid",
                "Legal and professional fees",
                "Loss on discontinued operations, net of tax",
                "Management compensation",
                "Meals and entertainment",
                "Office/General Administrative Expenses",
                "Other Miscellaneous Service Cost",
                "Other selling expenses",
                "Payroll Expenses",
                "Rent or Lease of Buildings",
                "Repair and maintenance",
                "Shipping and delivery expense",
                "Supplies and materials",
                "Taxes Paid",
                "Travel expenses - general and admin expenses",
                "Travel expenses - selling expense",
                "Unapplied Cash Bill Payment Expense",
                "Utilities",
            ],
            "Other Expense": [
                "Amortisation",
                "Depreciation",
                "Exchange Gain or Loss",
                "Other Expense",
                "Penalties and settlements",
            ],
        }
        return detail_type_mapping.get(self.account_type, [])


class Supplier(models.Model):
    title = models.CharField(null=True, max_length=255)
    first_name = models.CharField(null=True, max_length=255)
    middle_name = models.CharField(null=True, max_length=255)
    last_name = models.CharField(null=True, max_length=255)
    suffix = models.CharField(null=True, max_length=255)
    email = models.CharField(null=True, max_length=255)
    company = models.ForeignKey(
        Company, related_name="vendor_details", on_delete=models.CASCADE
    )
    phone = models.CharField(null=True, max_length=255)
    mobile = models.CharField(null=True, max_length=255)
    fax = models.CharField(null=True, max_length=255)
    display_name = models.CharField(null=True, max_length=255)
    other = models.CharField(null=True, max_length=255)
    website = models.CharField(null=True, max_length=255)
    street_address = models.TextField(null=True)
    city = models.CharField(null=True, max_length=255)
    province = models.CharField(null=True, max_length=255)
    postal_code = models.CharField(null=True, max_length=255)
    country = models.CharField(null=True, max_length=255)
    billing_rate = models.CharField(null=True, max_length=255)
    terms = models.CharField(
        max_length=20,
        null=True,
        choices=[
            ("Due on receipt", "Due on receipt"),
            ("Net 30", "Net 30"),
            ("Net 60", "Net 60"),
            ("Net 90", "Net 90"),
        ],
    )
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    as_of = models.DateField(null=True)
    notes = models.TextField(null=True)
    account_no = models.CharField(null=True, max_length=255)
    business_id = models.CharField(null=True, max_length=255)
    default_expense_account = models.ForeignKey(
        ExpenseAccount, on_delete=models.CASCADE
    )
    attachment = models.FileField(upload_to="attachments/", null=True)
    inactive = models.BooleanField(default=False)


class Bills(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    payment_account = models.CharField(max_length=255, default="Payment Account")
    payment_date = models.DateField(null=True)
    payment_method = models.CharField(
        max_length=30,
        null=True,
        choices=[
            ("Cash", "Cash"),
            ("Cheque", "Cheque"),
            ("Credit Card", "Credit Card"),
            ("Direct Debit", "Direct Debit"),
        ],
    )
    tags = models.TextField(null=True)
    memo = models.CharField(max_length=255, null=True)
    attachment = models.FileField(upload_to="attachments/", null=True)


class BillItems(models.Model):
    invoice = models.ForeignKey(Bills, on_delete=models.CASCADE)
    service_date = models.DateField(null=True)
    # product_service = models.ForeignKey(
    #     Items, on_delete=models.CASCADE, related_name="products"
    # )
    description = models.TextField(null=True)
    quantity = models.PositiveIntegerField(null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.BooleanField(default=False)


class Categories(models.Model):
    category_name = models.CharField(max_length=255, default="default")


class CategoryItem(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    description = models.TextField(null=True)


class Customer(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255)
    suffix = models.CharField(max_length=255, null=True, blank=True)
    customer_display_name = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    other = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    is_sub_customer = models.BooleanField(default=False)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=255)
    billing_address = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=255)
    notes = models.TextField(null=True, blank=True)
    attachment = models.FileField(upload_to="attachments/", null=True, blank=True)
    primary_payment_method = models.CharField(max_length=255, null=True, blank=True)
    terms = models.CharField(max_length=255, null=True, blank=True)
    sales_delivery_options = models.CharField(max_length=255, null=True, blank=True)
    invoice_language = models.CharField(max_length=255, null=True, blank=True)
    sales_tax_registration = models.CharField(max_length=255, null=True, blank=True)
    opening_balance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    as_of_date = models.DateField(null=True, blank=True)
