from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import viewsets
from .models import user
from .serializers import Userserializer
from django.core.paginator import Paginator, EmptyPage,  PageNotAnInteger
from django.db.models import Q
from datetime import datetime
from django.contrib import messages
from django.utils import timezone



# Create your views here.




class UserView(viewsets.ModelViewSet):
    
    queryset = user.objects.all()
    serializer_class = Userserializer    





# =================================================================================================================================================

# ------ALL RECORDS------------

# def allrecords(request):
    
#     rid = user.objects.all()
    
#     con = {
        
#         'rid' : rid,
#         'disable_pagination': True
#     }
    

#     return render(request,'allrecords.html',con)
    

def allrecords(request):
    query = request.GET.get('search', '')  # Get the search keyword from the input field
    filter_option = request.GET.get('filter', '') 
    
    try:
        records_per_page = int(request.GET.get('records_per_page', 5))  # Default to 5 if not set or invalid
    except ValueError:
        records_per_page = 5  # Fallback to default if conversion fails
        
    users = user.objects.all().order_by('-id')  # Fetch all tasks
    
    if query:
        # Apply filter to author, title, and description based on the search term
        users = users.filter(
            Q(book__icontains=query) | 
            Q(author__icontains=query) | 
            Q(publication__icontains=query) |
            Q(booktypes__icontains=query)
        )
    
        # Apply date filter based on the selected filter option
    if filter_option == 'published_before_2024':  # Published Before 2024
        users = users.filter(date__lt='2024-01-01')
    elif filter_option == 'published_after_2024':  # Published After 2024
        users = users.filter(date__gte='2024-01-01')
    elif filter_option == 'Religious Books':  # Filter by Religious book type
        users = users.filter(booktypes__icontains='Religious Books')
    elif filter_option == 'Technical Books':  # Filter by technical Books book type
        users = users.filter(booktypes__icontains='Technical Books')
    elif filter_option == 'Novel Books':  # Filter by Novel Books book type
        users = users.filter(booktypes__icontains='Novel Books')
    elif filter_option == 'Story Books':  # Filter by Novel Books book type
        users = users.filter(booktypes__icontains='Story Books')
    
    # Get the number of records per page from the GET parameter (default to 5)
    records_per_page = int(request.GET.get('records_per_page', 5))  # Default is 5 if no value is provided
    
    # Paginate the tasks queryset with the dynamic records_per_page value
    paginator = Paginator(users, records_per_page)  # Records per page based on user selection
    page_number = request.GET.get('page')  # Get the current page number from the query params
    page_obj = paginator.get_page(page_number)  # Get the tasks for the current page

    # Add sequential ID logic
    for idx, user_obj in enumerate(page_obj.object_list, start=1):
        user_obj.display_id = idx
        
    start_index = (page_obj.number - 1 )* records_per_page  

    
    return render(request, 'allrecords.html', {
        'users': page_obj, 
        'search': query,
        'filter': filter_option,
        'records_per_page': records_per_page,
        'start_index': start_index})
    

# =================================================================================================================================================   

  
  
  
# ------INDEX------------  
    
    
def index(request):
    query = request.GET.get('search', '')  # Get the search keyword from the input field
    filter_option = request.GET.get('filter', '') 
    
    try:
        records_per_page = int(request.GET.get('records_per_page', 5))  # Default to 5 if not set or invalid
    except ValueError:
        records_per_page = 5  # Fallback to default if conversion fails
    users = user.objects.all().order_by('-updated_at', '-id')
    
    if query:
        # Apply filter to author, title, and description based on the search term
        users = users.filter(
            Q(book__icontains=query) | 
            Q(author__icontains=query) | 
            Q(publication__icontains=query) |
            Q(booktypes__icontains=query)
        )
    
        # Apply date filter based on the selected filter option
    if filter_option == 'published_before_2024':  # Published Before 2024
        users = users.filter(date__lt='2024-01-01')
    elif filter_option == 'published_after_2024':  # Published After 2024
        users = users.filter(date__gte='2024-01-01')
    elif filter_option == 'Religious Books':  # Filter by Religious book type
        users = users.filter(booktypes__icontains='Religious Books')
    elif filter_option == 'Technical Books':  # Filter by technical Books book type
        users = users.filter(booktypes__icontains='Technical Books')
    elif filter_option == 'Novel Books':  # Filter by Novel Books book type
        users = users.filter(booktypes__icontains='Novel Books')
    elif filter_option == 'Story Books':  # Filter by Novel Books book type
        users = users.filter(booktypes__icontains='Story Books')
    
    
    # Paginate the tasks queryset with the dynamic records_per_page value
    paginator = Paginator(users, records_per_page)  # Records per page based on user selection
    page_number = request.GET.get('page')  # Get the current page number from the query params
    page_obj = paginator.get_page(page_number)  # Get the tasks for the current page

    # Add sequential ID logic
    for idx, user_obj in enumerate(page_obj.object_list, start=1):
        user_obj.display_id = idx
        
    start_index = (page_obj.number - 1 )* records_per_page  

    
    return render(request, 'index.html', {
        'users': page_obj, 
        'search': query,
        'filter': filter_option,
        'records_per_page': records_per_page,
        'start_index': start_index})
    
    
    
    
