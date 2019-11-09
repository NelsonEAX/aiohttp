import aiohttp_jinja2

async def view_index(request):
    '''
    Главная страница
    :param request:
    :return:
    '''
    response = aiohttp_jinja2.render_template('index.html', request, {})
    response.headers['Content-Language'] = 'ru'
    return response