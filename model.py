# import asyncio
# from aiopg.sa import create_engine, Engine
import sqlalchemy as sa
import base64
from envparse import env
# from cryptography import fernet
from os.path import isfile
from aiohttp_session.cookie_storage import EncryptedCookieStorage

# Чтение настроек
if isfile('.env'):
    env.read_envfile('.env')

# Параметры подключения к БД, полученные из .env
def get_dsn():
    '''
    Строка подключения к БД
    :return:
    '''
    return f"dbname={env.str('PG_DATABASE')} user={env.str('PG_USERNAME')} " \
           f"password={env.str('PG_PASSWORD')} host={env.str('PG_SERVER')}"

def get_sekret_key():
    '''
    SECRET_KEY для сессии
    :return:
    '''
    return EncryptedCookieStorage(base64.urlsafe_b64decode(env.str('SECRET_KEY')))

metadata = sa.MetaData()

# Таблица user
tb_user = sa.Table('user', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('email', sa.String(255)),
    sa.Column('password', sa.String(255)),
    sa.Column('name', sa.String(255)),
    sa.Column('surname', sa.String(255)))

# Таблица rule
tb_rule = sa.Table('rule', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('rule', sa.String(255)),
    sa.Column('comment', sa.String(255)))

# Тестовая функция с raw-запросом
async def create_table(engine):
    async with engine.acquire() as conn:
        await conn.execute('DROP TABLE IF EXISTS tbl')
        await conn.execute('''CREATE TABLE tbl (
                                  id serial PRIMARY KEY,
                                  val varchar(255))''')

async def get_user(engine, json):
    '''
    Проверка существования пользователя/пароля
    :param engine: Подключение к БД
    :param json: Объект, содержащий email и password
    :return:
    '''
    # with (yield from engine) as conn:
    #     uid = yield from conn.execute(tb_user.select().where(email=json['email'], password=json['password']))
    #     for row in uid:
    #         print(row.email)
    #     return uid
    async with engine.acquire() as conn:
        result = []
        async for row in conn.execute(tb_user.select()
                                 .where(tb_user.c.email==json['email'])
                                 .where(tb_user.c.password==json['password'])):
            result.append(row)
        return result
        # print(row.id, row.email, row.password)
        # await conn.fetchone()

        # async for row in conn.execute(tb_user.select()):
        #     print(row.id, row.name, row.surname)

# async def go(id):
#     async with create_engine(
#             user=env.str('PG_USERNAME'),
#             database=env.str('PG_DATABASE'),
#             host=env.str('PG_SERVER'),
#             password=env.str('PG_PASSWORD')
#     ) as engine:
#         async with engine.acquire() as conn:
#             await conn.execute(tb_user.insert().values(id=id, email='abc@mail{}.ru'.format(str(id)), password='abcd'))
#
#             async for row in conn.execute(tb_user.select()):
#                 print(row.id, row.email, row.password)
#
#         await create_table(engine)



# loop = asyncio.get_event_loop()
# engine = loop.run_until_complete(create_engine(dsn, loop=loop))
# loop.run_until_complete(create_table(engine=engine))
#
# engine.close()
# loop.run_until_complete(engine.wait_closed())