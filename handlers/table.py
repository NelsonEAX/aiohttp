import aiohttp_jinja2

# @routes.get('/table')
# @aiohttp_jinja2.template('table.html')
async def get_table(request):
    '''

    :param request:
    :return:
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
    response = aiohttp_jinja2.render_template('table.html',
                                              request,
                                              context)
    response.headers['Content-Language'] = 'ru'
    return response