# -*- coding: utf-8 -*-
'''The file contains functions for working with the database'''

import base64
import time
from os.path import isfile

import sqlalchemy as sa
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from envparse import env

# Reading settings file
if isfile('.env'):
    env.read_envfile('.env')


# Database connection parameters obtained from .env
def get_dsn():
    '''DB connection string
    :return:
    '''
    return f"dbname={env.str('PG_DATABASE')} user={env.str('PG_USERNAME')} " \
           f"password={env.str('PG_PASSWORD')} host={env.str('PG_SERVER')}"


def get_sekret_key():
    '''SECRET_KEY for the session
    :return:
    '''
    return EncryptedCookieStorage(base64.urlsafe_b64decode(env.str('SECRET_KEY')))


def get_timestamp_str():
    '''TimeStamp string of the current timestamp for the base
    :return:
    '''
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


metadata = sa.MetaData()

# Table user
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

# Table user_rule
tb_user_rule = sa.Table(
    'user_rule',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('rule', None, sa.ForeignKey('tb_rule.id')),
    sa.Column('user', None, sa.ForeignKey('tb_user.id')))

# Table rule
tb_rule = sa.Table(
    'rule',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('rule', sa.String(255)),
    sa.Column('comment', sa.String(255)))


async def get_user_by_email(engine, email):
    '''User existence check
    :param engine: DB connection
    :param email: user email
    :return: a list of users
    '''
    async with engine.acquire() as conn:
        async for row in conn.execute(tb_user.select().where(tb_user.c.email == email)):
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
    '''Obtaining user rights by id
    :param engine: DB connection
    :param user_id: user id
    :return: user rights list
    '''
    async with engine.acquire() as conn:
        rules = []
        join = sa.join(tb_rule, tb_user_rule, tb_rule.c.id == tb_user_rule.c.rule)
        async for row in conn.execute(
                tb_rule.select().select_from(join).where(tb_user_rule.c.user == user_id)):
            rules.append(row[1])
        return rules


async def get_user_info(engine, user_id):
    '''Getting user data by id
    :param engine: DB connection
    :param user_id: user id
    :return: user information
    '''
    async with engine.acquire() as conn:
        async for row in conn.execute(tb_user.select().where(tb_user.c.id == user_id)):
            return {
                'id': row[0],
                'email': row[1],
                'password': row[2],
                'name': row[3],
                'surname': row[4],
                'rules': await get_user_rules(engine=engine, user_id=user_id)
            }


async def get_users(engine, admin):
    '''Retrieving user data
    :param engine: DB connection
    :param admin: Request data for admin user
    :return: a list of users
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
            # If the data is requested not by the Admin, then we do not show the admins
            if not admin and 'admin' in row[6]:
                continue
            users.append({
                'id': row[0],
                'email': row[1],
                'password': row[2],
                'name': row[3],
                'surname': row[4],
                'delete': row[5] is not None,
                'rules': row[6]
            })
        return users


async def get_rules(engine):
    '''Obtaining rights data
    :param engine: DB connection
    :return: list of rights
    '''
    async with engine.acquire() as conn:
        rules = {}
        async for row in conn.execute(tb_rule.select()):
            # {'admin': 0}
            rules[row[1]] = row[0]
        return rules


async def set_rules_for_user(engine, user_id, data):
    '''Setting / changing user rights
    :param engine: DB connection
    :param user_id: user id
    :param data: data for setting
    :return:
    '''
    rules = await get_rules(engine)
    user_rules = await get_user_rules(engine, user_id)

    for rule, rule_id in rules.items():
        # The user already has the current role and from the form flew to True
        # if rule in user_rules and data.get(rule, False) is True:

        # The user does not have the current role and from the form flew to False
        # if rule not in user_rules and data.get(rule, False) is False:

        # The user has a role, but False has arrived from the form - delete
        if rule in user_rules and data.get(rule, False) is False:
            async with engine.acquire() as conn:
                await conn.execute(
                    tb_user_rule.delete(None)
                    .where(tb_user_rule.c.user == user_id)
                    .where(tb_user_rule.c.rule == rule_id))

        # The user does not have roles, but True has arrived from the form - add
        if rule not in user_rules and data.get(rule, False) is True:
            async with engine.acquire() as conn:
                await conn.execute(tb_user_rule.insert(None).values(user=user_id, rule=rule_id))


async def set_delete_at_for_user(engine, user_id, restore=False):
    '''Delete user by id
    :param engine: DB connection
    :param user_id: id of the user to be deleted
    :return:
    '''
    timestamp = 'null' if restore else f"'{get_timestamp_str()}'"

    async with engine.acquire() as conn:
        await conn.execute(f'''UPDATE "user" SET delete_at={timestamp} WHERE id={user_id};''')


async def create_user(engine, data):
    '''User creation
    :param engine: DB connection
    :param data: new user data
    :return:
    '''
    async with engine.acquire() as conn:
        user = await get_user_by_email(engine=engine, email=data['email'])
        if user is not None:
            raise Warning('A user with this email already exists.')

        user_id = await conn.scalar(
            tb_user.insert(None).values(
                email=data['email'],
                password=data['password'],
                name=data['name'],
                surname=data['surname'],
                create_at=get_timestamp_str()))

        await set_rules_for_user(engine=engine, user_id=user_id, data=data)


async def update_user(engine, data):
    '''User data update
    :param engine: DB connection
    :param data: user data to update
    :return:
    '''
    async with engine.acquire() as conn:
        # Check that the email matches the current one, or that it is unique in the database
        user = await get_user_by_email(engine=engine, email=data['email'])
        if user is not None and int(user['id']) != int(data['id']):
            raise Warning('A user with this email already exists')

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
