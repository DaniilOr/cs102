from config import *
import requests
from time import sleep
from random import normalvariate
from datetime import date
from igraph import Graph, plot
import numpy as np
import igraph

def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    # PUT YOUR CODE HERE
    delay = 1
    counter = 0
    Jitter = 0.15
    Factor = backoff_factor
    while counter < max_retries:
        response = requests.get(url, timeout = timeout)
        if response.status_code == 200:
            break
        sleep(delay)

        # calculate next delay
        delay = min(delay * Factor, timeout)
        delay = delay + normalvariate(delay * Jitter)
    return response

def get_friends(user_id, fields):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    # PUT YOUR CODE HERE
    query = "{}/friends.get?access_token={}&user_id={}&fields={}&v={}".format(domain, access_token, user_id, fields, v)
    response = get(query, backoff_factor=2,timeout=100).json()
    return response

def get_age(born):
    born = born.split('.')
    year = int(born[2])
    month = int(born[1])
    day = int(born[0])
    today = date.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    return age


def age_predict(user_id):
    """
    >>> age_predict(???)
    ???
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    # PUT YOUR CODE HERE
    friends = get_friends(user_id, 'bdate')
    ages = []
    for friend in friends['response']['items']:
        try:
            age = get_age(friend['bdate'])
            ages.append(age)
        except:
            pass
    if len(ages) % 2:
        return ages[len(ages) // 2]
    else:
        return (ages[len(ages) // 2] + ages[len(ages) // 2 + 1]) // 2


def get_network(users_ids, as_edgelist=True):
    """ Building a friend graph for an arbitrary list of users """
    # PUT YOUR CODE HERE
    vertices = []
    edges = []
    cipher = {}
    for user_id in users_ids:
        print(user_id)
        if not user_id in cipher.keys():
            cipher.update({user_id:len(cipher.keys())+1})
        friends = get_friends(user_id, 'sex')
        for friend in friends['response']['items'][:5]:
            lable = friend['id']
            #print(lable)
            if not lable in cipher.keys():
                cipher.update({lable:len(cipher.keys())+1})
                vertices.append(cipher[lable])
            edges.append((cipher[user_id], cipher[lable]))
    print("FFF")
    g = Graph(vertex_attrs={"label":vertices},
                edges=edges, directed=False)
    print("FFF")
    print(edges)
    print(vertices)
    g.simplify(multiple=True, loops=True)
    communities = g.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()
    print(clusters)
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    plot(g, **visual_style)




if __name__ == '__main__':
    friends = get_friends(268067723, 'sex')['response']['items']
    ids = [friend['id'] for friend in friends]
    print(ids)
    print(get_network(ids[:2]))

