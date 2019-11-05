from aiohttp import web
from aiohttp_session import get_session
import aiohttp_jinja2
import time


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

    context = {'name': 'Andrew', 'surname': 'Svetlov'}
    response = aiohttp_jinja2.render_template('auth.html',
                                              request,
                                              context)
    response.headers['Content-Language'] = 'ru'
    return response


async def post_auth_singin(request):
    '''

    :param request:
    :return:
    '''
    data = await request.post()
    session = await get_session(request)
    email = data['email']
    print(email)
    last_visit = session['last_visit'] if 'last_visit' in session else None
    session['last_visit'] = time.time()
    session['rule'] = ['admin']

    text = 'Last visited: {}'.format(last_visit)
    return web.Response(text=text)