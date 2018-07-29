from django.contrib import admin
from .models import Cardetails, Chapters, Cardetailsupdate, HistoricalImages, Historicalinformation, Cardetailspending
from EL.models import EL_Cardetails, EL_Chapters, EL_Cardetailsupdate
from V16.models import V16_Cardetails, V16_Chapters, V16_Cardetailsupdate

def mark_approved(CarDetailsPendingAdmin, request, queryset):
    queryset.update(approved='1')
    for i in queryset:
        cardetaillist = Cardetails.objects.values_list('carid', flat=True).distinct()
        if i.carid in cardetaillist:
            ob = Cardetails.objects.get(carid=i.carid)
            obj = Cardetailspending.objects.get(carid=i)
            ob.content=ob.content+obj.content
            #ob.lastupdatedate=obj.lastupdatedate
            #ob.jalbumlink=obj.jalbumlink
            ob.status=obj.status
            #ob.chapterid=obj.chapterid
            ob.save()
            obj.delete()

mark_approved.short_description = "Approve Entry and Move to Car Details"


class CarAdmin(admin.ModelAdmin):
    list_display = ('carid', 'status')
    search_fields = ['carid', 'status']
    list_filter = ['status']

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('chapterid', 'chaptername')
    search_fields = ['chaptername', 'chaptername']
    
class CarDetailsPendingAdmin(admin.ModelAdmin):
    list_display = ('carid', 'status', 'approved')
    search_fields = ['carid', 'status']
    list_filter = ['approved', 'status']
    actions = [mark_approved]

admin.site.register(Cardetails, CarAdmin)
admin.site.register(Chapters, ChapterAdmin)
admin.site.register(Cardetailsupdate)
admin.site.register(EL_Cardetails)
admin.site.register(EL_Chapters)
admin.site.register(EL_Cardetailsupdate)
admin.site.register(V16_Cardetails)
admin.site.register(V16_Chapters)
admin.site.register(V16_Cardetailsupdate)
admin.site.register(Cardetailspending, CarDetailsPendingAdmin)
admin.site.register(Historicalinformation)
admin.site.register(HistoricalImages)