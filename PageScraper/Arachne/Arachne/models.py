from peewee import *

#TODO change
database = SqliteDatabase('C:/Users/Kanan-PC/PycharmProjects/DjangoScrapy/WordCount/db.wordcount', **{})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class AuthGroup(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'auth_group'

class DjangoContentType(BaseModel):
    app_label = CharField()
    model = CharField()

    class Meta:
        db_table = 'django_content_type'
        indexes = (
            (('app_label', 'model'), True),
        )

class AuthPermission(BaseModel):
    codename = CharField()
    content_type = ForeignKeyField(db_column='content_type_id', rel_model=DjangoContentType, to_field='id')
    name = CharField()

    class Meta:
        db_table = 'auth_permission'
        indexes = (
            (('content_type', 'codename'), True),
        )

class AuthGroupPermissions(BaseModel):
    group = ForeignKeyField(db_column='group_id', rel_model=AuthGroup, to_field='id')
    permission = ForeignKeyField(db_column='permission_id', rel_model=AuthPermission, to_field='id')

    class Meta:
        db_table = 'auth_group_permissions'
        indexes = (
            (('group', 'permission'), True),
        )

class AuthUser(BaseModel):
    date_joined = DateTimeField()
    email = CharField()
    first_name = CharField()
    is_active = BooleanField()
    is_staff = BooleanField()
    is_superuser = BooleanField()
    last_login = DateTimeField(null=True)
    last_name = CharField()
    password = CharField()
    username = CharField(unique=True)

    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(BaseModel):
    group = ForeignKeyField(db_column='group_id', rel_model=AuthGroup, to_field='id')
    user = ForeignKeyField(db_column='user_id', rel_model=AuthUser, to_field='id')

    class Meta:
        db_table = 'auth_user_groups'
        indexes = (
            (('user', 'group'), True),
        )

class AuthUserUserPermissions(BaseModel):
    permission = ForeignKeyField(db_column='permission_id', rel_model=AuthPermission, to_field='id')
    user = ForeignKeyField(db_column='user_id', rel_model=AuthUser, to_field='id')

    class Meta:
        db_table = 'auth_user_user_permissions'
        indexes = (
            (('user', 'permission'), True),
        )

class DjangoAdminLog(BaseModel):
    action_flag = IntegerField()
    action_time = DateTimeField()
    change_message = TextField()
    content_type = ForeignKeyField(db_column='content_type_id', null=True, rel_model=DjangoContentType, to_field='id')
    object = TextField(db_column='object_id', null=True)
    object_repr = CharField()
    user = ForeignKeyField(db_column='user_id', rel_model=AuthUser, to_field='id')

    class Meta:
        db_table = 'django_admin_log'

class DjangoMigrations(BaseModel):
    app = CharField()
    applied = DateTimeField()
    name = CharField()

    class Meta:
        db_table = 'django_migrations'

class DjangoSession(BaseModel):
    expire_date = DateTimeField(index=True)
    session_data = TextField()
    session_key = CharField(primary_key=True)

    class Meta:
        db_table = 'django_session'

class MainWord(BaseModel):
    gender = CharField(null=True)
    word = CharField(primary_key=True)

    class Meta:
        db_table = 'main_word'

class MainEnglishword(BaseModel):
    english = CharField()
    word = ForeignKeyField(db_column='word_id', rel_model=MainWord, to_field='word')

    class Meta:
        db_table = 'main_englishword'

class MainName(BaseModel):
    gender = CharField()
    name = CharField(primary_key=True)

    class Meta:
        db_table = 'main_name'

class MainSite(BaseModel):
    checked_date = DateTimeField(null=True)
    site = CharField(primary_key=True)

    class Meta:
        db_table = 'main_site'

class MainNamesoup(BaseModel):
    count = IntegerField()
    name = ForeignKeyField(db_column='name_id', rel_model=MainName, to_field='name')
    site = ForeignKeyField(db_column='site_id', rel_model=MainSite, to_field='site')

    class Meta:
        db_table = 'main_namesoup'

class MainType(BaseModel):
    word = ForeignKeyField(db_column='word_id', rel_model=MainWord, to_field='word')
    word_type = CharField()

    class Meta:
        db_table = 'main_type'

class MainWordsoup(BaseModel):
    count = IntegerField()
    site = ForeignKeyField(db_column='site_id', rel_model=MainSite, to_field='site')
    word = ForeignKeyField(db_column='word_id', rel_model=MainWord, to_field='word')

    class Meta:
        db_table = 'main_wordsoup'

class SqliteSequence(BaseModel):
    name = UnknownField(null=True)  # 
    seq = UnknownField(null=True)  # 

    class Meta:
        db_table = 'sqlite_sequence'

