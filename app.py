# -*- coding: utf-8 -*-
'''Application start module. Point of entry.
Initializing an application
Setting up a session
Setting up templates, adding routes
'''

import aiohttp_jinja2
import jinja2
from aiohttp_session import session_middleware
from aiohttp import web

from middleware import auth_middleware, pg_engine_ctx
from model import get_sekret_key
from routes import setup_routes

# initialize the application
app = web.Application(middlewares=[
    session_middleware(get_sekret_key()),
    # db_middleware, # migrate to app.cleanup_ctx
    auth_middleware,
])

# app.on_startup.append(create_pg_engine)
# app.on_cleanup.append(dispose_pg_engine)
app.cleanup_ctx.append(pg_engine_ctx)

# specify a folder with html-templates for the template engine
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# set routes
setup_routes(app)

web.run_app(app)
