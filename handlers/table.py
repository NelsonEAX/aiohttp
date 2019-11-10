# -*- coding: utf-8 -*-
'''Table page module'''

import aiohttp_jinja2
from aiohttp_session import get_session
from aiohttp import web

# pylint: disable=import-error
from model import get_users, get_user_info, set_delete_at_for_user, create_user, update_user
# pylint: enable=import-error



async def view_table(request):
    '''Get Table page
    :param request: get-request /table
    :return: page /table
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

    except Exception as exc:
        print('[get_table] except ', exc)
        return web.json_response({'status': 'error', 'message': str(exc)}, status=500)


async def post_table_read(request):
    '''Reading user data
    :param request: post-request
    :return:
    '''
    try:
        post = await request.json()
        if post['id'] is None:
            raise Warning('Invalid data')

        user_info = await get_user_info(engine=request.app['pg_engine'], user_id=post['id'])
        if len(user_info) == 0:
            raise Warning('Invalid data')

        return web.json_response(user_info, status=200)
    except Exception as exc:
        print('[post_table_read] except ', exc)
        return web.json_response({'status': 'error', 'message': str(exc)}, status=500)


async def post_table_create(request):
    '''Create a new user
    :param request: post-request
    :return:
    '''
    try:
        post = await request.json()
        if post['email'] == '' or post['password'] == '':
            raise Warning('Required fields are not filled')

        await create_user(engine=request.app['pg_engine'], data=post)

        return web.json_response(post, status=200)
    except Exception as exc:
        print('[post_table_create] except ', exc)
        return web.json_response({'status': 'error', 'message': str(exc)}, status=500)


async def post_table_update(request):
    '''User data update
    :param request: post-request
    :return:
    '''
    try:
        # Receive and verify data to update the record
        post = await request.json()
        if post['email'] == '' or post['password'] == '':
            raise Warning('Required fields are not filled')

        await update_user(engine=request.app['pg_engine'], data=post)

        return web.json_response(post, status=200)
    except Exception as exc:
        print('[post_table_update] except ', exc)
        return web.json_response({'status': 'error', 'message': str(exc)}, status=500)


async def table_delete_restore_user(request, restore=False):
    '''Delete or restore user
    :param request: post-request
    :param user_id: user id for delete or restore
    :param restore: state
    :return:
    '''
    print(f'[table_delete_restore_user] start {restore}')

    post = await request.json()
    if post['id'] is None:
        raise Warning('No user id')

    session = await get_session(request)
    if session.get('id', None) == int(post['id']):
        raise Warning('Cannot delete own user')

    await set_delete_at_for_user(
        engine=request.app['pg_engine'], user_id=int(post['id']), restore=restore)


async def post_table_restore(request):
    '''User record recovery
    :param request: post-request
    :return:
    '''
    try:
        await table_delete_restore_user(request, restore=True)
        return web.json_response({'status': 'succes', 'message': 'ok restore'}, status=200)

    except Exception as exc:
        print('[post_table_delete] except ', exc)
        return web.json_response({'status': 'error', 'message': str(exc)}, status=500)


async def post_table_delete(request):
    '''Delete user record
    :param request: post-request
    :return:
    '''
    try:
        await table_delete_restore_user(request, restore=False)
        return web.json_response({'status': 'succes', 'message': 'ok delete'}, status=200)

    except Exception as exc:
        print('[post_table_delete] except ', exc)
        return web.json_response({'status': 'error', 'message': str(exc)}, status=500)
