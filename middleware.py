from aiohttp import web
from aiohttp_session import get_session
from aiopg.sa import create_engine

from model import get_dsn


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
    print(f'[auth_middleware] start {request.path}')
    if request.path.startswith('/static/'):
        response = await handler(request)
        return response

    # Доступные пути исходя из прав доступа пользователя
    guest_path = ['/', '/index', '/auth', '/auth/singin']
    view_path = guest_path + ['/auth/singout', '/table', '/part2']
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
    else:
        print(f'[auth_middleware] NOT allowed {result}')
        raise web.HTTPFound(request.app.router['/auth'].url())


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
