import logging
from errbot.backends.base import RoomOccupant
from .mattermostPerson import MattermostPerson

log = logging.getLogger('errbot.backends.mattermost.roomOccupant')


class MattermostRoomOccupant(RoomOccupant, MattermostPerson):
	"""
	A Person inside a Team (Room)
	"""
	def __init__(self, client, teamid, userid, channelid, bot):
		super().__init__(client, userid, channelid)
		self._teamid = teamid
		# Importing inside __init__ to prevent a circular import, which is ugly
		from .mattermostRoom import MattermostRoom
		self._room = MattermostRoom(channelid=channelid, teamid=teamid, bot=bot)

	@property
	def room(self):
		return self._room

	def __unicode__(self):
		return "~{}/{}".format(self._room.name, self.username)

	def __str__(self):
		return self.__unicode__()

	def __eq__(self, other):
		if not isinstance(other, RoomOccupant):
			log.warning('tried to compare a MattermostRoomOccupant with a MattermostPerson \
					{} vs {}'.format(self, other))
			return False
		return other.room.id == self.room.id and other.userid == self.userid