from django.contrib.admin.sites import AdminSite
from django.contrib import admin

from EB.models import AuthUser, Cardetails, Chapters, Cardetailsupdate, HistoricalImages, Historicalinformation, Cardetailspending
from V16.models import V16_Cardetails, V16_Chapters, V16_Cardetailsupdate
from EL.models import EL_Cardetails, EL_Chapters, EL_Cardetailsupdate

class BaseAdmin(AdminSite):

    def has_permission(self, request):
        return request.user.is_active

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

base_admin = BaseAdmin(name="base_admin")

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


base_admin.register(AuthUser)

base_admin.register(Cardetails, CarAdmin)
base_admin.register(Chapters, ChapterAdmin)
base_admin.register(Cardetailsupdate)
base_admin.register(Cardetailspending, CarDetailsPendingAdmin)
base_admin.register(Historicalinformation)
base_admin.register(HistoricalImages)

base_admin.register(EL_Cardetails)
base_admin.register(EL_Chapters)
base_admin.register(EL_Cardetailsupdate)

base_admin.register(V16_Cardetails)
base_admin.register(V16_Chapters)
base_admin.register(V16_Cardetailsupdate)