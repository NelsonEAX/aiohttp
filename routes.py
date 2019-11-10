# -*- coding: utf-8 -*-
'''The file contains information about routes'''

from handlers.auth import view_auth, post_auth_singin, post_auth_singout
from handlers.index import view_index
from handlers.part2 import view_part2, view_part2_json
from handlers.table import view_table, post_table_create, post_table_read, \
    post_table_update, post_table_restore, post_table_delete


def setup_routes(app):
    '''Application REST API
    :param app: application instance
    :return:
    '''
    app.router.add_view('/', view_index)
    app.router.add_view('/index', view_index)

    app.router.add_view('/auth', view_auth, name='auth')
    app.router.add_post('/auth/singin', post_auth_singin)
    app.router.add_post('/auth/singout', post_auth_singout)

    app.router.add_view('/table', view_table)
    app.router.add_post('/table/create', post_table_create)
    app.router.add_post('/table/read', post_table_read)
    app.router.add_post('/table/update', post_table_update)
    app.router.add_post('/table/restore', post_table_restore)
    app.router.add_post('/table/delete', post_table_delete)

    app.router.add_view('/part2', view_part2)
    app.router.add_get('/part2/json/{part:[0-4]}', view_part2_json, name='json_part')
    # app.router.add_get('/part2/json2', view_part2)
    # app.router.add_get('/part2/json3', view_part2)
