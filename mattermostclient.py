import ssl
import asyncio
from urllib.parse import urlparse
import websockets
import logging
import json

logging.basicConfig(level=logging.INFO)

log = logging.getLogger('mattermost.client')

from mattermostapi import MattermostApi, MattermostApiResponseError

# Default websocket timeout - this is needed to send a heartbeat to keep the connection alive
DEFAULT_TIMEOUT = 30

class MattermostClientError(Exception):
	"""Raise for client errors"""

class MattermostClient:
	def __init__(self, url, api=MattermostApi, verify=True, timeout=DEFAULT_TIMEOUT):
		self._urlparts = urlparse(url)
		self._apiUrl = '/api/v3'
		self._userid = ''
		self._teamid = ''
		self._channelid = ''
		self._username = ''
		self._url = url
		self._token = ''
		self._verify = verify
		self._timeout = timeout
		self._loop = None
		self._websocket = None
		self._cookie = None
		self.api = api(url, verify=verify)

	def login(self, email, password, token=None, device_id=None):
		response = self.api.login(email, password, token, device_id)
		user = json.loads(response.text)
		self._token = response.headers['Token']
		self._cookie = response.cookies['MMAUTHTOKEN']
		if 'id' in user:
			self._userid = user['id']
		if 'username' in user:
			self._username = user['username']
		return user

	@property
	def userid(self):
		return self._userid

	@property
	def username(self):
		return self._username

	@property
	def url(self):
		return self._url

	@property
	def urlparts(self):
		return self._urlparts

	@property
	def apiUrl(self):
		return self._apiUrl

	@property
	def token(self):
		return self._token

	@property
	def cookie(self):
		return self._cookie

	def connect(self, eventHandler):
		self._loop = asyncio.get_event_loop()
		self._loop.run_until_complete(self.createConnection(eventHandler))
		self._loop.run_forever()

	async def createConnection(self, eventHandler):
		context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
		if not self._verify:
			context.verify_mode = ssl.CERT_NONE

		if self.urlparts.scheme == 'https':
			scheme = 'wss://'
		else:
			scheme = 'ws://'

		url = scheme + self.urlparts.hostname + self.apiUrl + '/users/websocket'

		async with websockets.connect(
				url,
				ssl=context,
				extra_headers={'Cookie': 'MMAUTHTOKEN={}'.format(self._cookie)}
		) as websocket:
			self._websocket = websocket
			# TODO: Use a cookie in websocket connection, because of a bug in mattermost
			# https://github.com/mattermost/platform/pull/5406
			# if not await self._authenticateWebsocket(websocket):
			#	raise MattermostClientError('Could not authenticate Websocket connection.')
			await self._startLoop(websocket, eventHandler)

	async def _startLoop(self, websocket, eventHandler):
		"""
		We will listen for websockets events, sending a heartbeat/pong everytime
		we react a TimeoutError. If we don't the webserver would close the idle connection,
		forcing us to reconnect.
		"""
		log.debug('Starting websocket loop')
		while True:
			try:
				await asyncio.wait_for(
					self.waitForMessage(websocket, eventHandler),
					timeout=self._timeout
				)
			except asyncio.TimeoutError:
				await websocket.pong()
				log.debug("Sending heartbeat...")
				continue

	async def _authenticateWebsocket(self, websocket):
		"""
		Sends a authentication challenge over a websocket.
		This is not needed when we just send the cookie we got on login
		when connecting to the websocket.
		Currently (Mattermost 3.6.2) won't send all events when authenticated this way
		"""
		jsonData = json.dumps({
			"seq": 1,
			"action": "authentication_challenge",
			"data": {
				"token": self.token
			}
		}).encode('utf8')
		await websocket.send(jsonData)
		response = await websocket.recv()
		status = json.loads(response)
		if ('status' in status and status['status'] == 'OK') and \
				('seq_reply' in status and status['seq_reply'] == 1):
			log.info('Authentification OK')
			return True
		else:
			log.error(status)
			return False

	async def waitForMessage(self, websocket, eventHandler):
		while True:
			message = await websocket.recv()
			await eventHandler(message)
