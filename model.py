import base64
import time
from os.path import isfile

import sqlalchemy as sa
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from envparse import env

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


def get_timestamp_str():
    '''
    Строка TimeStamp текущей временной метки для базы
    :return:
    '''
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


metadata = sa.MetaData()

# Таблица user
tb_user = sa.Table(
    'user',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('email', sa.String(255)),
    sa.Column('password', sa.String(255)),
    sa.Column('name', sa.String(255)),
    sa.Column('surname', sa.String(255)),
    sa.Column('create_at', sa.TIMESTAMP),
    sa.Column('delete_at', sa.TIMESTAMP))

# Таблица user_rule
tb_user_rule = sa.Table(
    'user_rule',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('rule', None, sa.ForeignKey('tb_rule.id')),
    sa.Column('user', None, sa.ForeignKey('tb_user.id')))

# Таблица rule
tb_rule = sa.Table(
    'rule',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('rule', sa.String(255)),
    sa.Column('comment', sa.String(255)))


async def get_user_by_email(engine, email):
    '''
    Проверка существования пользователя
    :param engine: Подключение к БД
    :param email: email пользователя
    :return: Список пользователей
    '''
    async with engine.acquire() as conn:
        async for row in conn.execute(tb_user.select()
                                              # .where(tb_user.c.password==json['password'])
                                              .where(tb_user.c.email == email)):
            # TODO: Требуется автоматическое преобразование в dict, без обращения по индексу
            return {
                'id': row[0],
                'email': row[1],
                'password': row[2],
                'name': row[3],
                'surname': row[4],
                'create_at': row[5],
                'delete_at': row[6]
            }


async def get_user_rules(engine, user_id):
    '''
    Получение прав пользователя по id
    :param engine: Подключение к БД
    :param user_id: id пользователя
    :return:
    '''
    async with engine.acquire() as conn:
        rules = []
        join = sa.join(tb_rule, tb_user_rule, tb_rule.c.id == tb_user_rule.c.rule)
        async for row in conn.execute(tb_rule.select()
                                              .select_from(join)
                                              .where(tb_user_rule.c.user == user_id)):
            rules.append(row[1])
        return rules


async def get_user_info(engine, user_id):
    '''
    Получение данных о пользователе по id
    :param engine: Подключение к БД
    :param user_id: id пользователя
    :return:
    '''
    async with engine.acquire() as conn:
        async for row in conn.execute(tb_user.select()
                                              .where(tb_user.c.id == user_id)):
            return {
                'id': row[0],
                'email': row[1],
                'password': row[2],
                'name': row[3],
                'surname': row[4],
                'rules': await get_user_rules(engine=engine, user_id=user_id)
            }


async def get_users(engine, admin):
    '''
    Получение данных о пользователях
    :param engine: Подключение к БД
    :param admin: Запрос данных для пользователя с правами админа
    :return:
    '''
    async with engine.acquire() as conn:
        users = []
        where = '' if admin else 'WHERE u.delete_at is null'
        async for row in await conn.execute(
                f'''SELECT u.id, u.email, u.password, u.name, u.surname, u.delete_at,
                ARRAY(
                    SELECT r.rule 
                    FROM "user_rule" as ur
                    LEFT JOIN "rule" as r on ur.rule = r.id
                    WHERE ur.user = u.id
                ) as "rules"
                FROM "user" as u
                {where}
                ORDER BY u.id;'''):
            # Если данные запрашивает не Админ, то не показываем админов
            if not admin and 'admin' in row[6]:
                continue
            users.append({
                'id': row[0],
                'email': row[1],
                'password': row[2],
                'name': row[3],
                'surname': row[4],
                'delete': False if row[5] is None else True,
                'rules': row[6]
            })
        return users


async def get_rules(engine):
    '''
    Получение данных о правах
    :param engine: Подключение к БД
    :return:
    '''
    async with engine.acquire() as conn:
        rules = {}
        async for row in conn.execute(tb_rule.select()):
            # {'admin': 0}
            rules[row[1]] = row[0]
        return rules


async def set_rules_for_user(engine, user_id, data):
    '''
    Установка/изменение прав пользователя
    :param engine: Подключение к БД
    :param user_id:
    :param data:
    :return:
    '''
    rules = await get_rules(engine)
    user_rules = await get_user_rules(engine, user_id)

    for rule, rule_id in rules.items():
        # Текущая роль уже есть у пользователя и из формы прилетела в True - ничего не делаем, уже хорошо
        # if rule in user_rules and data.get(rule, False) is True:

        # Текущей роли нет у пользователя и из формы прилетела в False - ничего не делаем, уже хорошо
        # if rule not in user_rules and data.get(rule, False) is False:

        # Роль есть у пользователя, но с формы прилетела False - удаляем
        if rule in user_rules and data.get(rule, False) is False:
            async with engine.acquire() as conn:
                print(tb_user_rule.delete().where(tb_user_rule.c.user == user_id).where(tb_user_rule.c.rule == rule_id))
                await conn.execute(
                    tb_user_rule.delete().where(tb_user_rule.c.user == user_id).where(tb_user_rule.c.rule == rule_id))

        # Роли нет у пользователя, но с формы прилетела True - добавляем
        if rule not in user_rules and data.get(rule, False) is True:
            async with engine.acquire() as conn:
                await conn.execute(tb_user_rule.insert().values(user=user_id, rule=rule_id))


async def set_delete_at_for_user(engine, user_id, restore=False):
    '''
    Удаляем пользователя по id
    :param engine: Подключение к БД
    :param user_id: id удаляемого пользователя
    :return:
    '''
    timestamp = 'null' if restore else f"'{get_timestamp_str()}'"

    async with engine.acquire() as conn:
        await conn.execute(f'''UPDATE "user" SET delete_at={timestamp} WHERE id={user_id};''')


async def create_user(engine, data):
    '''
    Создание пользователя
    :param engine:
    :param data:
    :return:
    '''
    async with engine.acquire() as conn:
        user = await get_user_by_email(engine=engine, email=data['email'])
        if user is not None:
            raise Warning('Пользователь с таким email уже существует')

        user_id = await conn.scalar(
            tb_user.insert().values(
                email=data['email'],
                password=data['password'],
                name=data['name'],
                surname=data['surname'],
                create_at=get_timestamp_str()))

        await set_rules_for_user(engine=engine, user_id=user_id, data=data)


async def update_user(engine, data):
    '''
    Обновление данных пользователя
    :param engine:
    :param data:
    :return:
    '''
    async with engine.acquire() as conn:
        # Проверим, что переданный email совпадает с текущим, либо что он уникален в БД
        user = await get_user_by_email(engine=engine, email=data['email'])
        if user is not None and int(user['id']) != int(data['id']):
            raise Warning('Пользователь с таким email уже существует')

        await conn.execute(
            sa.update(tb_user)
                .values({
                'email': data['email'],
                'password': data['password'],
                'name': data['name'],
                'surname': data['surname']
            })
                .where(tb_user.c.id == int(data['id'])))

        await set_rules_for_user(engine=engine, user_id=int(data['id']), data=data)
