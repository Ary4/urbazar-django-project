from django.shortcuts import render
from urbazar_app.models import Product
from urbazar_app.models import Student
from urbazar_app.models import Flag
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.http import HttpResponse
from django.db import connection
import os
import datetime

MAX_PAGE_ITEMS = 9


def landing_view(request):
    return render(request, 'landing-page.html', context={})  # load the home page


def search_view(request, feed_query=None):
    query = request.GET.get("q")  # gets the query as a string from GET request
    currPage = request.GET.get("page", 1)
    currPage = int(currPage)

    if feed_query is not None:  # if feed_query is requested
        query = feed_query

    if query is None:  # if query is done by categories i.e electronics/books catagories
        query = request.GET.get("c")
        cursor = connection.cursor()
        cursor.execute("SELECT title,description,price,ffs_product.image,flag_count,first_name,last_name,hostel_name,email,status,ffs_product.id,ffs_student.id,category FROM ffs_product,ffs_student WHERE category like '%" + str(
                query) + "%' and ffs_product.owner_id=ffs_student.id ;")
        queryset = cursor.fetchall()
        connection.close()
    else:  # if query is done by search bar
        cursor = connection.cursor()
        cursor.execute("SELECT title,description,price,ffs_product.image,flag_count,first_name,last_name,hostel_name,email,status,ffs_product.id,ffs_student.id,category FROM ffs_product,ffs_student WHERE title like '%" + query + "%' and ffs_product.owner_id=ffs_student.id ;")
        queryset = cursor.fetchall()
        connection.close()
    # Page-ination is DONE with maximum 12 items per page
    pages = (((len(queryset) - (len(queryset) % MAX_PAGE_ITEMS)) / MAX_PAGE_ITEMS) + 1) if (
            len(queryset) > MAX_PAGE_ITEMS) else 1
    pages = range(1, int(pages) + 1)
    queryset = queryset[(currPage - 1) * MAX_PAGE_ITEMS:((currPage * MAX_PAGE_ITEMS)) if (
            ((currPage * MAX_PAGE_ITEMS)) < len(queryset)) else len(queryset)]
    context = {'results': queryset, 'entered_text': query, 'pages': pages,
               'currPage': currPage}  # making dictionary to be passed in search html page
    return render(request, 'search_result_page.html', context)


@login_required(
    login_url="/accounts/login/")  # checking if user is logged in..and if it isnt ..redirect him to login page
def flagged_view(request):  # show items which are marked/flagged by the user to purchase or interested in
    items = Flag.objects.filter(user=request.user.student)  # finds the products which are flagged by the user
    currPage = request.GET.get("page", 1)
    query = request.GET.get("qq", "")  # here qq is the query which is used in search bar in flagged items page
    currPage = int(currPage)
    lst = []
    for item in items:
        lst += [j for j in item.products.all()]
    newlst = []
    for item in lst:
        if query.lower() in item.title.lower():
            newlst.append(item)
        elif query == "":
            newlst.append(item)
    lst = newlst
    # page-ination is DONE by the followed code
    pages = (((len(lst) - (len(lst) % MAX_PAGE_ITEMS)) / MAX_PAGE_ITEMS) + 1) if (len(lst) > MAX_PAGE_ITEMS) else 1
    pages = range(1, int(pages) + 1)
    lst = lst[(currPage - 1) * MAX_PAGE_ITEMS:((currPage * MAX_PAGE_ITEMS)) if (
            ((currPage * MAX_PAGE_ITEMS)) < len(lst)) else len(lst)]
    context = {
        'flagged_items': lst,
        'pages': pages,
        'currPage': currPage
    }  # creates a dictionary of flagged items ,pages, current page number
    return render(request, 'flagged_items_page.html', context)


@csrf_exempt
@login_required(login_url="/accounts/login/")
def add_to_flagged(request):  # adds a product to flagged item list of a user
    if request.method == 'POST':
        print(request.POST)
        current_user = request.user.student
        id = request.POST.get("product_id")
        prod_obj = Product.objects.get(pk=id)
        qs = Flag.objects.filter(user=current_user, products=prod_obj)
        # Check to prevent user to flag own item and prevent user to flag same item multiple times
        if not qs.exists() and prod_obj.owner != current_user:
            prod_obj.flag_count += 1
            cursor = connection.cursor()
            cursor.execute("UPDATE ffs_product SET flag_count=flag_count+1 WHERE id='" + str(id) + "';")
            connection.close()
            #prod_obj.save()
            flag_obj = Flag.objects.create(user=current_user)
            flag_obj.products.add(
                prod_obj)  # product id taken using get method and saved as foreign key in flagged item table
    return redirect("/flagged/")


@csrf_exempt
@login_required(login_url="/accounts/login/")
def remove_from_flagged(request):  # removes the product from flagged item list
    flagged = Flag.objects.all()
    if request.method == 'POST':
        current_user = request.user.student
        id = request.POST.get("product_id")
        prod_obj = Product.objects.get(pk=id)
        flag_obj = Flag.objects.get(user=current_user, products=prod_obj)
        flag_obj.delete()  # deleting the flagged object
        if prod_obj.flag_count > 0:
            prod_obj.flag_count -= 1  # reduces the flag count by one
            prod_obj.save()
    return redirect("/flagged/")


@login_required(login_url="/accounts/login/")
def user_view(request):  # user profile data is shown
    return render(request, 'user.html', {'current_user': request.user.student})


@login_required(login_url="/accounts/login/")
def view_alt_user(request):  # another user profile is shown
    if request.method == 'GET':
        user_id = request.GET['user_obj']
        alt_user = Student.objects.get(id=user_id)
    return render(request, 'alt_user.html', {'alt_user': alt_user})


@csrf_exempt
@login_required(login_url="/accounts/login/")
def remove_from_user(request):  # product is deleted from the user's uploads
    if request.method == 'POST':
        id = request.POST.get("product_id")
        prod_inst = Product.objects.get(pk=id)
        prod_inst.delete()
    return redirect("/user/")


from .forms import UploadProductForm


@login_required(login_url="/accounts/login/")
def upload_view(request):  # create upload view to upload a product
    if request.method == "POST":
        form = UploadProductForm(request.POST, request.FILES) # takes the form data
        if form.is_valid():  # checks the form is valid or not
            product_instance = form.save(commit=False)
            product_owner = request.user.student
            product_instance.owner = product_owner
            product_instance.save() # save the product to database

            return HttpResponseRedirect("../user/?success")
    else:
        form = UploadProductForm()
    return render(request, 'upload-page.html', {'form': form})


from .forms import EditProfileForm


@login_required(login_url="/accounts/login/")
def edit_profile_view(request):
    logged_in_user = request.user.student
    college = logged_in_user.get_college_display()
    form = EditProfileForm(instance=logged_in_user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=logged_in_user)
        if form.is_valid():
            form.save()
    return render(request, 'user_edit.html', {'form': form, 'user_college': college})


from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if (request.FILES.get('image') != None):
            if (os.path.splitext(request.FILES['image'].name)[1] in settings.ALLOWED_IMAGE_TYPES):
                if form.is_valid():
                    user = form.save()
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password1')
                    student = Student(django_user=user,
                                      first_name=form.cleaned_data.get('first_name'),
                                      last_name=form.cleaned_data.get('last_name'),
                                      room_number=form.cleaned_data.get('room_number'),
                                      hostel_name=form.cleaned_data.get('hostel_name'),
                                      email=form.cleaned_data.get('username'),
                                      star_count=0,
                                      image=request.FILES.get('image')
                                      )
                    student.save()
                    login(request, user)
                    return render(request, 'landing-page.html', context={})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
