import uuid
import sys
import bcrypt
import time
import json
from helper import *
from tornado_json.requesthandlers import APIHandler
from models.PgUser import User
from playhouse.shortcuts import model_to_dict


class UserAPIHandler(APIHandler):
    __url_names__ = ["user"]


class ListHandler(UserAPIHandler):

    def get(self):
        page = int(self.get_argument("page", 1))
        per_page = int(self.get_argument("per_page", 10))
        query = User.select().order_by(-User.id).paginate(page, per_page)
        users = []
        for user in query:
            rs = model_to_dict(user)
            # json.dumps 太弱了，居然不能转换时间类型和UUID
            rs["uuid"] = rs["uuid"].__str__()
            rs["created_at"] = time_fmt(rs["created_at"])
            rs["updated_at"] = time_fmt(rs["updated_at"])
            rs["last_login_at"] = time_fmt(rs["last_login_at"])
            del rs['password']
            users.append(rs)
        self.success(users)

    def post(self):
        salt = bcrypt.gensalt(10)
        password = self.get_argument("password").encode('ascii')
        hashed = bcrypt.hashpw(password, salt)
        now = time_fmt()
        # print(bcrypt.checkpw(password, hashed))
        x_real_ip = self.request.headers.get("X-Real-IP")
        remote_ip = x_real_ip or self.request.remote_ip
        data = {
            "username": self.get_argument("username"),
            "email": self.get_argument("email"),
            "mobile": self.get_argument("mobile"),
            "password": hashed,
            "uuid": uuid.uuid1().__str__(),
            "created_at" : now,
            "updated_at": now,
            "last_login_at": now,
            "last_login_ip": remote_ip
        }
        user = User.create(**data)
        rs = model_to_dict(user)
        del rs['password']
        self.success(rs)


class LoginHandler(APIHandler):
    __url_names__ = ["login"]

    def get(self):
         self.success("login")