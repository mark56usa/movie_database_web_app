from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
              'Movies',
              api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)

def create(request):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/No_image_available_400_x_600.svg/320px-No_image_available_400_x_600.svg.png'}] ,
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes'),
        }
        try:
            response=AT.insert(data)
            messages.success(request, 'Your entry for {} has been added'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'The error {} was generated when attempting create entry'.format(e))

    return redirect("/")

def edit(request, movie_id):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/No_image_available_400_x_600.svg/320px-No_image_available_400_x_600.svg.png'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes'),
        }

        try:
            response=AT.update(movie_id, data)
            messages.success(request, '{} has been updated'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'The error {} was generated when attempting update the movie'.format(e))

    return redirect("/")

def delete(request, movie_id):
    try:
        movie_name=AT.get(movie_id)['fields'].get('Name')
        response=AT.delete(movie_id)
        messages.warning(request, 'Then entry for {} has been deleted'.format(movie_name))
    except Exception as e:
        messages.warning(request, 'The error {} was generated when attempting to delete the record.'.format(e))

    return redirect("/")
