from django.conf import settings
 
class DatabaseAppsRouter(object):

    def db_for_read(self, model, **hints):
        if not settings.DATABASES.has_key('EL'):
            return None
        if model._meta.app_label == 'EL':
            return 'EL'
        return None

    def db_for_write(self, model, **hints):
        if not settings.DATABASES.has_key('EL'):
            return None
        if model._meta.app_label == 'EL':
            return 'EL'
        return None

    def allow_syncdb(self, db, model):
        if not settings.DATABASES.has_key('EL'):
            return None
        if db == 'EL_newcadillac':
            return model._meta.app_label == 'EL'
        elif model._meta.app_label == 'EL':
            return False
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        if not settings.DATABASES.has_key('EL'):
            return None
        if obj1._meta.app_label == 'EL' or obj2._meta.app_label == 'EL':
            return True
        return None