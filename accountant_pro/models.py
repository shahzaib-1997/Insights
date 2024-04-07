from django.db import models
from django.utils import timezone
from accounts.models import Account, Tax
from companydetails.models import Company, Currency
from expense.models import ExpenseAccount, Supplier


class Client(models.Model):
    title = models.CharField(null=True, max_length=255)
    first_name = models.CharField(null=True, max_length=255)
    middle_name = models.CharField(null=True, max_length=255)
    last_name = models.CharField(null=True, max_length=255)
    suffix = models.CharField(null=True, max_length=255)
    display_name = models.CharField(null=True, max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    email = models.CharField(null=True, max_length=255)
    phone = models.CharField(null=True, max_length=255)
    mobile = models.CharField(null=True, max_length=255)
    fax = models.CharField(null=True, max_length=255)
    other = models.CharField(null=True, max_length=255)
    website = models.CharField(null=True, max_length=255)
    sub_customer = models.BooleanField(default=False)
    street_address = models.TextField(null=True)
    city = models.CharField(null=True, max_length=255)
    province = models.CharField(null=True, max_length=255)
    postal_code = models.CharField(null=True, max_length=255)
    country = models.CharField(null=True, max_length=255)
    shipping_street_address = models.TextField(null=True)
    shipping_city = models.CharField(null=True, max_length=255)
    shipping_province = models.CharField(null=True, max_length=255)
    shipping_postal_code = models.CharField(null=True, max_length=255)
    shipping_country = models.CharField(null=True, max_length=255)
    notes = models.TextField(null=True)
    attachment = models.FileField(upload_to="attachments/", null=True, blank=True)
    primary_payment_method = models.ForeignKey(
        "PaymentMethod", null=True, on_delete=models.CASCADE, blank=True
    )
    terms = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=[
            ("Due on receipt", "Due on receipt"),
            ("Net 30", "Net 30"),
            ("Net 60", "Net 60"),
            ("Net 90", "Net 90"),
        ],
    )
    sales_form_delivery_options = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        choices=[
            ("Print later", "Print later"),
            ("Send later", "Send later"),
            ("None", "None"),
            ("Use company default", "Use company default"),
        ],
    )
    language_for_invoices = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        choices=[
            ("English", "English"),
            ("French", "French"),
            ("Spanish", "Spanish"),
            ("Italian", "Italian"),
            ("Chinese (traditional)", "Chinese (traditional)"),
            ("Portuguese (Brazil)", "Portuguese (Brazil)"),
        ],
    )
    sales_tax_registration = models.CharField(null=True, max_length=255)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    as_of = models.DateField(null=True)


class SubClient(Client):
    parent_client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE, related_name="parent", blank=True)
    bill_parent_customer = models.BooleanField(default=False)


class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(null=True, max_length=255)
    first_name = models.CharField(null=True, max_length=255)
    last_name = models.CharField(null=True, max_length=255)
    display_name = models.CharField(null=True, max_length=255)
    email = models.CharField(null=True, max_length=255)
    phone = models.CharField(null=True, max_length=255)
    mobile = models.CharField(null=True, max_length=255)
    street_address = models.TextField(null=True)
    city = models.CharField(null=True, max_length=255)
    province = models.CharField(null=True, max_length=255)
    postal_code = models.CharField(null=True, max_length=255)
    country = models.CharField(null=True, max_length=255)
    notes = models.TextField(null=True)
    employee_id_number = models.CharField(null=True, max_length=255)
    employee_id = models.CharField(null=True, max_length=255)
    hire_date = models.DateField(null=True)
    released_date = models.DateField(null=True)
    billing_rate = models.CharField(null=True, max_length=255)
    billable_by_default = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(
        max_length=50,
        null=True,
        choices=[
            ("Prefer not to answer", "Prefer not to answer"),
            ("Male", "Male"),
            ("Female", "Female"),
        ],
    )


class TagGroup(models.Model):
    name = models.CharField(null=True, max_length=255)


class Tag(models.Model):
    name = models.CharField(null=True, max_length=255)
    group = models.ForeignKey(
        TagGroup, on_delete=models.SET_NULL, null=True, blank=True
    )


