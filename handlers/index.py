import aiohttp_jinja2

# @routes.get('/')
# @routes.get('/index')
# @aiohttp_jinja2.template('index.html')
async def get_index(request):
    '''

    :param request:
    :return:
    '''
    # responce_obj = { 'status': 'success' }
    # return web.Response(text=json.dumps(responce_obj), status=200)
    context = {'name': 'Andrew', 'surname': 'Svetlov'}
    response = aiohttp_jinja2.render_template('index.html',
                                              request,
                                              context)
    response.headers['Content-Language'] = 'ru'
    return response