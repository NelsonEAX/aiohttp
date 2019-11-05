import json
import time
import base64
from cryptography import fernet


import asyncio
from aiohttp import web
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

import aiohttp_jinja2
import jinja2


from model import *

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

# @routes.get('/')
# @routes.get('/index')
# @aiohttp_jinja2.template('index.html')
async def get_index(request):
    '''

    :param request:
    :return:
    '''
    # responce_obj = { 'status': 'success' }
    # return web.Response(text=json.dumps(responce_obj), status=200)
    context = {'name': 'Andrew', 'surname': 'Svetlov'}
    response = aiohttp_jinja2.render_template('index.html',
                                              request,
                                              context)
    response.headers['Content-Language'] = 'ru'
    return response

# @routes.get('/auth')
# @aiohttp_jinja2.template('auth.html')
async def get_auth(request):
    '''

    :param request:
    :return:
    '''
    # try:
    #     user = request.query['name']
    #     print('Creating a new user with name: ', user)
    #
    #     responce_obj = {'status': 'success', 'message': 'user successfully created'}
    #     return web.Response(text=json.dumps(responce_obj), status=200)
    # except Exception as e:
    #     responce_obj = {'status': 'success', 'message': str(e)}
    #     return web.Response(text=json.dumps(responce_obj), status=500)

    session = await get_session(request)
    print(str(session))
    # last_visit = session['last_visit'] if 'last_visit' in session else None
    session['last_visit'] = time.time()
    # text = 'Last visited: {}'.format(last_visit)
    # //return web.Response(text=text)

    context = {'name': 'Andrew', 'surname': 'Svetlov'}
    response = aiohttp_jinja2.render_template('auth.html',
                                              request,
                                              context)
    response.headers['Content-Language'] = 'ru'
    return response


# @routes.get('/table')
# @aiohttp_jinja2.template('table.html')
async def get_table(request):
    '''

    :param request:
    :return:
    '''

    # responce_obj = {'status': 'success'}
    # return web.Response(text=json.dumps(responce_obj), status=200)
    context = {
        'name': 'Admin',
        'rule': ['admin', 'editor'],
        'items': [
            {'id': '1', 'email': 'email_1', 'name': 'name_1', 'surname': 'surname_1'},
            {'id': '2', 'email': 'email_2', 'name': 'name_2', 'surname': 'surname_2'},
            {'id': '3', 'email': 'email_3', 'name': 'name_3', 'surname': 'surname_3'},
            {'id': '4', 'email': 'email_4', 'name': 'name_4', 'surname': 'surname_4'}
        ]
    }
    response = aiohttp_jinja2.render_template('table.html',
                                              request,
                                              context)
    response.headers['Content-Language'] = 'ru'
    return response


def make_app():
    '''
    Инициализация приложения, установка сессии, установка шаблонов, добавление роутов
    :return:
    '''
    app = web.Application()
    # secret_key must be 32 url-safe base64-encoded bytes
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    # print(secret_key.decode('utf8'))
    setup(app, EncryptedCookieStorage(secret_key))


    # app = web.Application()

    aiohttp_jinja2.setup(app,
        loader=jinja2.FileSystemLoader('templates'))

    # app.add_routes(routes)
    app.router.add_get('/', get_index)
    app.router.add_get('/index', get_index)
    app.router.add_get('/auth', get_auth)
    app.router.add_get('/table', get_table)

    return app

web.run_app(make_app())