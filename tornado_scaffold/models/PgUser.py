# encoding: utf-8

from peewee import *
from PgBaseModel import *


class User(PgBaseModel):
    uuid = UUIDField(unique=True)
    username = CharField()
    avatar = CharField(null=True)
    email = CharField(null=True)
    mobile = CharField(null=True)
    password = CharField(null=True)
    last_login_ip = CidrField(null=True)
    last_login_at = DateTimeField(null=True)
    created_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        db_table = 'users'