from handlers.index import get_index
from handlers.auth import get_auth, post_auth_singin, post_auth_singout
from handlers.table import get_table
from handlers.part2 import get_part2

def setup_routes(app):
    '''
    :param app: application instance
    :return:
    '''
    app.router.add_get('/', get_index)
    app.router.add_get('/index', get_index)
    app.router.add_get('/auth', get_auth)
    app.router.add_post('/auth/singin', post_auth_singin)
    app.router.add_post('/auth/singout', post_auth_singout)
    app.router.add_get('/table', get_table)
    app.router.add_get('/part2', get_part2)
