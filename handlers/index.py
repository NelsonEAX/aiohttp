# -*- coding: utf-8 -*-
'''Main page module'''

import aiohttp_jinja2

async def view_index(request):
    '''Get Main page
    :param request: get-request /index
    :return: page /index
    '''
    response = aiohttp_jinja2.render_template('index.html', request, {})
    response.headers['Content-Language'] = 'ru'
    return response
