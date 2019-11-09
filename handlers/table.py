import json

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from model import get_users, get_user_info, set_delete_at_for_user, create_user, update_user


async def view_table(request):
    '''

    :param request:
    :return:
    '''
    try:
        session = await get_session(request)
        users = await get_users(engine=request.app['pg_engine'], admin=('admin' in session['rule']))
        context = {
            'email': session['email'],
            'rule': session['rule'],
            'items': users
        }
        response = aiohttp_jinja2.render_template('table.html', request, context)
        response.headers['Content-Language'] = 'ru'
        return response

    except Exception as e:
        print('[get_table] except ', e)
        return web.Response(text=json.dumps({'status': 'error', 'message': str(e)}), status=500)


async def post_table_read(request):
    '''

    :param request:
    :return:
    '''
    try:
        # Получаем и проверям данные для входа
        post = await request.json()
        if post['id'] is None:
            raise Warning('Данные указаны неверно')

        user_info = await get_user_info(engine=request.app['pg_engine'], user_id=post['id'])
        if len(user_info) == 0:
            raise Warning('Данные указаны неверно')

        return web.Response(text=json.dumps(user_info), status=200)
    except Exception as e:
        print('[post_table_read] except ', e)
        return web.Response(text=json.dumps({'status': 'error', 'message': str(e)}), status=500)


async def post_table_create(request):
    '''

    :param request:
    :return:
    '''
    try:
        # Получаем и проверям данные для создания записи
        post = await request.json()
        if post['email'] == '' or post['password'] == '':
            raise Warning('Не заполнены обязательные поля')

        await create_user(engine=request.app['pg_engine'], data=post)

        return web.Response(text=json.dumps(post), status=200)
    except Exception as e:
        print('[post_table_create] except ', e)
        return web.Response(text=json.dumps({'status': 'error', 'message': str(e)}), status=500)


async def post_table_update(request):
    '''

    :param request:
    :return:
    '''
    try:
        # Получаем и проверям данные для обновления записи
        post = await request.json()
        if post['email'] == '' or post['password'] == '':
            raise Warning('Не заполнены обязательные поля')

        await update_user(engine=request.app['pg_engine'], data=post)

        return web.Response(text=json.dumps(post), status=200)
    except Exception as e:
        print('[post_table_update] except ', e)
        return web.Response(text=json.dumps({'status': 'error', 'message': str(e)}), status=500)


async def table_delete_restore_user(request, restore=False):
    '''

    :param request:
    :param user_id:
    :param restore:
    :return:
    '''
    print(f'[table_delete_restore_user] start {restore}')

    post = await request.json()
    if post['id'] is None:
        raise Warning('Нет id пользователя')

    session = await get_session(request)
    if session.get('id', None) == int(post['id']):
        raise Warning('Нельзя удалить собственного пользователя')

    await set_delete_at_for_user(engine=request.app['pg_engine'], user_id=int(post['id']), restore=restore)


async def post_table_restore(request):
    '''
    Восстановление записи пользователя
    :param request:
    :return:
    '''
    try:
        await table_delete_restore_user(request, restore=True)

        return web.Response(text=json.dumps({
            'status': 'succes',
            'message': 'ok post_table_delete'
        }), status=200)

    except Exception as e:
        print('[post_table_delete] except ', e)
        return web.Response(text=json.dumps({'status': 'error', 'message': str(e)}), status=500)


async def post_table_delete(request):
    '''
    Удаление записи пользователя
    :param request:
    :return:
    '''
    try:
        await table_delete_restore_user(request, restore=False)

        return web.Response(text=json.dumps({
            'status': 'succes',
            'message': 'ok post_table_delete'
        }), status=200)

    except Exception as e:
        print('[post_table_delete] except ', e)
        return web.Response(text=json.dumps({'status': 'error', 'message': str(e)}), status=500)
