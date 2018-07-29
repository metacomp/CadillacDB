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
from .models import V16_Cardetails, V16_Chapters, V16_Cardetailsupdate
from .forms import V16_RegistrationForm, V16_ContactForm, V16_ContributeForm
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import sys

def register(request):
    if request.method == 'POST':
        form = V16_RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            #login(request, user)
            return redirect('/register/success/')
    else:
        form = V16_RegistrationForm()
    variables = RequestContext(request, {'form': form})
 
    return render_to_response('V16/register.html',variables,)

def success(request):
    return render_to_response('V16/success.html',)

def logout_page(request):
    logout(request)
    return redirect('/')
    #return render_to_response('V16/homepage.html',context_instance=RequestContext(request))

def contact(request):
    if request.method == 'GET':
        form = V16_ContactForm()
    else:
        form = V16_ContactForm(request.POST)
        if form.is_valid():
            contact_name = form.cleaned_data['contact_name']
            from_email = form.cleaned_data['from_email']
            content = form.cleaned_data['content']
            try:
                send_mail(contact_name, content, from_email, ['mrcadillac@newcadillacdatabase.org'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
    return render(request, "V16/contact.html", {'form': form})

def contribute(request):
    user = request.user
    if user.is_active : 
        if request.method == 'GET':
            form = V16_ContributeForm()
        else:
            form = V16_ContributeForm(request.POST, request.FILES)
            if form.is_valid():
                contact_name = form.cleaned_data['contact_name']
                from_email = form.cleaned_data['from_email']
                content = form.cleaned_data['content']
                imagefile = request.FILES['image']
                try:
                    mail = EmailMessage("Someone Contributed an Image for Cadillac Database","Sender: "+contact_name+"\n"+"Message: "+content,from_email, ['mrcadillac@newcadillacdatabase.org'])
                    mail.attach(imagefile.name, imagefile.read(), imagefile.content_type)
                    mail.send()
                    template = 'V16/thanks.html'
                except:
                    return HttpResponse('Attachment Error')

                return render_to_response(template, {'form':form},context_instance=RequestContext(request))
        return render(request, "V16/contribute.html", {'form': form})
    else:
        return redirect('/login')


def thanks(request):
    return render_to_response('V16/thanks.html',)

def sitemap(request):
    return render_to_response('V16/sitemap.txt',)
    
def home(request):
    chapters = V16_Chapters.objects.filter(superchapterid = 1)
    chapterheading = V16_Chapters.objects.get(pk = 1)

    return render_to_response('V16/homepage.html', {'chapters':chapters, 'chapterheading':chapterheading, 'user': request.user});

def survivors(requests):
    chapters = V16_Chapters.objects.filter(superchapterid = 4)
    chapterheading = V16_Chapters.objects.get(pk = 4)

    return render_to_response('V16/chapter_template.html', {'chapters':chapters, 'chapterheading':chapterheading, 'user': requests.user});


def ebparts(requests):
    chapters = V16_Chapters.objects.filter(superchapterid = 10).order_by('chaptername')
    chapterheading = V16_Chapters.objects.get(pk = 10)
    superchapheading = chapterheading.superchapterid.chaptername
    return render_to_response('V16/chap_no_image.html', {'chapters':chapters, 'chapterheading':chapterheading, 'user': requests.user});

def ebyear(requests):
    chapters = V16_Chapters.objects.filter(superchapterid = 46).order_by('chapterid')
    chapterheading = V16_Chapters.objects.get(pk = 46)
    return render_to_response('V16/chapter_template.html', {'chapters':chapters, 'chapterheading':chapterheading, 'user': requests.user});


def statistics(request):		
    chapterheading = V16_Chapters.objects.get(chapterid=61)
    return render_to_response('V16/statistics.html',{'chapterheading': chapterheading,'user': request.user});

def cardisplay(request,year):
    cars_list = V16_Cardetails.objects.filter(caryear=year).order_by('carnum')
    endindex = V16_Cardetails.objects.count()
    chapid = 'V16'#'Year '+ str(year)
    chapterheading = V16_Chapters.objects.get(chaptername = chapid)

    print 'V16 cardisplay view'
    paginator = Paginator(cars_list, 1)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    curpage = page
    curpage1958 = page+400

    if year == '1958':
        viewupdate = V16_Cardetailsupdate.objects.filter(carnum= curpage1958).filter(caryear=year)
    else:
        viewupdate = V16_Cardetailsupdate.objects.filter(carnum=curpage).filter(caryear=year)
    
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

    return render_to_response('V16/car_template.html', { 'cars' : cars, 'chapterheading':chapterheading, 'endindex' : endindex, 'minpage':minpage, 'maxpage':maxpage, 'updateboolean':updateboolean, 'year':year, 'user': request.user}, context_instance=RequestContext(request));

def carupdates(request, year , carnum):
    update_list = V16_Cardetailsupdate.objects.filter(carnum=carnum).filter(caryear=year)
    endindex = update_list.count()
    chapid = 'Year '+ str(year)
    chapterheading = V16_Chapters.objects.get(chaptername = chapid)

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

    return render_to_response('V16/carupdate_template.html', { 'updates' : updates, 'chapterheading':chapterheading,'endindex' : endindex, 'minpage':minpage, 'maxpage':maxpage, 'user': request.user}, context_instance=RequestContext(request));
