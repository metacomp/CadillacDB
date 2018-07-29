from django.conf import settings
 
class DatabaseAppsRouter(object):

    def db_for_read(self, model, **hints):
        if not settings.DATABASES.has_key('V16'):
            return None
        if model._meta.app_label == 'V16':
            return 'V16'
        return None

    def db_for_write(self, model, **hints):
        if not settings.DATABASES.has_key('V16'):
            return None
        if model._meta.app_label == 'V16':
            return 'V16'
        return None

    def allow_syncdb(self, db, model):
        if not settings.DATABASES.has_key('V16'):
            return None
        if db == 'V16_newcadillac':
            return model._meta.app_label == 'V16'
        elif model._meta.app_label == 'V16':
            return False
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        if not settings.DATABASES.has_key('V16'):
            return None
        if obj1._meta.app_label == 'V16' or obj2._meta.app_label == 'V16':
            return True
        return None