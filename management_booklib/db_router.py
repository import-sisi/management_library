class MongoDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'mongo_app':
            return 'mongo'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'mongo_app':
            return 'mongo'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        db_obj1 = hints.get('instance') if 'instance' in hints else obj1._state.db
        db_obj2 = hints.get('instance') if 'instance' in hints else obj2._state.db
        if db_obj1 is not None and db_obj2 is not None and db_obj1 == db_obj2:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'mongo_app':
            return db == 'mongo'
        return db == 'default'