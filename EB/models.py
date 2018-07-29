# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desidered behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator

CARDETAILSTATUS = (
        (0, 'Pending'),
        (1, 'Approved')
)


class Chapters(models.Model):
    chapterid = models.IntegerField(db_column='ChapterID', primary_key=True)  # Field name made lowercase.
    chaptername = models.CharField(db_column='ChapterName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=150, blank=True, null=True)  # Field name made lowercase.
    superchapterid = models.ForeignKey('self', db_column='SuperChapterID')  # Field name made lowercase.
    imagepath = models.CharField(db_column='ImagePath', max_length=150, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='url', max_length=150, blank=True, null=True)

    def __str__(self):
        return self.chaptername

    class Meta:
        db_table = 'Chapters'

class Cardetails(models.Model):
    carid = models.CharField(db_column ='id', max_length=30, primary_key=True)
    caryear = models.IntegerField(db_column='CarYear')  # Field name made lowercase.
    carnum = models.IntegerField(db_column='CarNum')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=30, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    lastupdatedate = models.DateTimeField(db_column='LastUpdateDate', blank=True, null=True)  # Field name made lowercase.
    jalbumlink = models.CharField(db_column='JAlbumLink', max_length=100, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='CarStatus', max_length=30, blank=True, null=True) # Field name made lowercase.
    chapterid = models.ForeignKey(Chapters, db_column='ChapterID')  # Field name made lowercase.

    def __str__(self):
        return self.carid

    class Meta:
        db_table = 'CarDetails'
        ordering = ['caryear', 'carnum']

class Cardetailsupdate(models.Model):
    carid = models.ForeignKey(Cardetails, db_column='CarID')  # Field name made lowercase.
    updateid = models.CharField(db_column='UpdateId', primary_key=True, max_length=10)  # Field name made lowercase.
    caryear = models.IntegerField(db_column='CarYear', blank=True, null=True)  # Field name made lowercase.
    carnum = models.IntegerField(db_column='CarNum', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=30, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    lastupdatedate = models.DateTimeField(db_column='LastUpdateDate', blank=True, null=True)  # Field name made lowercase.
    jalbumlink = models.CharField(db_column='JAlbumLink', max_length=100, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.updateid

    class Meta:
        db_table = 'CarDetailsUpdate'

class Carimages(models.Model):
    carcategory = models.CharField(db_column='CarCategory', max_length=30)  # Field name made lowercase.
    caryear = models.IntegerField(db_column='CarYear')  # Field name made lowercase.
    carnum = models.IntegerField(db_column='CarNum')  # Field name made lowercase.
    imagenum = models.IntegerField(db_column='ImageNum', primary_key=True)  # Field name made lowercase.
    imagepath = models.CharField(db_column='ImagePath', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    lastupdatedate = models.DateTimeField(db_column='LastUpdateDate', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.carnum

    class Meta:
        db_table = 'CarImages'

class Cardetailspending(models.Model):
    carid = models.CharField(db_column ='id', max_length=30, primary_key=True)
    caryear = models.IntegerField(db_column='CarYear')  # Field name made lowercase.
    carnum = models.IntegerField(db_column='CarNum')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=30, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    lastupdatedate = models.DateTimeField(db_column='LastUpdateDate', blank=True, null=True)  # Field name made lowercase.
    jalbumlink = models.CharField(db_column='JAlbumLink', max_length=100, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='CarStatus', max_length=30, blank=True, null=True) # Field name made lowercase.
    chapterid = models.CharField(db_column='ChapterID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    approved = models.IntegerField(choices=CARDETAILSTATUS, default=0, validators=[MaxValueValidator(1)])
    
    def __str__(self):
        return self.carid

    class Meta:
        db_table = 'CarDetailsPending'
        ordering = ['caryear', 'carnum']


class Historicalinformation(models.Model):
    chapterid = models.ForeignKey(Chapters, db_column='ChapterID')  # Field name made lowercase.
    sectionid = models.CharField(db_column='SectionID', primary_key=True, max_length=50)  # Field name made lowercase.
    sectionorder = models.IntegerField(db_column='SectionOrder')  # Field name made lowercase.
    sectiontitle = models.CharField(db_column='SectionTitle', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sectiontext = models.TextField(db_column='SectionText', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    lastupdatedate = models.DateTimeField(db_column='LastUpdateDate', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.sectionid
        
    class Meta:
        db_table = 'HistoricalInformation'


class HistoricalImages(models.Model):
    sectionid = models.ForeignKey(Historicalinformation, db_column='SectionID')  # Field name made lowercase.
    imageurl = models.CharField(db_column='ImageUrl', max_length=100)  # Field name made lowercase.
    imagecaption = models.CharField(db_column='ImageCaption', max_length=200, blank=True, null=True)  # Field name made lowercase.
    imageid = models.AutoField(db_column='ImageID', primary_key=True)  # Field name made lowercase.
    
    def __str__(self):
        return str(self.imageid)
        
    class Meta:
        db_table = 'Historical_Images'



class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
