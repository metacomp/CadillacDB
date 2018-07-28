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
from .models import AuthUser, Cardetails, Chapters, Cardetailsupdate, Historicalinformation, HistoricalImages
from .forms import RegistrationForm, ContactForm, ContributeForm
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from decimal import Decimal
import sys

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            #login(request, user)
            return redirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
 
    return render_to_response('EB/register.html',variables,)

def success(request):
    return render_to_response('EB/success.html',)

def logout_page(request):
    logout(request)
    return redirect('/')
    #return render_to_response('EB/homepage.html',context_instance=RequestContext(request))

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_name = form.cleaned_data['contact_name']
            from_email = form.cleaned_data['from_email']
            content = form.cleaned_data['content']
            try:
                send_mail(contact_name, content, from_email, ['mrcadillac@newcadillacdatabase.org'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
    return render(request, "EB/contact.html", {'form': form})

def contribute(request):
    user = request.user
    if user.is_active : 
	    if request.method == 'GET':
	        form = ContributeForm()
	    else:
	        form = ContributeForm(request.POST, request.FILES)
	        if form.is_valid():
	            contact_name = form.cleaned_data['contact_name']
	            from_email = form.cleaned_data['from_email']
	            content = form.cleaned_data['content']
	            imagefile = request.FILES['image']
	            try:
   		    	mail = EmailMessage("Someone Contributed an Image for Cadillac Database","Sender: "+contact_name+"\n"+"Message: "+content,from_email, ['mrcadillac@newcadillacdatabase.org'])
    		    	mail.attach(imagefile.name, imagefile.read(), imagefile.content_type)
	            	mail.send()
	            	template = 'EB/thanks.html'
	            except:
	            	return HttpResponse('Attachment Error')

        	    return render_to_response(template, {'form':form},context_instance=RequestContext(request))
	    return render(request, "EB/contribute.html", {'form': form})
    else:
        return redirect('/login')


def thanks(request):
    return render_to_response('EB/thanks.html',)

def sitemap(request):
    return render_to_response('EB/sitemap.txt',)
    
def home(request):
    chapters = Chapters.objects.filter(superchapterid = 1)
    chapterheading = Chapters.objects.get(pk = 1)

    return render_to_response('EB/homepage.html', {'chapters':chapters, 'chapterheading':chapterheading, 'user': request.user});

def survivors(requests):
    chapters = Chapters.objects.filter(superchapterid = 4)
    chapterheading = Chapters.objects.get(pk = 4)

    return render_to_response('EB/chapter_template.html', {'chapters':chapters, 'chapterheading':chapterheading, 'user': requests.user});

def historical(requests):
    chapters = Chapters.objects.filter(superchapterid = 3)
    chapterheading = Chapters.objects.get(pk = 3)

    return render_to_response('EB/chapter_template.html', {'chapters':chapters, 'chapterheading':chapterheading, 'user': requests.user});

def ebparts(requests):
    #if " Survivors" in chapterheading.superchapterid.chaptername:
    #    return render_to_response('EB/chapter_template.html',)
    #else:
        chapters = Chapters.objects.filter(superchapterid = 10).order_by('chaptername')
        chapterheading = Chapters.objects.get(pk = 10)
        superchapheading = chapterheading.superchapterid.chaptername
        return render_to_response('EB/chap_no_image.html', {'chapters':chapters, 'chapterheading':chapterheading, 'user': requests.user});

def ebyear(requests):
    chapters = Chapters.objects.filter(superchapterid = 60).order_by('chapterid')
    chapterheading = Chapters.objects.get(pk = 60)
    superchapheading = chapterheading.superchapterid.chaptername
    return render_to_response('EB/chapter_template.html', {'chapters':chapters, 'chapterheading':chapterheading, 'user': requests.user});
	

def statistics(request):		
    #chapterheading = Chapters.objects.get(chapterid=61)
    chapterheading = Chapters.objects.get(pk = 61)
    superchapheading = chapterheading.superchapterid.chaptername
    EB57s = Decimal(Cardetails.objects.all().filter(caryear="1957", status__in=["Survivor","Parts"]).count())
    EB57s_Ratio = Decimal(EB57s/400)
    EB57s_Ratio = round(EB57s_Ratio,2)*100
    EB58s = Decimal(Cardetails.objects.all().filter(caryear="1958", status__in=["Survivor","Parts"]).count())
    EB58s_Ratio = Decimal(EB58s/304)
    EB58s_Ratio = round(EB58s_Ratio,2)*100
    EB5758s = Decimal(EB57s+EB58s)
    EB5758s_Ratio = Decimal(EB5758s/704)
    EB5758s_Ratio = round(EB5758s_Ratio,2)*100
    EB59s = Decimal(Cardetails.objects.all().filter(caryear="1959", status__in=["Survivor","Parts"]).count())
    EB59s_Ratio = Decimal(EB59s/99)
    EB59s_Ratio = round(EB59s_Ratio,2)*100
    EB60s = Decimal(Cardetails.objects.all().filter(caryear="1960", status__in=["Survivor","Parts"]).count())
    EB60s_Ratio = Decimal(EB60s/101)
    EB60s_Ratio = round(EB60s_Ratio,2)*100
    EB5960s = Decimal(EB59s+EB60s)
    EB5960s_Ratio = Decimal(EB5960s/200)
    EB5960s_Ratio = round(EB5960s_Ratio,2)*100
    EBTotal = Decimal(EB5758s+EB5960s)
    EBTotal_Ratio = Decimal(EBTotal/904)
    EBTotal_Ratio = round(EBTotal_Ratio,2)*100
    return render_to_response('EB/statistics.html',{'EB57s': EB57s, 'EB57s_Ratio': EB57s_Ratio, 
                                                    'EB58s': EB58s, 'EB58s_Ratio': EB58s_Ratio,
                                                    'EB59s': EB59s, 'EB59s_Ratio': EB59s_Ratio,
                                                    'EB60s': EB60s, 'EB60s_Ratio': EB60s_Ratio,
                                                    'EB5758s': EB5758s, 'EB5758s_Ratio': EB5758s_Ratio, 
                                                    'EB5960s': EB5960s, 'EB5960s_Ratio': EB5960s_Ratio,
                                                    'EBTotal': EBTotal, 'EBTotal_Ratio': EBTotal_Ratio,
                                                    'chapterheading': chapterheading,'user': request.user});

def historicaltemplate(request, sectionorder):
    chapterheading = Chapters.objects.get(pk = 36)
    totsectionnum = Historicalinformation.objects.all().count()   
    section = Historicalinformation.objects.get(sectionorder = sectionorder)
    section_fk = section.sectionid
    sectionimages = HistoricalImages.objects.filter(sectionid = section_fk)

    return render_to_response('EB/historicaltemplate.html', {'section': section, 'chapterheading':chapterheading, 'sectionimages':sectionimages, 'totsectionnum':totsectionnum, 'user': request.user});

def cardisplay(request,year):
    cars_list = Cardetails.objects.filter(caryear=year).order_by('carnum')
    endindex = Cardetails.objects.count()
    chapid = 'Year '+ str(year)
    chapterheading = Chapters.objects.get(chaptername = chapid)


    paginator = Paginator(cars_list, 1)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    curpage = page
    curpage1958 = page+400

    if year == '1958':
    	viewupdate = Cardetailsupdate.objects.filter(carnum= curpage1958).filter(caryear=year)
    else:
    	viewupdate = Cardetailsupdate.objects.filter(carnum=curpage).filter(caryear=year)
    
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

    return render_to_response('EB/car_template.html', { 'cars' : cars, 'chapterheading':chapterheading, 'endindex' : endindex, 'minpage':minpage, 'maxpage':maxpage, 'updateboolean':updateboolean, 'year':year, 'user': request.user}, context_instance=RequestContext(request));

def carupdates(request, year , carnum):
    update_list = Cardetailsupdate.objects.filter(carnum=carnum).filter(caryear=year)
    endindex = update_list.count()
    chapid = 'Year '+ str(year)
    chapterheading = Chapters.objects.get(chaptername = chapid)

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

    return render_to_response('EB/carupdate_template.html', { 'updates' : updates, 'chapterheading':chapterheading,'endindex' : endindex, 'minpage':minpage, 'maxpage':maxpage, 'user': request.user}, context_instance=RequestContext(request));