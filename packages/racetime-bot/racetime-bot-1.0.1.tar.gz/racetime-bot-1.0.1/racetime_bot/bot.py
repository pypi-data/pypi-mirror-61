import asyncio
import json
from datetime import timedelta
from functools import partial

import requests
import websockets

from .handler import RaceHandler


class Bot:
    """
    The racetime.gg bot class.

    This bot uses event loops to connect to multiple race rooms at once. Each
    room is assigned a handler object, which you can determine with the
    `get_handler_class`/`get_handler_kwargs` methods.

    When implementing your own bot, you will need to specify what handler you
    wish to use, as the default `RaceHandler` will not actually do anything
    other than connect to the room and log the messages.
    """
    racetime_host = 'racetime.gg'
    racetime_secure = True
    scan_races_every = timedelta(seconds=30)
    gather_tasks_every = timedelta(seconds=30)

    def __init__(self, category_slug, client_id, client_secret, logger,
                 ssl_context=None):
        """
        Bot constructor.
        """
        self.logger = logger
        self.category_slug = category_slug
        self.ssl_context = ssl_context

        self.loop = asyncio.get_event_loop()
        self.last_scan = None
        self.races = {}
        self.handlers = {}

        self.access_token = self.authorize(client_id, client_secret)

    def get_handler_class(self):
        """
        Returns the handler class for races. Each race the bot finds will have
        its own handler object of this class.
        """
        return RaceHandler

    def get_handler_kwargs(self, ws_conn):
        """
        Returns a dict of keyword arguments to be passed into the handler class
        when instantiated.

        Override this method if you need to pass additional kwargs to your race
        handler.
        """
        return {
            'logger': self.logger,
            'conn': ws_conn,
        }

    def should_handle(self, race_data):
        """
        Determine if a race we've found should be handled by this bot or not.

        Returns True if the race should have a handler created for it, False
        otherwise.
        """
        return race_data.get('status', {}).get('value') not in RaceHandler.stop_at

    def authorize(self, client_id, client_secret):
        """
        Get an OAuth2 token from the authentication server.
        """
        resp = requests.post(self.http_uri('/o/token'), {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials',
        })
        data = json.loads(resp.content)
        token = data.get('access_token')
        if not token:
            raise Exception('Unable to retrieve access token.')
        return token

    def create_handler(self, race_data):
        """
        Create a new WebSocket connection and set up a handler object to manage
        it.
        """
        ws_conn = websockets.connect(
            self.ws_uri(race_data.get('websocket_bot_url')),
            extra_headers={
                'Authorization': 'Bearer ' + self.access_token,
            },
            ssl=self.ssl_context,
        )

        cls = self.get_handler_class()
        kwargs = self.get_handler_kwargs(ws_conn)

        handler = cls(**kwargs)

        self.logger.info(
            'Created handler for %(race)s'
            % {'race': race_data.get('name')}
        )

        return handler

    async def gather_tasks(self):
        """
        Examines the current races, and creates a handler and task for any race
        that should be handled but currently isn't.

        This method runs in a constant loop, checking for new races every few
        seconds.
        """
        tasks = {}

        def done(task_name, *args):
            del tasks[task_name]

        while True:
            for name, summary_data in self.races.items():
                if name not in tasks:
                    resp = requests.get(self.http_uri(summary_data.get('data_url')))
                    race_data = json.loads(resp.content)
                    if self.should_handle(race_data):
                        handler = self.create_handler(race_data)
                        tasks[name] = self.loop.create_task(handler.handle())
                        tasks[name].add_done_callback(partial(done, name))
                        self.logger.debug(tasks[name])
                    else:
                        self.logger.info(
                            'Ignoring %(race)s by configuration.'
                            % {'race': race_data.get('name')}
                        )
            await asyncio.sleep(self.gather_tasks_every.seconds)

    async def refresh_races(self):
        """
        Retrieve current race information from the category detail API
        endpoint, and populate the race list.

        This method runs in a constant loop, checking for new races every few
        seconds.
        """
        while True:
            self.logger.info('Refresh races')
            resp = requests.get(self.http_uri(f'/{self.category_slug}/data'))
            data = json.loads(resp.content)
            self.races = {}
            for race in data.get('current_races', []):
                self.races[race.get('name')] = race
            await asyncio.sleep(self.scan_races_every.seconds)

    def run(self):
        """
        Run the bot. Creates an event loop then iterates over it forever.
        """
        self.loop.create_task(self.refresh_races())
        self.loop.create_task(self.gather_tasks())
        self.logger.info('Running event loop')
        self.loop.run_forever()

    def http_uri(self, url):
        """
        Generate a HTTP/HTTPS URI from the given URL path fragment.
        """
        return self.uri(
            proto='https' if self.racetime_secure else 'http',
            url=url,
        )

    def ws_uri(self, url):
        """
        Generate a WS/WSS URI from the given URL path fragment.
        """
        return self.uri(
            proto='wss' if self.racetime_secure else 'ws',
            url=url,
        )

    def uri(self, proto, url):
        """
        Generate a URI from the given protocol and URL path fragment.
        """
        return '%(proto)s://%(host)s%(url)s' % {
            'proto': proto,
            'host': self.racetime_host,
            'url': url,
        }
