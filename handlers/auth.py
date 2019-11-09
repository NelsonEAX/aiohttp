import json

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from model import get_user_by_email, get_user_rules


async def view_auth(request):
    '''
    :param request: get-запрос /auth
    :return: Контент страницы /auth
    '''
    try:
        context = {}
        session = await get_session(request)
        if session.get('email', None) is not None:
            context['email'] = session['email']

        response = aiohttp_jinja2.render_template('auth.html', request, context)
        response.headers['Content-Language'] = 'ru'
        return response

    except Exception as e:
        print('[get_auth] except ', e)
        return web.Response(text=json.dumps({'status': 'error', 'message': str(e)}), status=500)


async def post_auth_singin(request):
    '''
    Авторизация на сайте
    :param request: post содержит поля email и password
    :return: статус и сервисное сообщение
    '''
    try:
        # Получаем и проверям данные для входа
        post = await request.json()
        if post['email'] is None or post['password'] is None:
            raise Warning('Данные указаны неверно')

        user = await get_user_by_email(engine=request.app['pg_engine'], email=post['email'])

        # TODO: Так пароли хранить и проверять НЕЛЬЗЯ
        # Найден пользователь and пароли совпадают and пользователь не удален
        if user is None or post['password'] != user['password'] or user['delete_at'] is not None:
            raise Warning('Неверно указан логин или пароль')

        session = await get_session(request)
        session['id'] = user['id']
        session['email'] = user['email']
        session['rule'] = await get_user_rules(engine=request.app['pg_engine'], user_id=user['id'])

        print('[post_auth_singin] user', str(user), str(session['rule']))

        return web.Response(text=json.dumps({
            'status': 'succes',
            'message': 'ok post_auth_singin'
        }), status=200)

    except Exception as e:
        print('[post_auth_singin] except ', e)
        return web.Response(text=json.dumps({
            'status': 'error',
            'message': str(e)
        }), status=(401 if type(e).__name__ == 'Warning' else 500))


async def post_auth_singout(request):
    '''
    Очистка сессии клиента
    :param request: post-запрос
    :return: статус и сервисное сообщение
    '''
    try:
        session = await get_session(request)
        session.clear()

        return web.Response(text=json.dumps({
            'status': 'succes',
            'message': 'ok post_auth_singout'
        }), status=200)

    except Exception as e:
        print('[post_auth_singout] except ', e)
        return web.Response(text=json.dumps({
            'status': 'error',
            'message': str(e)
        }), status=500)
