# -*- coding: utf-8 -*-
'''Test part 2 module'''

import json
import time
import random

import asyncio
import aiohttp_jinja2
from aiohttp import web, ClientSession

TIMEOUT = 2
TIMEOUT_COEF = 0.7

async def fetch_json(request, part):
    '''Get a piece of the json-object
    :param request:
    :param part: part of json to recive
    :return: list of object
    '''
    try:
        start = time.time()
        timeout = random.randint(1, 4) * TIMEOUT_COEF
        print(f'[fetch_json] fetching JSON from part {part} in timeout {timeout}')
        await asyncio.sleep(timeout)

        url = f'{request.url.parent}{str(request.app.router["json_part"].url_for(part=str(part)))}'
        try:
            async with ClientSession(cookies=request.cookies) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        json_obj = await response.json()
                    else:
                        json_obj = []

        except Exception as exc:
            raise exc

        print(f'[fetch_json] part {part} received in: {time.time() - start} seconds')
        return json_obj

    except Exception as exc:
        print(f'[fetch_json] part {part} except ', exc)
        return []

async def view_part2(request):
    '''Get Test Part 2 page
    :param request: get-request /part2
    :return: page /test2
    '''
    try:
        json_obj = []

        # formulate requests for resources
        futures = [fetch_json(request, part) for part in range(5)]
        done, pending = await asyncio.wait(futures, timeout=TIMEOUT)

        # waiting for completion and pull out the result
        for future in pending:
            future.cancel()

        for future in done:

            json_obj += future.result()

        # sort the list and serialize to a string
        json_obj.sort(key=(lambda obj: obj['id']))
        json_str = json.dumps(json_obj).replace('}, {', '},\n{')

        response = aiohttp_jinja2.render_template('part2.html', request, {'json': json_str})
        response.headers['Content-Language'] = 'ru'
        return response

    except Exception as exc:
        print('[view_part2] except ', exc)
        return web.json_response({'status': 'error', 'message': str(exc)}, status=500)


async def view_part2_json(request):
    '''Get json page
    :param request: get-request /part2/json/{part}
    :return: json part
    '''
    try:
        json_part = int(request.match_info['part'])
        if json_part == 3:
            json_obj = [
                {"id": 21, "name": "Test 21"}, {"id": 22, "name": "Test 22"},
                {"id": 23, "name": "Test 23"}, {"id": 24, "name": "Test 24"},
                {"id": 25, "name": "Test 25"}, {"id": 26, "name": "Test 26"},
                {"id": 27, "name": "Test 27"}, {"id": 28, "name": "Test 28"},
                {"id": 29, "name": "Test 29"}, {"id": 30, "name": "Test 30"},
                {"id": 51, "name": "Test 51"}, {"id": 52, "name": "Test 52"},
                {"id": 53, "name": "Test 53"}, {"id": 54, "name": "Test 54"},
                {"id": 55, "name": "Test 55"}, {"id": 56, "name": "Test 56"},
                {"id": 57, "name": "Test 57"}, {"id": 58, "name": "Test 58"},
                {"id": 59, "name": "Test 59"}, {"id": 60, "name": "Test 60"}
            ]
        else:
            with open(f'./seed/file{json_part}.json', 'r') as read_file:
                json_obj = json.load(read_file)

        return web.json_response(json_obj, status=200)

    except Exception as exc:
        print('[view_part2_json] except ', exc)
        return web.json_response({'status': 'error', 'message': str(exc)}, status=500)
