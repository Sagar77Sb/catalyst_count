from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User as AuthUser
from .forms import FileUploadForm
import csv
import pandas as pd


def dashboard(request):
    d = {'form': FileUploadForm()}
    return render(request, "dashboard.html", d)


def upload_data(request):
    return render(request, 'upload_data.html')


def user(request):
    return render(request, 'user.html')


def query_builder(request):
    latest_file = UploadedFile.objects.last()
    unique_data = {}

    if latest_file:
        try:
            # Read the content of the uploaded file
            file_content = latest_file.file.read().decode('utf-8').splitlines()

            # Parse CSV data into a DataFrame
            csv_reader = csv.DictReader(file_content)
            df = pd.DataFrame(csv_reader)

            # Extract unique values from each column and capitalize column names
            unique_data = {column.capitalize(): df[column].unique().tolist() for column in df.columns}
        except Exception as e:
            messages.error(request, f"An error occurred while processing the file: {e}")

    return render(request, 'query_builder.html', {'unique_data': unique_data})


def index(request):
    if request.method == 'POST':
        uname = request.POST.get("username")
        passwd = request.POST.get("password")
        user = authenticate(request, username=uname, password=passwd)
        if user is not None:
            try:
                request.session["id"] = user.id
                login(request, user)
                return redirect("/Catalyst-dashboard")
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
            obj.save()
            return redirect("/Catalyst-index")

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
                # File save logic
                uploaded_file_instance = form.save(commit=False) 
                uploaded_file_instance.file = request.FILES['file']  
                uploaded_file_instance.save()  
                messages.success(request, 'File uploaded successfully!')
                return redirect("/Catalyst-dashboard")  
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
            return redirect('/Catalyst-user_list')  # Redirect to user list page
        except Exception as e:
            messages.error(request, f"An error occurred while adding user: {e}")
    return redirect('/Catalyst-user_list')


def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return redirect('/Catalyst-user_list')
        except User.DoesNotExist:
            return HttpResponseNotFound()
        except Exception as e:
            messages.error(request, f"An error occurred while deleting user: {e}")
            return redirect('/Catalyst-user_list')
    else:
        return HttpResponseNotFound()


def filter_data(request):
    if request.method == 'GET':
        try:
            keyword = request.GET.get('keyword')
            industry = request.GET.get('Industry')
            city = request.GET.get('City')
            state = request.GET.get('State')
            country = request.GET.get('Country')
            employee_from = request.GET.get('Employee(From)')
            employee_to = request.GET.get('Employee(To)')

            # Read the content of the uploaded file
            latest_file = UploadedFile.objects.last()
            if latest_file:
                file_content = latest_file.file.read().decode('utf-8').splitlines()

                # Parse CSV data into a DataFrame
                csv_reader = csv.DictReader(file_content)
                df = pd.DataFrame(csv_reader)

                # Filter data based on input values
                filtered_data = df
                if keyword:
                    # Filter by keyword search (example: searching in filename)
                    filtered_data = filtered_data[df['file'].str.contains(keyword, case=False, na=False)]
                if industry:
                    filtered_data = filtered_data[df['Industry'].str.contains(industry, case=False, na=False)]
                if city:
                    filtered_data = filtered_data[df['City'].str.contains(city, case=False, na=False)]
                if state:
                    filtered_data = filtered_data[df['State'].str.contains(state, case=False, na=False)]
                if country:
                    filtered_data = filtered_data[df['Country'].str.contains(country, case=False, na=False)]
                if employee_from:
                    filtered_data = filtered_data[df['Employee(From)'].str.contains(employee_from, case=False, na=False)]
                if employee_to:
                    filtered_data = filtered_data[df['Employee(To)'].str.contains(employee_to, case=False, na=False)]

                # Count the number of matching rows
                num_records = len(filtered_data)

                # Display flash message with the number of matching rows
                messages.success(request, f"Number of matching rows: {num_records}")

                return redirect("/Catalyst-query_builder")
            else:
                messages.error(request, 'No uploaded file found')
                return redirect("/Catalyst-query_builder")
        except Exception as e:
            messages.error(request, f"An error occurred while filtering data: {e}")
            return redirect("/Catalyst-query_builder")
    else:
        messages.error(request, 'Method not allowed')
        return redirect("/Catalyst-query_builder")


def logout(request):
    auth_logout(request)
    return redirect("/Catalyst-index")
