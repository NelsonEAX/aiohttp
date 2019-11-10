# -*- coding: utf-8 -*-
'''Auth page module'''

import json

import aiohttp_jinja2
from aiohttp_session import get_session
from aiohttp import web

# pylint: disable=import-error
from model import get_user_by_email, get_user_rules
# pylint: enable=import-error



async def view_auth(request):
    '''Get Auth page
    :param request: get-request /auth
    :return: page /auth
    '''
    try:
        context = {}
        session = await get_session(request)
        if session.get('email', None) is not None:
            context['email'] = session['email']

        response = aiohttp_jinja2.render_template('auth.html', request, context)
        response.headers['Content-Language'] = 'ru'
        return response

    except Exception as exc:
        print('[get_auth] except ', exc)
        return web.Response(text=json.dumps({'status': 'error', 'message': str(exc)}), status=500)


async def post_auth_singin(request):
    '''Authorization on the site
    :param request: post contains email and password fields
    :return: status and service message
    '''
    try:
        # Receive and verify login details
        post = await request.json()
        if post['email'] is None or post['password'] is None:
            raise Warning('Invalid data')

        user = await get_user_by_email(engine=request.app['pg_engine'], email=post['email'])

        # Do not store passwords in their pure form
        # User found and passwords match and user not deleted
        if user is None or post['password'] != user['password'] or user['delete_at'] is not None:
            raise Warning('Invalid username or password')

        session = await get_session(request)
        session['id'] = user['id']
        session['email'] = user['email']
        session['rule'] = await get_user_rules(engine=request.app['pg_engine'], user_id=user['id'])

        print('[post_auth_singin] user', str(user), str(session['rule']))

        return web.Response(text=json.dumps({
            'status': 'succes',
            'message': 'ok post_auth_singin'
        }), status=200)

    except Exception as exc:
        print('[post_auth_singin] except ', exc)
        return web.Response(text=json.dumps({
            'status': 'error',
            'message': str(exc)
        }), status=(401 if type(exc).__name__ == 'Warning' else 500))


async def post_auth_singout(request):
    '''Clearing a client session
    :param request: post-request
    :return: status and service message
    '''
    try:
        session = await get_session(request)
        session.clear()

        return web.Response(text=json.dumps({
            'status': 'succes',
            'message': 'ok post_auth_singout'
        }), status=200)

    except Exception as exc:
        print('[post_auth_singout] except ', exc)
        return web.Response(text=json.dumps({
            'status': 'error',
            'message': str(exc)
        }), status=500)
