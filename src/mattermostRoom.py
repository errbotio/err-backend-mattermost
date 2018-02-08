import logging
from errbot.backends.base import Room, RoomDoesNotExistError, RoomError, UserDoesNotExistError
from mattermostdriver.exceptions import NotEnoughPermissions, ResourceNotFound, InvalidOrMissingParameters
from .mattermostRoomOccupant import MattermostRoomOccupant

log = logging.getLogger('errbot.backends.mattermost.room')


class MattermostRoom(Room):
	def __init__(self, name=None, channelid=None, teamid=None, bot=None):
		if channelid is not None and name is not None:
			raise ValueError("channelid and name are mutually exclusive")
		if teamid is None:
			raise ValueError("teamid is not optional")

		if name is not None:
			if name.startswith('~'):
				self._name = name[1:]
			else:
				self._name = name
		else:
			self._name = bot.channelid_to_channelname(channelid)

		self._teamid = teamid
		self._id = None if channelid is None else channelid
		if self._id is None and name is not None:
			try:
				self._id = bot.channelname_to_channelid(name)
			except RoomDoesNotExistError as e:
				# If the room does not exist, maybe it will be created.
				log.info(e)
		self._bot = bot
		self.driver = bot.driver

	@property
	def teamid(self):
		return self._teamid

	@property
	def name(self):
		return self._name

	@property
	def id(self):
		if self._id is None:
			self._id = self._channel['id']
		return self._id

	channelid = id

	@property
	def _channel(self):
		channel = self.driver.channels.get_channel_by_name(team_id=self.teamid, channel_name=self.name)
		if 'status_code' in channel and channel['status_code'] != 200:
			raise RoomDoesNotExistError("{}: {}".format(channel['status_code'], channel['message']))
		return channel

	@property
	def _channel_info(self):
		return NotImplementedError("TODO")

	@property
	def private(self):
		return self._channel.type == 'P'

	@property
	def exists(self):
		channels = []
		channels.extend(self.driver.channels.get_channels_for_user(user_id='me', team_id=self.teamid))
		public_channels = self._bot.get_public_channels()
		for channel in public_channels:
			if channel not in channels:
				channels.append(channel)
		return len([c for c in channels if c['name'] == self.name]) > 0

	@property
	def joined(self):
		channels = self.driver.channels.get_channels_for_user(user_id='me', team_id=self.teamid)
		return len([c for c in channels if c['name'] == self.name]) > 0

	@property
	def topic(self):
		if self._channel['header'] == '':
			return None
		else:
			return self._channel['header']

	@topic.setter
	def topic(self, topic):
		self.driver.channels.update_channel(
			channel_id=self.id,
			options={'header': topic, 'id': self.id}
		)

	@property
	def purpose(self):
		if self._channel['purpose'] == '':
			return None
		else:
			return self._channel['purpose']

	@purpose.setter
	def purpose(self, purpose):
		self.driver.channels.update_channel(
			channel_id=self.id,
			options={'purpose': purpose, 'id': self.id}
		)

	@property
	def occupants(self):
		member_count = self.driver.channels.get_channel_statistics(channel_id=self.id)['member_count']
		members = []
		user_page_limit = 200
		for start in range(0, member_count, user_page_limit):
			member_part = self.driver.channels.get_channel_members(
					channel_id=self.id,
					params={'page': start, 'per_page': user_page_limit}
				)
			members.extend(member_part)

		room_occupants = [MattermostRoomOccupant(
				self.driver,
				userid=m['user_id'],
				teamid=self.teamid,
				channelid=self.id,
				bot=self._bot
			) for m in members]
		return room_occupants

	def create(self, private=False):
		channel_type = 'O'
		if private:
			log.info("Creating private group {}".format(str(self)))
			channel_type = 'P'
		else:
			log.info("Creating public channel {}".format(str(self)))
		try:
			self.driver.channels.create_channel(options={
				'team_id': self.teamid,
				'name': self.name,
				'display_name': self.name,
				'type': channel_type
			})
			self.driver.channels.get_channel_by_name(team_id=self.teamid, channel_name=self.name)
			self._bot.callback_room_joined(self)
		except (NotEnoughPermissions, ResourceNotFound) as e:
			raise RoomError(e)

	def join(self, username: str=None, password: str=None):
		if not self.exists:
			log.info("Channel {} doesn't seem exist, trying to create it.".format(str(self)))
			self.create()  # This always creates a public room!
		log.info("Joining channel {}".format(str(self)))
		try:
			self.driver.channels.add_user(
				channel_id=self._id,
				options={
					'user_id': self._bot.userid
				}
			)
			self._bot.callback_room_joined(self)
		except (InvalidOrMissingParameters, NotEnoughPermissions) as e:
			raise RoomError(e)

	def leave(self, reason: str=None):
		log.info('Leaving channel {} ({})'.format(str(self), self.id))
		try:
			self.driver.channels.remove_user_from_channel(channel_id=self.id, user_id=self._bot.id)
			self._bot.callback_room_left(self)
		except (InvalidOrMissingParameters, NotEnoughPermissions) as e:
			raise RoomError(e)

	def destroy(self):
		try:
			self.driver.channels.delete_channel(channel_id=self.id)
			self._bot.callback_room_left(self)
		except (InvalidOrMissingParameters, NotEnoughPermissions) as e:
			log.debug('Could not delete the channel. Are you a member of the channel?')
			raise RoomError(e)
		self._id = None

	def invite(self, *args):
		user_count = self.driver.teams.get_team_stats(team_id=self.teamid)['total_member_count']
		user_page_limit = 200
		users_not_in_channel = []
		for start in range(0, user_count, user_page_limit):
			users_not_in_channel.extend(self.driver.users.get_users(
				params={
					'page': start,
					'per_page': user_page_limit,
					'in_team': self.teamid,
					'not_in_channel': self.id
				}
			))
		users = {}
		for user in users_not_in_channel:
			users.update({user['username']: user['id']})
		for user in args:
			if user not in users:
				raise UserDoesNotExistError('User \'{}\' not found'.format(user))
			log.info('Inviting {} into {} ({})'.format(user, str(self), self.id))

			try:
				self.driver.channels.add_user(channel_id=self.id, options={'user_id': users[user]})
			except (InvalidOrMissingParameters, NotEnoughPermissions):
				raise RoomError("Unable to invite {} to channel {} ({})".format(
					user, str(self), self.id
				))

	def __str__(self):
		return "~{}".format(self._name)

	def __eq__(self, other):
		if not isinstance(other, MattermostRoom):
			return False
		return self.id == other.id