# =================================================================================================================================================





# ------ADD RECORDS------------

def addrecords(request):
    
    if request.POST:
        book = request.POST['book'].strip()
        author = request.POST['author'].strip()
        publication = request.POST['publication'].strip()
        booktypes = request.POST['booktypes'].strip()
        date = request.POST['date'].strip()
        
        
        # Convert date to a datetime object
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'add_records.html', {'error': 'Invalid Date Format! Please use YYYY-MM-DD.'})

        # Check for invalid date: 500 years ago or future date
        current_date = datetime.now().date()
        min_date = current_date.replace(year=current_date.year - 600)

        if date_obj > current_date:
            return render(request, 'add_records.html', {'error': 'Date cannot be in the future!'})
        elif date_obj < min_date:
            return render(request, 'add_records.html', {'error': 'Date cannot be older than 600 years!'})
        
        
         # Check for invalid inputs (e.g., double spaces or empty strings after stripping)
        if not book or "  " in book:
            return render(request, 'addrecords.html', {'error': 'Invalid Book Title! No double spaces or empty values allowed.'})
        if not author or "  " in author:
            return render(request, 'addrecords.html', {'error': 'Invalid Author Name! No double spaces or empty values allowed.'})
        if not booktypes:
            return render(request, 'addrecords.html', {'error': 'Please select a Book Type!'})
        if not date:
            return render(request, 'addrecords.html', {'error': 'Published Date is required!'})

        # Optionally allow description to be empty but no double spaces
        if publication and "  " in publication:
            return render(request, 'add_records.html', {'error': 'Invalid publication! No double spaces allowed.'})

        
        uid = user.objects.create(book=book,
                                author=author,
                              publication=publication,
                            booktypes = booktypes,
                              date=date)
    
        messages.success(request, 'Book added successfully!')
        
        return redirect('index')
    else:
        return render(request,'addrecords.html')
    


# =================================================================================================================================================





# ------DELETE------------

def deletes(request,id):
    
    did = user.objects.get(id=id).delete()
    
    messages.success(request, 'Book Deleted successfully!')
    
    return redirect('index')


    
    
# =================================================================================================================================================    




# ------UPDATE------------

def update(request, id):
    uid = user.objects.get(id=id)
    

    if request.method == "POST":
        book = request.POST['book'].strip()
        author = request.POST['author'].strip()
        publication = request.POST['publication'].strip()
        booktypes = request.POST['booktypes'].strip()
        date = request.POST['date'].strip()
        # date = datetime.now().date()  # Get current date
        # Convert date to a datetime object
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'update.html', {'error': 'Invalid Date Format! Please use YYYY-MM-DD.', 'users': [uid]})

        # Check for invalid date: 500 years ago or future date
        current_date = datetime.now().date()
        min_date = current_date.replace(year=current_date.year - 600)

        if date_obj > current_date:
            return render(request, 'update.html', {'error': 'Date cannot be in the future!', 'users': [uid]})
        elif date_obj < min_date:
            return render(request, 'update.html', {'error': 'Date cannot be older than 600 years!', 'users': [uid]})        
        

        uid.book = book     
        uid.author = author
        uid.publication = publication
        uid.booktypes = booktypes
        uid.date = date
        uid.updated_at = timezone.now()
        uid.save()
        
        messages.success(request, 'Book updated successfully!')
    
        return redirect('index')  # Redirect to index or wherever you want
    else:
        return render(request, 'update.html', {'rid': [uid]},)



# =================================================================================================================================================




# ------SEARCH------------
   
    
# def search(request):
#     query = request.GET.get('search', '')  # Get the search keyword from the input field
#     filter_option = request.GET.get('filter', '')  # Get the selected filter option

#     # Initially fetch all records
#     users = user.objects.all().order_by('id')
    

#     if query:
#         # Apply filter to author, title, and description based on the search term
#         users = users.filter(
#             Q(book__icontains=query) | 
#             Q(author__icontains=query) | 
#             Q(publication__icontains=query) |
#             Q(booktypes__icontains=query)
#         )
    
