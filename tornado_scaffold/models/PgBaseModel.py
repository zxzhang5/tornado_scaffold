# encoding: utf-8
from helper import *
import ConfigParser
from peewee import PostgresqlDatabase, Field, Model

env = read_env()
dbname = env.get('POSTGRESQL', 'PG_DATABASE')
pgdb = PostgresqlDatabase(dbname, **{
    'host': env.get('POSTGRESQL', 'PG_HOST'),
    'port': env.get('POSTGRESQL', 'PG_PORT'),
    'user': env.get('POSTGRESQL', 'PG_USERNAME'),
    'password': env.get('POSTGRESQL', 'PG_PASSWORD'),
})


class CidrField(Field):
    db_field = 'cidr'

    def db_value(self, value):
        return str(value)

    def python_value(self, value):
        return value


class PgBaseModel(Model):
    class Meta:
        database = pgdb