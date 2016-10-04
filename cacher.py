import cherrypy
import requests
import functools
import datetime
from threading import Lock

seconds_in_24_hours = 86400
server_host = '0.0.0.0'
server_port = 8000
request_address = 'https://vast-eyrie-4711.herokuapp.com/?key='
response_status_ok = 200

def mem_cached(func):
    cache = {}
    response_in_progress = set()
    dict_lock = Lock()
    set_lock = Lock()
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if 'key' not in kwargs:
            return ''
        cache_key = kwargs['key']
        current_time = datetime.datetime.now()
        if cache_key in response_in_progress :
            return ''
        if cache_key in cache:
            time_delta = current_time - cache[cache_key][1]
            if time_delta.seconds < seconds_in_24_hours:
                return cache[cache_key][0]
        with set_lock :
            response_in_progress.add(cache_key)
        server_answer = func(*args, **kwargs)
        if server_answer != '' :
            with dict_lock :
                cache[cache_key] = (server_answer, current_time)
        with set_lock :
            response_in_progress.discard(cache_key)
        return server_answer
    return inner

class CacheGetter(object):
    @cherrypy.expose
    def index(self):
        return ""
    
    @mem_cached
    @cherrypy.expose    
    def from_cache(self, key):
        response = requests.get(request_address + key)
        if response.status_code == response_status_ok :
            return response.text
        return ''

cherrypy.config.update(
    {
     'server.socket_host': server_host,
     'server.socket_port': server_port,
    }
)

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True
        }
    }
    cherrypy.quickstart(CacheGetter(), '/', conf)