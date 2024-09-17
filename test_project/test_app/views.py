import os
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib import messages
from .models import *
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User as AuthUser
from .forms import FileUploadForm,CompanyFilterForm
from .tasks import process_csv



def dashboard(request):
    d = {'form': FileUploadForm()}
    return render(request, "dashboard.html", d)


def upload_data(request):
    return render(request, 'upload_data.html')


def user(request):
    return render(request, 'user.html')


def query_builder_view(request):
    form = CompanyFilterForm(request.GET or None)  # Bind form with GET data

    # Base query for filtering
    companies = Company.objects.all()

    # If the form is valid, apply filters
    if form.is_valid():
        # Apply filters based on form input
        name = form.cleaned_data.get('name')
        industry = form.cleaned_data.get('industry')
        country = form.cleaned_data.get('country')
        min_revenue = form.cleaned_data.get('min_revenue')
        max_revenue = form.cleaned_data.get('max_revenue')

        if name:
            companies = companies.filter(name__icontains=name)
        if industry:
            companies = companies.filter(industry__icontains=industry)
        if country:
            companies = companies.filter(country__icontains=country)
        if min_revenue is not None:
            companies = companies.filter(revenue__gte=min_revenue)
        if max_revenue is not None:
            companies = companies.filter(revenue__lte=max_revenue)

    # Get the count of filtered results
    company_count = companies.count()

    return render(request, 'query_builder.html', {'form': form, 'company_count': company_count})



def index(request):
    if request.method == 'POST':
        uname = request.POST.get("username")
        passwd = request.POST.get("password")
        user = authenticate(request, username=uname, password=passwd)
        if user is not None:
            try:
                request.session["id"] = user.id
                login(request, user)
                return redirect("test_app/dashboard")
            except Exception as e:
                messages.error(request, f"An error occurred while logging in: {e}")
        else:
            messages.error(request, "Invalid username or password.")
            d = {'form': LoginForm}
            return render(request, 'index.html', d)
    else:
        d = {'form': LoginForm}
        return render(request, 'index.html', d)


def register(request):
    try:
        if request.method == 'POST':
            obj = RegisterForm(request.POST)
            obj.save(obj)
            return redirect("test_app/index")

        else:
            d = {'form': RegisterForm}
            return render(request, 'registration.html', d)
    except Exception as e:
        messages.error(request, f"An error occurred while registering: {e}")
        d = {'form': RegisterForm}
        return render(request, 'registration.html', d)


def upload_file(request):
    if request.method == 'POST':
        try:
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                # Save the uploaded file
                uploaded_file_instance = form.save(commit=False)
                uploaded_file_instance.file = request.FILES['file']
                uploaded_file_instance.save()

                # Get the file path
                csv_file = request.FILES['file']
                file_path = os.path.join(settings.MEDIA_ROOT, csv_file.name)

                # Save the file to the server
                with open(file_path, 'wb+') as destination:
                    for chunk in csv_file.chunks():
                        destination.write(chunk)

                # Call the Celery task to process the CSV in the background
                process_csv.delay(file_path)  # .delay() to run asynchronously

                messages.success(request, 'File uploaded successfully! Data is being processed in the background.')
                return redirect("/test_app/dashboard")
            else:
                messages.error(request, 'File upload failed. Please try again.')
        except Exception as e:
            messages.error(request, f"An error occurred while uploading the file: {e}")
    else:
        form = FileUploadForm()

    return render(request, 'dashboard.html', {'form': form})
def user_list(request):
    if request.method == 'POST':
        # Toggle active status
        user_id = request.POST.get('user_id')
        try:
            user = AuthUser.objects.get(id=user_id)
            user.is_active = not user.is_active
            user.save()
            return JsonResponse({'success': True})
        except AuthUser.DoesNotExist:
            return JsonResponse({'success': False})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f"An error occurred: {e}"})
    else:
        # Fetch authenticated users
        try:
            users = AuthUser.objects.all()
            return render(request, 'user.html', {'users': users})
        except Exception as e:
            messages.error(request, f"An error occurred while fetching users: {e}")
            return render(request, 'user.html')


def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'User added successfully!')
            return redirect('test_app/user_list')  # Redirect to user list page
        except Exception as e:
            messages.error(request, f"An error occurred while adding user: {e}")
    return redirect('test_app/user_list')


def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return redirect('/test_app/user_list')
        except User.DoesNotExist:
            return HttpResponseNotFound()
        except Exception as e:
            messages.error(request, f"An error occurred while deleting user: {e}")
            return redirect('test_app/user_list')
    else:
        return HttpResponseNotFound()





def logout(request):
    auth_logout(request)
    return redirect("test_app/index")


