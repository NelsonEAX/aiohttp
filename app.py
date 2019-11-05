import json
import base64
from cryptography import fernet

import asyncio
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

import aiohttp_jinja2
import jinja2

from routes import setup_routes
from model import *
from middleware import auth_middleware, db_middleware

loop = asyncio.get_event_loop()
engine = loop.run_until_complete(create_engine(dsn, loop=loop))
loop.run_until_complete(create_table(engine=engine))

engine.close()
loop.run_until_complete(engine.wait_closed())


# loop = asyncio.get_event_loop()
# routes = web.RouteTableDef()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(go(9))
# loop.run_until_complete(go(10))



def make_app():
    '''
    Инициализация приложения, установка сессии, установка шаблонов, добавление роутов
    :return:
    '''

    # Инициализируем приложение,
    app = web.Application(loop=loop, middlewares=[
        session_middleware(EncryptedCookieStorage(base64.urlsafe_b64decode('kGVpDE_X9rNsyJfQTLKSK65FoXAZ7bJ3nfALpt6oCZs='))),
        auth_middleware,
        # db_middleware,
    ])

    # secret_key must be 32 url-safe base64-encoded bytes
    # fernet_key = fernet.Fernet.generate_key()
    # print(fernet_key)
    # secret_key = base64.urlsafe_b64decode(fernet_key)
    # print(secret_key.decode('cp1251'))
    # setup(app, EncryptedCookieStorage(secret_key))

    # Указываем шаблонизатору папку с html-шаблонами
    aiohttp_jinja2.setup(app,
        loader=jinja2.FileSystemLoader('templates'))

    # Устанавливаем роуты
    setup_routes(app)

    return app

web.run_app(make_app())