class ItemType(models.Model):
    name = models.CharField(null=True, max_length=255)


class Category(models.Model):
    name = models.CharField(null=True, max_length=255)


class Items(models.Model):
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    SKU = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    initial_quantity = models.IntegerField()
    as_of_date = models.DateField()
    reorder_point = models.DateField()
    description = models.TextField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    tax_inclusive = models.BooleanField(default=False)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, null=True, blank=True)
    purchasing_information = models.TextField(null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    expense_account = models.ForeignKey(ExpenseAccount, on_delete=models.CASCADE, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)


class BaseModel(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    email = models.TextField(null=True)
    cc = models.TextField(null=True)
    bcc = models.TextField(null=True)
    send_later = models.BooleanField(default=False)
    date = models.DateField(null=True)
    attachment = models.FileField(upload_to="attachments/", null=True, blank=True)

    class Meta:
        abstract = True


class RepeatModel(models.Model):
    number = models.CharField(max_length=50, null=True)
    billing_address = models.TextField(null=True)
    tags = models.ManyToManyField(Tag)
    message = models.CharField(max_length=255, null=True)
    message_on_statement = models.CharField(max_length=255, null=True)

    class Meta:
        abstract = True


class BaseItemModel(models.Model):
    service_date = models.DateField(null=True)
    product_service = models.ForeignKey(Items, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(null=True)
    quantity = models.PositiveIntegerField(null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True


class Invoice(BaseModel, RepeatModel):
    terms = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=[
            ("Due on receipt", "Due on receipt"),
            ("Net 30", "Net 30"),
            ("Net 60", "Net 60"),
            ("Net 90", "Net 90"),
        ],
    )
    due_date = models.DateField(null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=[
            ("Opened", "Opened"),
            ("Sent", "Sent"),
            ("Viewed", "Viewed"),
            ("Paid", "Paid"),
            ("Deposited", "Deposited"),
            ("Cancelled", "Cancelled"),
            ("Refund", "Refund"),
        ],
    )


class InvoiceItem(BaseItemModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True)


class InvoiceSent(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class InvoiceViewed(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class InvoicePaid(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class InvoiceCancelled(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class InvoiceRefund(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    credit_card = models.BooleanField(default=False)


class Payment(BaseModel):
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, blank=True, null=True)
    reference_no = models.CharField(max_length=20, null=True)
    deposit_to = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2)
    memo = models.TextField(null=True)
    status = models.CharField(
        max_length=10,
        null=True,
        choices=[("Paid", "Paid"), ("Cancelled", "Cancelled")],
    )


class PaymentPaid(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class PaymentCancelled(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class Estimate(BaseModel, RepeatModel):
    expiration_date = models.DateField(null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        null=True,
        choices=[
            ("Created", "Created"),
            ("Pending", "Pending"),
            ("Rejected", "Rejected"),
            ("Accepted", "Accepted"),
            ("Closed", "Closed"),
        ],
    )


class EstimateItem(BaseItemModel):
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, blank=True, null=True)


class EstimatePending(models.Model):
    estimate = models.OneToOneField(Estimate, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class EstimateRejected(models.Model):
    estimate = models.OneToOneField(Estimate, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class EstimateAccepted(models.Model):
    estimate = models.OneToOneField(Estimate, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class EstimateClosed(models.Model):
    estimate = models.OneToOneField(Estimate, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class SalesReceipt(BaseModel, RepeatModel):
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, blank=True, null=True)
    reference_no = models.CharField(max_length=20, null=True)
    deposit_to = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        null=True,
        choices=[
            ("Active", "Active"),
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
    )


class SalesReceiptItem(BaseItemModel):
    sales_receipt = models.ForeignKey(SalesReceipt, on_delete=models.CASCADE, blank=True, null=True)


class SalesReceiptActive(models.Model):
    sales_receipt = models.OneToOneField(SalesReceipt, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class SalesReceiptPending(models.Model):
    sales_receipt = models.OneToOneField(SalesReceipt, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class SalesReceiptCompleted(models.Model):
    sales_receipt = models.OneToOneField(SalesReceipt, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class SalesReceiptCancelled(models.Model):
    sales_receipt = models.OneToOneField(SalesReceipt, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class CreditNote(BaseModel, RepeatModel):
    total_credit = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        null=True,
        choices=[
            ("Active", "Active"),
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
    )


class CreditNoteItem(BaseItemModel):
    credit_note = models.ForeignKey(CreditNote, on_delete=models.CASCADE, blank=True, null=True)


class CreditNoteActive(models.Model):
    credit_note = models.OneToOneField(CreditNote, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class CreditNotePending(models.Model):
    credit_note = models.OneToOneField(CreditNote, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class CreditNoteCompleted(models.Model):
    credit_note = models.OneToOneField(CreditNote, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class CreditNoteCancelled(models.Model):
    credit_note = models.OneToOneField(CreditNote, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class RefundReceipt(BaseModel, RepeatModel):
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, blank=True, null=True)
    refund_from = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    amount_refunded = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        null=True,
        choices=[
            ("Active", "Active"),
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
    )


class RefundReceiptItem(BaseItemModel):
    refund_receipt = models.ForeignKey(RefundReceipt, on_delete=models.CASCADE, blank=True, null=True)


class RefundReceiptActive(models.Model):
    refund_receipt = models.OneToOneField(RefundReceipt, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class RefundReceiptPending(models.Model):
    refund_receipt = models.OneToOneField(RefundReceipt, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class RefundReceiptCompleted(models.Model):
    refund_receipt = models.OneToOneField(RefundReceipt, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class RefundReceiptCancelled(models.Model):
    refund_receipt = models.OneToOneField(RefundReceipt, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class DelayedCredit(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(null=True)
    number = models.CharField(max_length=50, null=True)
    tags = models.ManyToManyField(Tag)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    memo = models.TextField(null=True)
    attachment = models.FileField(upload_to="attachments/", null=True)
    status = models.CharField(
        max_length=10,
        null=True,
        choices=[
            ("Active", "Active"),
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
    )


class DelayedCreditItem(BaseItemModel):
    delayed_credit = models.ForeignKey(DelayedCredit, on_delete=models.CASCADE, blank=True, null=True)


class DelayedCreditActive(models.Model):
    delayed_credit = models.OneToOneField(DelayedCredit, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class DelayedCreditPending(models.Model):
    delayed_credit = models.OneToOneField(DelayedCredit, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class DelayedCreditCompleted(models.Model):
    delayed_credit = models.OneToOneField(DelayedCredit, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class DelayedCreditCancelled(models.Model):
    delayed_credit = models.OneToOneField(DelayedCredit, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class DelayedCharge(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(null=True)
    number = models.CharField(max_length=50, null=True)
    tags = models.ManyToManyField(Tag)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    memo = models.TextField(null=True)
    attachment = models.FileField(upload_to="attachments/", null=True)
    status = models.CharField(
        max_length=10,
        null=True,
        choices=[
            ("Active", "Active"),
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
    )


class DelayedChargeItem(BaseItemModel):
    delayed_charge = models.ForeignKey(DelayedCharge, on_delete=models.CASCADE, blank=True, null=True)


class DelayedChargeActive(models.Model):
    delayed_charge = models.OneToOneField(DelayedCharge, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class DelayedChargePending(models.Model):
    delayed_charge = models.OneToOneField(DelayedCharge, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class DelayedChargeCompleted(models.Model):
    delayed_charge = models.OneToOneField(DelayedCharge, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class DelayedChargeCancelled(models.Model):
    delayed_charge = models.OneToOneField(DelayedCharge, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class TimeActivity(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=255)
    customer = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    service = models.ForeignKey(Items, on_delete=models.CASCADE, blank=True, null=True)
    billable = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    activity_time = models.TimeField(null=True)
    description = models.TextField(null=True)


class BankAccount(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    start_amount = models.IntegerField()
    name = models.CharField(max_length=200)
    iban = models.CharField(max_length=34)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True)
