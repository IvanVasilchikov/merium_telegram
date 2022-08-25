from peewee import *

db = SqliteDatabase('sql.db')


class Users(Model):
    phone = CharField(default="")
    estate_type = CharField(default="")
    estate_type_id = IntegerField(default=0)
    budget = CharField(default="")
    repair = CharField(default="")
    zagorod_place = CharField(default="")
    city_type = CharField(default="")
    city_apartment_type = CharField(default="")
    telegram_id = IntegerField(default=0)

    class Meta:
        database = db


db.connect()
db.create_tables([Users])


def add_user(id):
    user = Users.get_or_create(telegram_id=id)


def set_user_estate_type(id, type, type_id):
    user = Users.get(Users.telegram_id == id)
    user.estate_type = type
    user.estate_type_id = type_id
    user.save()

def set_user_repair(id, repair):
    user = Users.get(Users.telegram_id == id)
    user.repair = repair
    user.save()

def set_user_zagorod_place(id,place):
    user = Users.get(Users.telegram_id == id)
    user.zagorod_place = place
    user.save()

def set_user_budget(id,budget):
    user = Users.get(Users.telegram_id == id)
    user.budget = budget
    user.save()

def set_user_city_type(id,city_type):
    user = Users.get(Users.telegram_id == id)
    user.city_type = city_type
    user.save()

def set_user_city_apartment_type(id,city_apartment_type):
    user = Users.get(Users.telegram_id == id)
    user.city_apartment_type = city_apartment_type
    user.save()

def set_user_phone(id,phone):
    user = Users.get(Users.telegram_id == id)
    user.phone = phone
    user.save()