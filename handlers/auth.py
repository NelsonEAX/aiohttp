from aiohttp import web
from aiohttp_session import get_session
import aiohttp_jinja2
import time
import json

from model import create_table, get_user_by_email, get_user_rules
# @routes.get('/auth')
# @aiohttp_jinja2.template('auth.html')
async def get_auth(request):
    '''

    :param request:
    :return:
    '''
    try:
        context = {}
        session = await get_session(request)
        if(session.get('email', None) is not None):
            context['email'] = session['email']

        response = aiohttp_jinja2.render_template(
            'auth.html',
            request,
            context
        )
        response.headers['Content-Language'] = 'ru'
        return response

    except Exception as e:
        return web.Response(text=json.dumps({'status': 'error', 'message': str(e)}), status=500)


    # print(str(session))
    # last_visit = session['last_visit'] if 'last_visit' in session else None
    # session['last_visit'] = time.time()
    # session['rule'] = ['admin']
    # text = 'Last visited: {}'.format(last_visit)
    # //return web.Response(text=text)




async def post_auth_singin(request):
    '''

    :param request:
    :return:
    '''
    result = {
        'status': 'success',
        'message': 'Во время выполнения возникли ошибки',
        'http_code': 200
    }

    try:
        print('[post_auth_singin] try')

        post = await request.json()
        if post['email'] is None or post['password'] is None:
            raise Warning('Данные указаны неверно')

        user = await get_user_by_email(engine=request.app['pg_engine'], email=post['email'])

        # TODO: Так пароли хранить и проверять НЕЛЬЗЯ
        if user is None or post['password'] != user['password']:
            raise Warning('Неверно указан логин или пароль')

        session = await get_session(request)

        session['email'] = user['email']
        session['rule'] = await get_user_rules(engine=request.app['pg_engine'], user_id=user['id'])

        print('[post_auth_singin] user', str(user), str(session['rule']))
        result['message'] = f"Вы вошли в систему как {user['email']}"

    except Exception as e:
        print('[post_auth_singin] except ', e)
        result['status'] = 'error'
        result['message'] = str(e)
        result['http_code'] = 401 if type(e).__name__ == 'Warning' else 500
    finally:
        print('[post_auth_singin] finally')
        return web.Response(text=json.dumps({
            'status': result['status'],
            'message': result['message']
        }), status=result['http_code'])