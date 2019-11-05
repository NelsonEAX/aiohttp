from handlers.index import get_index
from handlers.auth import get_auth, post_auth_singin
from handlers.table import get_table

def setup_routes(app):
    '''
    :param app: application instance
    :return:
    '''
    app.router.add_get('/', get_index)
    app.router.add_get('/index', get_index)
    app.router.add_get('/auth', get_auth)
    app.router.add_post('/auth/singin', post_auth_singin)
    app.router.add_get('/table', get_table)