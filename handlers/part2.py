# -*- coding: utf-8 -*-
'''Test part 2 module'''

import aiohttp_jinja2

async def view_part2(request):
    '''Get Test Part 2 page
    :param request: get-request /part2
    :return: page /test2
    '''

    # responce_obj = {'status': 'success'}
    # return web.Response(text=json.dumps(responce_obj), status=200)
    context = {
        'name': 'Admin',
        'rule': ['admin', 'editor'],
        'items': [
            {'id': '1', 'email': 'email_1', 'name': 'name_1', 'surname': 'surname_1'},
            {'id': '2', 'email': 'email_2', 'name': 'name_2', 'surname': 'surname_2'},
            {'id': '3', 'email': 'email_3', 'name': 'name_3', 'surname': 'surname_3'},
            {'id': '4', 'email': 'email_4', 'name': 'name_4', 'surname': 'surname_4'}
        ]
    }
    response = aiohttp_jinja2.render_template('part2.html', request, context)
    response.headers['Content-Language'] = 'ru'
    return response
