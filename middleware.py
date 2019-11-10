# -*- coding: utf-8 -*-
'''The file contains functions for preprocessing requests'''

from aiohttp_session import get_session
from aiopg.sa import create_engine
from aiohttp import web

from model import get_dsn


@web.middleware
async def auth_middleware(request, handler):
    '''Upon transition, check that the request matches the access level
    :param request:
    :param handler:
    :return:
    '''
    print(f'[auth_middleware] start {request.path}')
    if request.path.startswith('/static/') or request.path.startswith('/favicon.ico'):
        return await handler(request)

    # Available paths based on user permissions
    guest_path = ['/', '/index', '/auth', '/auth/singin']
    view_path = guest_path + [
        '/auth/singout', '/table', '/part2',
        '/part2/json/0', '/part2/json/1', '/part2/json/2', '/part2/json/3', '/part2/json/4'
    ]
    edit_path = view_path + ['/table/create', '/table/read', '/table/update', '/table/delete']
    admin_path = edit_path + ['/table/restore']

    session = await get_session(request)
    rules = session.get("rule", [])

    allowed_path = guest_path
    if 'admin' in rules:
        allowed_path = admin_path
    elif 'edit' in rules:
        allowed_path = edit_path
    elif 'view' in rules:
        allowed_path = view_path

    result = f'path="{request.path}" rules="{str(rules)}" {str(allowed_path)}'
    if request.path in allowed_path:
        print(f'[auth_middleware] allowed {result}')
        return await handler(request)

    print(f'[auth_middleware] NOT allowed {result}')
    return web.HTTPFound(request.app.router['auth'].url())


@web.middleware
async def db_middleware(request, handler):
    '''Connection to the database.
    Called for each request, therefore, creates an extra load. Replaced
    :param request:
    :param handler:
    :return:
    '''
    print('[db_middleware] pg_engine create')
    request.app['pg_engine'] = await create_engine(get_dsn())

    response = await handler(request)

    print('[db_middleware] pg_engine close')
    request.app['pg_engine'].close()
    await request.app['pg_engine'].wait_closed()

    return response


async def pg_engine_ctx(app):
    '''Initializing the application and adding it to the context using app.cleanup_ctx.append ()
    Connects at application startup and closes the connection upon exit
    https://aiohttp.readthedocs.io/en/stable/web_advanced.html#cleanup-context
    :param app:
    :return:
    '''
    print('[pg_engine_ctx] pg_engine create')
    app['pg_engine'] = await create_engine(get_dsn())

    yield

    print('[pg_engine_ctx] pg_engine close')
    app['pg_engine'].close()
    await app['pg_engine'].wait_closed()
