from aiohttp import web
from aiohttp_session import get_session


# import asyncio
from aiopg.sa import create_engine
from model import get_dsn, get_sekret_key, create_table

@web.middleware
async def auth_middleware(request, handler):
    '''
    При переходе проверяем, что
    - Есть сессия
    - Либо страница не требует авторизации
    :param request:
    :param handler:
    :return:
    '''
    print('[auth_middleware] start')

    def need_auth_path(path):
        for r in ['/index', '/auth']:
            if path.startswith(r):
                return False
        return True

    session = await get_session(request)

    if session.get("rule"):
        print(f'[auth_middleware] session.get("rule"): {session.get("rule")}')
        return await handler(request)

    elif need_auth_path(request.path):
        print('[auth_middleware] need_auth_path(request.path)')
        url = request.app.router['/auth'].url()
        raise web.HTTPFound(url)
        # return handler(request)

    else:
        print('[auth_middleware] handler(request)')
        return await handler(request)


@web.middleware
async def db_middleware(request, handler):
    '''

    Подключение к БД. Вызывается для каждого запроса, поэтому создает лишнюю нагрузку
    Вариант рабочий, но
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
    '''
    https://aiohttp.readthedocs.io/en/stable/web_advanced.html#cleanup-context
    Инициализация приложения и добавление его в контекс посредством app.cleanup_ctx.append()
    Подключается при старте приложения и закрывает соединение при выходе
    :param app:
    :return:
    '''
    print('[pg_engine_ctx] pg_engine create')
    app['pg_engine'] = await create_engine(get_dsn())

    yield

    print('[pg_engine_ctx] pg_engine close')
    app['pg_engine'].close()
    await app['pg_engine'].wait_closed()