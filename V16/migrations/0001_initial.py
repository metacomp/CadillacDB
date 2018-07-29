# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='V16_AuthGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80)),
            ],
            options={
                'db_table': 'V16_auth_group',
            },
        ),
        migrations.CreateModel(
            name='V16_AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_id', models.IntegerField()),
                ('permission_id', models.IntegerField()),
            ],
            options={
                'db_table': 'V16_auth_group_permissions',
            },
        ),
        migrations.CreateModel(
            name='V16_AuthPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('content_type_id', models.IntegerField()),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'V16_auth_permission',
            },
        ),
        migrations.CreateModel(
            name='V16_AuthUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(null=True, blank=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(unique=True, max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'V16_auth_user',
            },
        ),
        migrations.CreateModel(
            name='V16_AuthUserGroups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField()),
                ('group_id', models.IntegerField()),
            ],
            options={
                'db_table': 'V16_auth_user_groups',
            },
        ),
        migrations.CreateModel(
            name='V16_AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField()),
                ('permission_id', models.IntegerField()),
            ],
            options={
                'db_table': 'V16_auth_user_user_permissions',
            },
        ),
        migrations.CreateModel(
            name='V16_Cardetails',
            fields=[
                ('carid', models.CharField(max_length=30, serialize=False, primary_key=True, db_column='id')),
                ('caryear', models.IntegerField(db_column='CarYear')),
                ('carnum', models.IntegerField(db_column='CarNum')),
                ('title', models.CharField(max_length=30, null=True, db_column='Title', blank=True)),
                ('content', models.TextField(null=True, db_column='Content', blank=True)),
                ('createdby', models.CharField(max_length=50, null=True, db_column='CreatedBy', blank=True)),
                ('createdate', models.DateTimeField(null=True, db_column='CreateDate', blank=True)),
                ('lastupdatedate', models.DateTimeField(null=True, db_column='LastUpdateDate', blank=True)),
                ('jalbumlink', models.CharField(max_length=100, null=True, db_column='JAlbumLink', blank=True)),
            ],
            options={
                'ordering': ['caryear', 'carnum'],
                'db_table': 'V16_CarDetails',
            },
        ),
        migrations.CreateModel(
            name='V16_Cardetailsupdate',
            fields=[
                ('updateid', models.CharField(max_length=10, serialize=False, primary_key=True, db_column='UpdateId')),
                ('caryear', models.IntegerField(null=True, db_column='CarYear', blank=True)),
                ('carnum', models.IntegerField(null=True, db_column='CarNum', blank=True)),
                ('title', models.CharField(max_length=30, null=True, db_column='Title', blank=True)),
                ('content', models.TextField(null=True, db_column='Content', blank=True)),
                ('createdby', models.CharField(max_length=50, null=True, db_column='CreatedBy', blank=True)),
                ('createdate', models.DateTimeField(null=True, db_column='CreateDate', blank=True)),
                ('lastupdatedate', models.DateTimeField(null=True, db_column='LastUpdateDate', blank=True)),
                ('jalbumlink', models.CharField(max_length=500, null=True, db_column='JAlbumLink', blank=True)),
                ('carid', models.ForeignKey(to='V16.V16_Cardetails', db_column='CarID')),
            ],
            options={
                'db_table': 'V16_CarDetailsUpdate',
            },
        ),
        migrations.CreateModel(
            name='V16_Carimages',
            fields=[
                ('carid', models.CharField(default=' ', max_length=30, db_column='id')),
                ('carcategory', models.CharField(max_length=30, db_column='CarCategory')),
                ('caryear', models.IntegerField(db_column='CarYear')),
                ('carnum', models.IntegerField(db_column='CarNum')),
                ('imagenum', models.IntegerField(serialize=False, primary_key=True, db_column='ImageNum')),
                ('imagepath', models.CharField(max_length=500, null=True, db_column='ImagePath', blank=True)),
                ('description', models.TextField(null=True, db_column='Description', blank=True)),
                ('createdby', models.CharField(max_length=50, null=True, db_column='CreatedBy', blank=True)),
                ('createdate', models.DateTimeField(null=True, db_column='CreateDate', blank=True)),
                ('lastupdatedate', models.DateTimeField(null=True, db_column='LastUpdateDate', blank=True)),
            ],
            options={
                'db_table': 'V16_CarImages',
            },
        ),
        migrations.CreateModel(
            name='V16_Chapters',
            fields=[
                ('chapterid', models.IntegerField(serialize=False, primary_key=True, db_column='ChapterID')),
                ('chaptername', models.CharField(max_length=50, null=True, db_column='ChapterName', blank=True)),
                ('description', models.CharField(max_length=150, null=True, db_column='Description', blank=True)),
                ('imagepath', models.CharField(max_length=150, null=True, db_column='ImagePath', blank=True)),
                ('url', models.CharField(max_length=150, null=True, db_column='url', blank=True)),
                ('superchapterid', models.ForeignKey(to='V16.V16_Chapters', db_column='SuperChapterID')),
            ],
            options={
                'db_table': 'V16_Chapters',
            },
        ),
        migrations.CreateModel(
            name='V16_DjangoAdminLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(null=True, blank=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
                ('content_type_id', models.IntegerField(null=True, blank=True)),
                ('user_id', models.IntegerField()),
            ],
            options={
                'db_table': 'V16_django_admin_log',
            },
        ),
        migrations.CreateModel(
            name='V16_DjangoContentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'V16_django_content_type',
            },
        ),
        migrations.CreateModel(
            name='V16_DjangoMigrations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'V16_django_migrations',
            },
        ),
        migrations.CreateModel(
            name='V16_DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'V16_django_session',
            },
        ),
        migrations.AlterUniqueTogether(
            name='v16_djangocontenttype',
            unique_together=set([('app_label', 'model')]),
        ),
        migrations.AddField(
            model_name='v16_cardetails',
            name='chapterid',
            field=models.ForeignKey(to='V16.V16_Chapters', db_column='ChapterID'),
        ),
        migrations.AlterUniqueTogether(
            name='v16_authuseruserpermissions',
            unique_together=set([('user_id', 'permission_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='v16_authusergroups',
            unique_together=set([('user_id', 'group_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='v16_authpermission',
            unique_together=set([('content_type_id', 'codename')]),
        ),
        migrations.AlterUniqueTogether(
            name='v16_authgrouppermissions',
            unique_together=set([('group_id', 'permission_id')]),
        ),
    ]
