import pandas as pd
import requests
import textwrap
from config import *
from pandas.io.json import json_normalize
from string import Template


def get_wall(
    owner_id: str='',
    domain: str='',
    offset: int=100,
    count: int=10,
    filter: str='owner',
    extended: int=0,
    fields: str='',
    v: str='5.103'
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.
    @see: https://vk.com/dev/wall.get
    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    """
    # PUT YOUR CODE HERE
    code = """
    var owner_id = '%s';
    var domain = '%s';
    var offset = %s;
    var count = %s;
    var filter = '%s';
    var extended = %s;
    var fields = '%s';
    var v = '%s';
    var posts = [];
    var shift = 0;
    while ((shift)<count) {
    posts.push(API.wall.get({
        "owner_id": owner_id,
        "domain": domain,
        "offset": shift,
        "count": count,
        "filter": filter,
        "extended": extended,
        "fields": fields,
        "v": v
    }));
    shift = shift + offset;
    }
    return posts;
    """ % (owner_id, domain, offset, count, filter, extended, fields, v)

    response = requests.post(
        url="https://api.vk.com/method/execute",
            data={
                "code": code,
                "access_token": access_token,
                "v": "5.103"
            }
    )
    posts = []
    responses = response.json()
    for i in responses['response']:
        for item in i['items']:
            post = {}
            post['text'] = item['text']
            post['likes'] = item['likes']['count']
            post['views'] = item['views']['count']
            posts.append(post)
    print(posts)
    print(len(posts))
    return posts
