from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import RegisterForm, NewObject, DeleteObject
from django.contrib.auth import login, authenticate
from .models import PasswordObject
from .auxiliary_functions import code_function, decode_function
import datetime
from dateutil import parser


def home(request):
    return render(request, 'home.html')

def signup(request):
    #form to signup
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('app:profile'))
    else:
        form = RegisterForm()

    context = {'form': form, }
    return render(request, 'account/access_account/signup.html', context)

@login_required(login_url='/login/')
def profile(request):
    #all object PasswordObject
    query = PasswordObject.objects.filter(user=request.user)
    #Check if the user has selected the show password button.
    # If so, please return the information which password should be displayed in template.
    password = False
    for object in query:
        if 'btn_password%s' %(object.id) in request.GET:
            password = object.id

    context = {'query': query,
               'password': password}
    return render(request, 'account/profile.html', context)

@login_required(login_url='/login/')
def profile_new_entry(request):
    #all object PasswordObject
    query = PasswordObject.objects.filter(user=request.user)
    #form to create new PasswordObject
    if request.method == 'POST':
        form = NewObject(request.POST)
        if form.is_valid():
            password_object = form.save(commit=False)
            password_object.user = request.user
            password_object.save()
            return HttpResponseRedirect(reverse('app:profile_new_entry'))
    else:
        form = NewObject()

    context = {'query': query,
               'form': form}
    return render(request, 'account/profile_new_entry.html', context)

@login_required(login_url='/login/')
def profile_object_edit(request, pk):
    #get instances of the object
    object = get_object_or_404(PasswordObject, pk=pk)
    #The form to edit the received object instance
    if request.method == "POST":
        form = NewObject(request.POST, instance=object)
        if form.is_valid():
            object = form.save(commit=False)
            object.user = request.user
            object.save()
            return HttpResponseRedirect(reverse('app:profile_new_entry'))
    else:
        form = NewObject(instance=object)

    context = {'form': form,
               'object': object}
    return render(request, 'account/profile_object_edit.html', context)

@login_required(login_url='/login/')
def profile_object_delete(request, pk):
    #get instances of the object
    object = get_object_or_404(PasswordObject, pk=pk)
    #The form to delete the received object instance
    if request.method == "POST":
        form = DeleteObject(request.POST, instance=object)
        if form.is_valid():
            object.delete()
            return HttpResponseRedirect(reverse('app:profile_new_entry'))
    else:
        form = DeleteObject(instance=object)

    context = {'form': form,
               'object': object}
    return render(request, 'account/profile_object_delete.html', context)

@login_required(login_url='/login/')
def profile_password_shared(request, pk):
    #basic
    object = get_object_or_404(PasswordObject, pk=pk) #instance object PasswordObject
    now_plus_5 = datetime.datetime.now() + datetime.timedelta(minutes=5) #actual time + 5 minutes
    url_app = request.build_absolute_uri("/") #URL my app
    #link element
    forwarding = '=#=%s=#==@=%s=@=' %(now_plus_5, pk) #create data to be provided in the link
    code_forwarding = code_function(forwarding) #encode forwarding data
    url_forwarding = '%spassword_get/%s/' %(url_app, code_forwarding) #create link to next temlate with encode data

    context = {'object': object,
               'time_link': now_plus_5,
               'url_forwarding': url_forwarding,
               }
    return render(request, 'account/profile_password_shared.html', context)

def password_get(request, forwarding):
    #entry from the link
    decode_forwarding = decode_function(forwarding) #decode forwarding
    time_end_str = ((decode_forwarding.split('=#='))[1].split('=#=')[0]) #get the date from the link, format-str
    time_end = parser.parse(time_end_str) #change str data to data field
    id_object = ((decode_forwarding.split('=@='))[1].split('=@=')[0]) #get the object pk to display from forwarding
    #check link is actual
    now = datetime.datetime.now()
    if time_end > now:
        data_valuation = True
    else:
        data_valuation = False
    #receive instances of the object from decrypted data
    object = get_object_or_404(PasswordObject, pk=int(id_object))

    context = {'time_end': time_end,
               'object': object,
               'data_valuation': data_valuation}
    return render(request, 'account/password_get.html', context)