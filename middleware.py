from aiohttp import web
from aiohttp_session import get_session

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
        return handler(request)

    else:
        print('[auth_middleware] handler(request)')
        return await handler(request)


# TODO: Реализовать подключение
@web.middleware
async def db_middleware(request, handler):
    '''
    Подключение к БД
    :param request:
    :param handler:
    :return:
    '''
    print('[db_middleware] handler(request)')
    return await handler(request)


