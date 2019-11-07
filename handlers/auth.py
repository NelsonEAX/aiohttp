from aiohttp import web
from aiohttp_session import get_session
import aiohttp_jinja2
import time
import json

from model import create_table,get_user
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

    # session = await get_session(request)
    # print(str(session))
    # last_visit = session['last_visit'] if 'last_visit' in session else None
    # session['last_visit'] = time.time()
    # session['rule'] = ['admin']
    # text = 'Last visited: {}'.format(last_visit)
    # //return web.Response(text=text)

    context = {'email': '', 'name': 'Andrew', 'surname': 'Svetlov'}
    response = aiohttp_jinja2.render_template(
        'auth.html',
        request,
        context
    )
    response.headers['Content-Language'] = 'ru'
    return response


async def post_auth_singin(request):
    '''

    :param request:
    :return:
    '''
    try:
        post = await request.json()
        email = post['email']
        password = post['password']



        if post is None or password is None:
            return web.Response(text=json.dumps({
                'status': 'error',
                'message': 'Данные указаны неверно'
            }), status=401)

        # await create_table(engine=request.app['pg_engine'])
        user = await get_user(engine=request.app['pg_engine'], json=post)

        print(str(user))


        # await request.loop.create_task(create_table(engine=engine))
        # print(str(request.app['pg_engine']))


        session = await get_session(request)

        last_visit = session['last_visit'] if 'last_visit' in session else None
        session['last_visit'] = time.time()
        session['rule'] = ['admin']
        text = 'Last visited: {}'.format(last_visit)

        return web.Response(text=json.dumps({
            'status': 'success',
            'message': 'Welcome, username'
        }), status=200)

    except Exception as e:

        return web.Response(text=json.dumps({
            'status': 'error',
            'message': str(e)
        }), status=500)