#     # Apply date filter based on the selected filter option
#     if filter_option == 'published_before_2024':  # Published Before 2024
#         users = users.filter(date__lt='2024-01-01')
#     elif filter_option == 'published_after_2024':  # Published After 2024
#         users = users.filter(date__gte='2024-01-01')
#     elif filter_option == 'Religious Books':  # Filter by Religious book type
#         users = users.filter(booktypes__icontains='Religious Books')
#     elif filter_option == 'Technical Books':  # Filter by technical Books book type
#         users = users.filter(booktypes__icontains='Technical Books')
#     elif filter_option == 'Novel Books':  # Filter by Novel Books book type
#         users = users.filter(booktypes__icontains='Novel Books')
#     elif filter_option == 'Story Books':  # Filter by Novel Books book type
#         users = users.filter(booktypes__icontains='Story Books')
    

#     # Ensure that the final queryset is ordered by 'id'
#     # users = users.order_by('id')

#     # Pagination logic
#     per_page = int(request.GET.get('per_page', 5))  # Default to 5 records per page
#     paginator = Paginator(users, per_page)
#     page_number = request.GET.get('page', 1)
#     # page_obj = paginator.get_page(page_number)
    
    
#     try:
#         # Get the records for the current page
#         page_obj = paginator.get_page(page_number)
#     except PageNotAnInteger:
#         # If page is not an integer, fallback to the first page
#         page_obj = paginator.get_page(1)
#     except EmptyPage:
#         # If page is out of range, fallback to the last page
#         page_obj = paginator.get_page(paginator.num_pages)
    
    
#     # Pass the paginated results, search query, and filter to the template
#     return render(request, 'index.html', {
#         'users': page_obj, 
#         'search': query,
#         'filter': filter_option,
#         'per_page': per_page,
#     })



# =================================================================================================================================================


















# --------------records_per_page_view2 all records--------------


def records_per_page_view2(request):
    # Step 1: Fetch the 'records_per_page' from session or GET parameter (default to 5)
    if 'default' in request.GET:
            records_per_page = 5  # Default to 5 if invalid value provided
            request.session['records_per_page'] = records_per_page  # Save to session
    elif 'records_per_page' in request.GET:
            records_per_page = int(request.GET.get('records_per_page'))  # Convert to integer
            request.session['records_per_page'] = records_per_page
    else:
        records_per_page = request.session.get('records_per_page', 5)  # Default to 5 if not in session

    # Step 2: Fetch all records and order by '-id'
    allrecords = user.objects.all().order_by('-id')  # Replace 'User' with your model

    # Step 3: Apply pagination based on 'records_per_page'
    paginator = Paginator(allrecords, records_per_page)
    page_number = request.GET.get('page', 1)  # Get the current page number (default to 1)
    page_obj = paginator.get_page(page_number)  # Get paginated data


    # Step 4: Render the template with paginated data
    return render(request, 'allrecords.html', {
        'users': page_obj,  # Paginated records for the current page
        'records_per_page': records_per_page,  # Pass selected records per page
    })

# =================================================================================================================================================

# --------------records_per_page_view index--------------



def records_per_page_view(request):
    # Step 1: Get the records_per_page from the session or GET parameter (default to 5)
    if 'records_per_page' in request.GET:
        records_per_page = int(request.GET.get('records_per_page'))
        request.session['records_per_page'] = records_per_page  # Save to session
    else:
        records_per_page = request.session.get('records_per_page', 5)  # Default to 5

    # Step 2: Fetch all records and order by '-id'
    allrecords = user.objects.all().order_by('-id')

    # Step 3: Apply pagination based on records_per_page
    paginator = Paginator(allrecords, records_per_page)
    page_number = request.GET.get('page', 1)  # Get the current page number (default to 1)
    page_obj = paginator.get_page(page_number)  # Get paginated data

    # Step 4: Render the template with paginated data
    return render(request, 'index.html', {
        'users': page_obj,  # Paginated records for the current page
        'records_per_page': records_per_page,  # Pass selected records per page
    })


# =================================================================================================================================================




# -------------- searchall --------------




def searchall(request):
    search_query = request.GET.get('search', '')
    rid = user.objects.all()

    if search_query:
        rid = rid.filter(
            Q(book__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(booktypes__icontains=search_query) |
            Q(publication__icontains=search_query)
        )
        
        records_per_page = int(request.GET.get('records_per_page', 5))  # Default is 5 if no value is provided
    
        # Paginate the tasks queryset with the dynamic records_per_page value
        paginator = Paginator(rid, records_per_page)  # Records per page based on user selection
        page_number = request.GET.get('page')  # Get the current page number from the query params
        page_obj = paginator.get_page(page_number)  # Get the tasks for the current page

        # Add sequential ID logic
        for idx, user_obj in enumerate(page_obj.object_list, start=1):
            user_obj.display_id = idx
            
        start_index = (page_obj.number - 1 )* records_per_page  

        
        return render(request,'allrecords.html', {'rid' : rid, 
                                                  'search': search_query,
                                                  'start_index': start_index, 
                                                  'records_per_page': records_per_page,})



