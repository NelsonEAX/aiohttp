import json

import asyncio
from aiohttp import web
from aiohttp_session import session_middleware
from aiopg.sa import create_engine

import aiohttp_jinja2
import jinja2

from routes import setup_routes
from model import get_dsn, get_sekret_key, create_table
from middleware import auth_middleware, db_middleware, pg_engine_ctx


# engine = loop.run_until_complete(create_engine(get_dsn(), loop=loop))
# loop.run_until_complete(create_table(engine=engine))
#
# engine.close()
# loop.run_until_complete(engine.wait_closed())


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
    loop = asyncio.get_event_loop()

    # Инициализируем приложение,
    app = web.Application(loop=loop, middlewares=[
        session_middleware(get_sekret_key()),
        # db_middleware, # migrate to app.cleanup_ctx
        auth_middleware,
    ])

    # app.on_startup.append(create_pg_engine)
    # app.on_cleanup.append(dispose_pg_engine)
    app.cleanup_ctx.append(pg_engine_ctx)

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