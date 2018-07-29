# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.template.loader import get_template
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.core.mail import EmailMultiAlternatives
from email.MIMEImage import MIMEImage
from .models import EL_Cardetails, EL_Chapters, EL_Cardetailsupdate
from .forms import EL_RegistrationForm, EL_ContactForm, EL_ContributeForm
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import sys

def register(request):
    if request.method == 'POST':
        form = EL_RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            #login(request, user)
            return redirect('/register/success/')
    else:
        form = EL_RegistrationForm()
    variables = RequestContext(request, {'form': form})
 
    return render_to_response('EL/register.html',variables,)

def success(request):
    return render_to_response('EL/success.html',)

def logout_page(request):
    logout(request)
    return redirect('/')
    #return render_to_response('EL/homepage.html',context_instance=RequestContext(request))

def contact(request):
    if request.method == 'GET':
        form = EL_ContactForm()
    else:
        form = EL_ContactForm(request.POST)
        if form.is_valid():
            contact_name = form.cleaned_data['contact_name']
            from_email = form.cleaned_data['from_email']
            content = form.cleaned_data['content']
            try:
                send_mail(contact_name, content, from_email, ['mrcadillac@newcadillacdatabase.org'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
    return render(request, "EL/contact.html", {'form': form})

def contribute(request):
    user = request.user
    if user.is_active : 
	    if request.method == 'GET':
	        form = EL_ContributeForm()
	    else:
	        form = EL_ContributeForm(request.POST, request.FILES)
	        if form.is_valid():
	            contact_name = form.cleaned_data['contact_name']
	            from_email = form.cleaned_data['from_email']
	            content = form.cleaned_data['content']
	            imagefile = request.FILES['image']
	            try:
   		    	mail = EmailMessage("Someone Contributed an Image for Cadillac Database","Sender: "+contact_name+"\n"+"Message: "+content,from_email, ['mrcadillac@newcadillacdatabase.org'])
    		    	mail.attach(imagefile.name, imagefile.read(), imagefile.content_type)
	            	mail.send()
	            	template = 'EL/thanks.html'
	            except:
	            	return HttpResponse('Attachment Error')

        	    return render_to_response(template, {'form':form},context_instance=RequestContext(request))
	    return render(request, "EL/contribute.html", {'form': form})
    else:
        return redirect('/login')


def thanks(request):
    return render_to_response('EL/thanks.html',)

def sitemap(request):
    return render_to_response('EL/sitemap.txt',)
    
def home(request):
    chapters = EL_Chapters.objects.filter(superchapterid = 1)
    chapterheading = EL_Chapters.objects.get(pk = 1)

    return render_to_response('EL/homepage.html', {'chapters':chapters, 'chapterheading':chapterheading, 'user': request.user});

def survivors(requests):
    chapters = EL_Chapters.objects.filter(superchapterid = 4)
    chapterheading = EL_Chapters.objects.get(pk = 4)

    return render_to_response('EL/chapter_template.html', {'chapters':chapters, 'chapterheading':chapterheading, 'user': requests.user});

def ebparts(requests):
    chapters = EL_Chapters.objects.filter(superchapterid = 10).order_by('chaptername')
    chapterheading = EL_Chapters.objects.get(pk = 10)
    superchapheading = chapterheading.superchapterid.chaptername
    return render_to_response('EL/chap_no_image.html', {'chapters':chapters, 'chapterheading':chapterheading, 'user': requests.user});

def ebyear(requests):
    chapters = EL_Chapters.objects.filter(superchapterid = 46).order_by('chapterid')
    chapterheading = EL_Chapters.objects.get(pk = 46)
    return render_to_response('EL/chapter_template.html', {'chapters':chapters, 'chapterheading':chapterheading, 'user': requests.user});

def statistics(request):		
	chapterheading = EL_Chapters.objects.get(chapterid=61)
	return render_to_response('EL/statistics.html',{'chapterheading': chapterheading,'user': request.user});

def cardisplay(request,year):
    cars_list = EL_Cardetails.objects.filter(caryear=year).order_by('carnum')
    endindex = EL_Cardetails.objects.count()
    chapid = 'Year '+ str(year)
    chapterheading = EL_Chapters.objects.get(chaptername = chapid)

    print 'EL cardisplay view'
    paginator = Paginator(cars_list, 1)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    curpage = page
    curpage1958 = page+400

    if year == '1958':
    	viewupdate = EL_Cardetailsupdate.objects.filter(carnum= curpage1958).filter(caryear=year)
    else:
    	viewupdate = EL_Cardetailsupdate.objects.filter(carnum=curpage).filter(caryear=year)
    
    if viewupdate.exists():
        updateboolean = True
    else:
        updateboolean = False


    try:
        cars = paginator.page(page)
    except(EmptyPage, InvalidPage):
        cars = paginator.page(paginator.num_pages)
    
    if cars.number < 5:
    	minpage = 1
    	maxpage = (5 - cars.number) + 5 + cars.number
    elif cars.number > (endindex - 5):
    	minpage = cars.number - ((5 - (endindex - cars.number)) + 5)
    	maxpage = endindex
    else:
	    minpage = cars.number - 5
	    maxpage = cars.number + 5

    return render_to_response('EL/car_template.html', { 'cars' : cars, 'chapterheading':chapterheading, 'endindex' : endindex, 'minpage':minpage, 'maxpage':maxpage, 'updateboolean':updateboolean, 'year':year, 'user': request.user}, context_instance=RequestContext(request));

def carupdates(request, year , carnum):
    update_list = EL_Cardetailsupdate.objects.filter(carnum=carnum).filter(caryear=year)
    endindex = update_list.count()
    chapid = 'Year '+ str(year)
    chapterheading = EL_Chapters.objects.get(chaptername = chapid)

    paginator = Paginator(update_list, 1)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1


    try:
        updates = paginator.page(page)
    except(EmptyPage, InvalidPage):
        updates = paginator.page(paginator.num_pages)
    
    if updates.number < 6:
        minpage = 1
        maxpage = (6 - updates.number) + 6 + updates.number
    elif updates.number > (endindex - 6):
        minpage = updates.number - ((6 - (endindex - updates.number)) + 6)
        maxpage = endindex
    else:
        minpage = updates.number - 6
        maxpage = updates.number + 6

    return render_to_response('EL/carupdate_template.html', { 'updates' : updates, 'chapterheading':chapterheading,'endindex' : endindex, 'minpage':minpage, 'maxpage':maxpage, 'user': request.user}, context_instance=RequestContext(request));