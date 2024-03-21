import random
import smtplib
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from companydetails.models import Company, CompanyDetail, company_user, Currency
from expense.models import Customer, Bills, Categories, BillItems, CategoryItem
from .models import *
from .forms import *


# Create
def logoutt(request):
    auth.logout(request)
    request.session.pop("company", [])
    return redirect(dashboard)


def login(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                company = company_user.objects.filter(user=user).first()
                request.session["company"] = company.id
                return redirect(dashboard)
        else:
            error = "username or password is incorrect"
            return render(request, "pages-login-2.html", {"error": error})
    else:
        return render(request, "pages-login-2.html")


def signup(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        user_name = request.POST["username"]
        print(request.POST["name"])
        first_name = request.POST["name"].split(" ")
        last_name = request.POST["name"].split(" ")
        email = request.POST["email"]
        if password == confirm_password:
            if User.objects.create_user(user_name, email, password):
                return redirect(company_create)
            else:
                context = {"error": "Could not create user account - please try again."}
                return render(request, "signup.html", context)
        else:
            context = {"error": "Passwords did not match. Please try again."}
            return render(request, "signup.html", context)
    else:
        return render(request, "signup.html")


@csrf_exempt
def company_create(request):

    if request.method == "POST":
        company_name = request.POST["company_name"]
        currency = request.POST["currency"]
        currency, created = Currency.objects.get_or_create(name=currency)
        company = Company(name=company_name, default_currency=currency)
        company.save()

        zip_code = request.POST["zip_code"]
        city = request.POST["city"]
        state = request.POST["state"]
        address = request.POST["address"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]

        company_details = CompanyDetail(
            email=email,
            phone=phone_number,
            address=address,
            zip=zip_code,
            city=city,
            state=state,
            company=company,
        )
        company_details.save()
        return redirect(dashboard)

    return render(request, "company_create.html")


@csrf_exempt
def dashboard(request):

    if request.user.is_authenticated:
        return render(request, "index2.html")
    else:
        return redirect(login)


def send_otp(email):
    otp = str(random.randint(100000, 999999))

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()

    # Authentication
    s.login("", "")

    message = (
        f"Subject: Your OTP for password reset\n\nYour OTP for password reset: {otp}"
    )

    s.sendmail("", [email], message)

    s.quit()

    return otp


def forget_password(request):
    if request.method == "POST":
        print(request.POST)
        email = request.POST["email"]

        otp = send_otp(email)
        print("xrdcftbhnjmk")
        print(otp)
        request.session["reset_email"] = email
        request.session["otp"] = otp

        messages.success(request, "OTP sent to your email.")
        print("otp send")
        return redirect("verify_otp_view")

    return render(request, "forget-pass.html")


def verify_otp_view(request):
    if request.method == "POST":
        entered_otp = request.POST["otp"]
        saved_otp = request.session.get("otp")

        if entered_otp == saved_otp:
            email = request.session.get("reset_email")
            return redirect(f"/reset_password_view?email={email}")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "otp.html")


def reset_password_view(request):
    email = request.GET.get("email")
    if request.method == "POST":
        email = request.POST.get("email")
        new_password = request.POST["new_password"]

        users_with_email = User.objects.filter(email=email)

        if users_with_email.exists():
            for user in users_with_email:
                user.set_password(new_password)
                user.save()

            messages.success(
                request,
                "Password reset successfully. Please login with your new password.",
            )
            return redirect(login)
        else:
            messages.error(request, "User with the provided email does not exist.")

    return render(request, "reset_password.html", {"email": email})


def sales(request):
    company = request.session["company"]
    # Define a dictionary mapping model names to their corresponding queryset objects
    querysets = {
        "Invoice": Invoice.objects.filter(company=company),
        "Payment": Payment.objects.filter(company=company),
        "Estimate": Estimate.objects.filter(company=company),
        "SalesReceipt": SalesReceipt.objects.filter(company=company),
        "CreditNote": CreditNote.objects.filter(company=company),
        "RefundReceipt": RefundReceipt.objects.filter(company=company),
        "DelayedCredit": DelayedCredit.objects.filter(company=company),
        "DelayedCharge": DelayedCharge.objects.filter(company=company),
        "TimeActivity": TimeActivity.objects.filter(company=company),
    }

    # Concatenate querysets into one list and add model name to each object
    merged_sales = []
    for model_name, queryset in querysets.items():
        for obj in queryset:
            obj.type = model_name
            merged_sales.append(obj)

    customers = Client.objects.filter(company=company)

    return render(
        request, "sales.dash.html", {"sales": merged_sales, "customers": customers}
    )


def invoice(request):
    clients = Client.objects.all()
    items = InvoiceItem.objects.all()
    company = Company.objects.first()
    currency = Currency.objects.first()
    client = clients.first()
    invoice = Invoice.objects.all()
    invo = invoice.first()

    if request.method == "POST":
        terms = request.POST["terms"]
        tags = request.POST["tags"]
        invoice_date = request.POST["invoice_date"]
        due_date = request.POST["due_date"]
        billing_address = request.POST["billing_address"]
        message_on_invice = request.POST["message_on_invice"]
        message_on_statement = request.POST["message_on_statement"]

        service_date = request.POST["service_date"]
        product_service_id = request.POST["product_servicet"]  # ID of the selected product/service
        description = request.POST["description"]
        quantity = request.POST["quantity"]
        rate = request.POST["rate"]
        amount = request.POST["amount"]
        tax = request.POST["tax"]

        # Retrieve the selected product or service based on the ID
        product_service = Items.objects.get(id=product_service_id)

        data = Invoice(
            company=company,
            currency=currency,
            client=client,
            terms=terms,
            tags=tags,
            invoice_date=invoice_date,
            due_date=due_date,
            billing_address=billing_address,
            message_on_invice=message_on_invice,
            message_on_statement=message_on_statement,
        )
        data.save()

        data_table = InvoiceItem(
            invoice=invo,
            service_date=service_date,
            product_service=product_service,
            description=description,
            quantity=quantity,
            rate=rate,
            amount=amount,
            tax=tax,
        )
        data_table.save()

    return render(request, "add-sales.html", {"clients": clients, "items": items})


def expense(request):
    suppliers = Supplier.objects.all()
    items = InvoiceItem.objects.all()
    invoice = Bills.objects.all()
    invo = invoice.first()
    company = Company.objects.first()
    currency = Currency.objects.first()
    selected_supplier = suppliers.first()
    category = Categories.objects.all()
    bill_items = BillItems.objects.all()
    item = Items.objects.all()
    cate = category.first()

    if request.method == "POST":
        payment_account = request.POST["payment_account"]
        payment_date = request.POST["payment_date"]
        payment_method = request.POST["payment_method"]
        tags = request.POST["tags"]
        memo = request.POST["memo"]
        attachment = request.POST.get("attachment")

        # category table
        cate = request.POST["category_name"]
        amount = request.POST["amount"]
        description = request.POST["description"]
        cate_id = request.POST["category_name"]
        category_instance = Categories.objects.get(pk=cate_id)

        # itemdetails
        product_service_id = request.POST[
            "product_servicet"
        ]  # Assuming this is the ID of the selected product/service
        description = request.POST["descriptions"]
        quantity = request.POST["qty"]
        rate = request.POST["rate"]
        amount = request.POST["amounts"]
        product_service = Items.objects.get(pk=1)

        data = Bills(
            company=company,
            currency=currency,
            supplier=selected_supplier,
            payment_account=payment_account,
            payment_date=payment_date,
            payment_method=payment_method,
            tags=tags,
            memo=memo,
            attachment=attachment,
        )

        data.save()

        data_table1 = CategoryItem(
            category=category_instance, description=description, amount=amount
        )
        data_table1.save()

        data_table2 = BillItems(
            invoice=invo,
            product_service=product_service,
            description=description,
            quantity=quantity,
            rate=rate,
            amount=amount,
        )

        data_table2.save()

    return render(
        request,
        "add_expense.html",
        {
            "suppliers": suppliers,
            "category": category,
            "bill_items": bill_items,
            "items": items,
        },
    )


def customer(request):
    if request.method == "POST":
        title = request.POST["title"]
        first_name = request.POST["first_name"]
        middle_name = request.POST["middle_name"]
        last_name = request.POST["last_name"]
        suffix = request.POST["suffix"]
        customer_display_name = request.POST["customer_display_name"]
        company_name = request.POST["company_name"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        mobile_number = request.POST["mobile_number"]
        fax = request.POST["fax"]
        other = request.POST["other"]
        website = request.POST["website"]
        street_address = request.POST["street_address"]
        city = request.POST["city"]
        province = request.POST["province"]
        country = request.POST["country"]
        notes = request.POST["notes"]
        billing_address = request.POST["cb_billing_address"]
        attachment = request.POST["attachment"]
        primary_payment_method = request.POST["primary_payment_method"]
        terms = request.POST["terms"]
        sales_from_delivery_options = request.POST["sales_from_delivery_options"]
        invoice_lang = request.POST["invoice_lang"]
        sales_tax_regidtration = request.POST["sales_tax_regidtration"]
        openig_balance = request.POST["openig_balance"]
        as_of = request.POST["as_of"]

        data = Customer(
            title=title,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            suffix=suffix,
            customer_display_name=customer_display_name,
            company_name=company_name,
            email=email,
            phone_number=phone_number,
            mobile_number=mobile_number,
            fax=fax,
            other=other,
            website=website,
            street_address=street_address,
            city=city,
            province=province,
            country=country,
            notes=notes,
            billing_address=billing_address,
            attachment=attachment,
            primary_payment_method=primary_payment_method,
            terms=terms,
            sales_delivery_options=sales_from_delivery_options,
            invoice_language=invoice_lang,
            sales_tax_registration=sales_tax_regidtration,
            opening_balance=openig_balance,
            as_of_date=as_of,
        )

        data.save()

    return render(request, "add_customer.html")


def supplier(request):
    if request.method == "POST":
        title = request.POST["title"]
        first_name = request.POST["first_name"]
        middle_name = request.POST["middle_name"]
        last_name = request.POST["last_name"]
        suffix = request.POST["suffix"]
        supplier_display_name = request.POST["supplier_display_name"]
        company_name = request.POST["company_name"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        mobile_number = request.POST["mobile_number"]
        fax = request.POST["fax"]
        other = request.POST["other"]
        website = request.POST["website"]
        street_address = request.POST["street_address"]
        city = request.POST["city"]
        province = request.POST["province"]
        postal = request.POST["postal"]
        country = request.POST["country"]
        notes = request.POST["notes"]
        attachment = request.POST["attachment"]
        buss_id_no = request.POST["buss_id_no"]
        bill_rate = request.POST["bill_rate"]
        payment_terms = request.POST["payments"]
        account_no = request.POST["account_no"]
        exp_cat = request.POST["exp_cat"]
        opening_balance = request.POST["openig_balance"]
        as_of = request.POST["as_of"]

        data = Supplier(
            title=title,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            suffix=suffix,
            supplier_display_name=supplier_display_name,
            company_name=company_name,
            email=email,
            phone_number=phone_number,
            mobile_number=mobile_number,
            fax=fax,
            other=other,
            website=website,
            street_address=street_address,
            city=city,
            province=province,
            postal=postal,
            country=country,
            notes=notes,
            attachment=attachment,
            buss_id_no=buss_id_no,
            bill_rate=bill_rate,
            payment_terms=payment_terms,
            account_no=account_no,
            exp_cat=exp_cat,
            opening_balance=opening_balance,
            as_of=as_of,
        )
        data.save()

    return render(request, "add_supplier.html")
