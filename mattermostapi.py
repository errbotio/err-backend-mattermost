import json

import requests
import logging
import time

from urllib import parse

logging.basicConfig(level=logging.INFO)

log = logging.getLogger('mattermost.api')

# TODO: Probably should replace that with the official swagger api, but it doesn't seem complete

class MattermostApiResponseError(Exception):
	"""Raise when the api does return a statuscode other then 200"""

class MattermostApi:
	def __init__(self, url, verify=True):
		self._url = url + '/api/v3'
		self._token = ''
		self._verify = verify

	@property
	def token(self):
		return self._token

	def login(self, email, password, token=None, device_id=None):
		""" Login with user Credentials. Token is for MF-Auth. """
		loginData = {'login_id': email, 'password': password}
		if token:
			loginData['token'] = token
		if device_id:
			loginData['device_id'] = device_id
		loginRequest = requests.post(self._url + '/users/login', json=loginData, verify=self._verify)
		loginRequest.raise_for_status()
		self._token = loginRequest.headers['Token']
		return loginRequest

	def logout(self):
		self.post('/users/logout')
		self._token = ''

	def authHeader(self):
		if self._token == "":
			log.error("You need to Log in first")
			raise Exception("You need to Log in first")
		return {"Authorization": "Bearer {}".format(self._token)}

	def get(self, request):
		header = self.authHeader()
		getRequest = requests.get(self._url + request, headers=header, verify=self._verify)
		data = json.loads(getRequest.text)
		log.debug(data)
		if 'status_code' in data and data['status_code'] != 200:
			raise MattermostApiResponseError(data)
		return data

	def post(self, request, jsonData=None, data=None, files=None):
		header = self.authHeader()
		postRequest = requests.post(
				self._url + request,
				headers=header,
				json=jsonData,
				data=data,
				files=files,
				verify=self._verify
		)
		data = json.loads(postRequest.text)
		log.debug(data)
		if 'status_code' in data and data['status_code'] != 200:
			raise MattermostApiResponseError(data)
		return data

	def createNewUser(self, email, username, password, first_name=None, last_name=None,
			nickname=None, locale=None, props=None):
		jsonData = {'email': email, 'username': username, 'password': password}
		if first_name:
			jsonData['first_name'] = first_name
		if last_name:
			jsonData['last_name'] = last_name
		if nickname:
			jsonData['nickname'] = nickname
		if locale:
			jsonData['locale'] = locale
		if props:
			jsonData['props'] = props
		return self.post('/users/create', jsonData)

	def getCurrentUser(self):
		return self.get('/users/me')

	def getUsers(self, offset=0, limit=50):
		return self.get('/users/{}/{}'.format(offset, limit))

	def getUsersInTeam(self, team_id, offset=0, limit=50):
		return self.get('/teams/{}/users/{}/{}'.format(
			team_id,
			offset,
			limit
		))

	def searchUsers(self, term, team_id=None, in_channel_id=None,
			not_in_channel_id=None, allow_inactive=None):
		jsonData = {'term': term}
		if team_id:
			jsonData['team_id'] = team_id
		if in_channel_id:
			jsonData['in_channel_id'] = in_channel_id
		if not_in_channel_id:
			jsonData['not_in_channel_id'] = not_in_channel_id
		if allow_inactive:
			jsonData['allow_inactive'] = allow_inactive
		return self.post('/users/search', jsonData)

	def getUserByUsername(self, username):
		return self.get('/users/name/{}'.format(username))

	def getUserByEmail(self, email):
		return self.get('/users/email/{}'.format(email))

	def getUserIDs(self, userIds):
		jsonData = json.dumps(userIds, ensure_ascii=False, sort_keys=False).encode('utf8')
		return self.post('/users/ids', data=jsonData)

	def getUsersInChannel(self, team_id, channel_id, offset=0, limit=50):
		return self.get('/teams/{}/channels/{}/users/{}/{}'.format(
			team_id,
			channel_id,
			offset,
			limit
		))

	def getUsersNotInChannel(self, team_id, channel_id, offset=0, limit=50):
		return self.get('/teams/{}/channels/{}/users/not_in_channel/{}/{}'.format(
			team_id,
			channel_id,
			offset,
			limit
		))

	def updateUser(self, id=None, create_at=None, update_at=None, delete_at=None, username=None,
			first_name=None, last_name=None, nickname=None, email=None, email_verified=None,
			password=None, authData=None, auth_service=None, roles=None, locale=None,
			notify_props=None, props=None, last_password_update=None, last_picture_update=None,
			failed_attempts=None, mfa_active=None, mfa_secret=None):
		jsonData = {}
		if id:
			jsonData['id'] = id
		if create_at:
			jsonData['create_at'] = create_at
		if update_at:
			jsonData['update_at'] = update_at
		if delete_at:
			jsonData['delete_at'] = delete_at
		if username:
			jsonData['username'] = username
		if first_name:
			jsonData['first_name'] = first_name
		if last_name:
			jsonData['last_name'] = last_name
		if nickname:
			jsonData['nickname'] = nickname
		if email:
			jsonData['email'] = email
		if email_verified:
			jsonData['email_verified'] = email_verified
		if password:
			jsonData['password'] = password
		if authData:
			jsonData['auth_data'] = authData
		if auth_service:
			jsonData['auth_service'] = auth_service
		if roles:
			jsonData['roles'] = roles
		if locale:
			jsonData['locale'] = locale
		if notify_props:
			jsonData['notify_props'] = notify_props
		if props:
			jsonData['props'] = props
		if last_password_update:
			jsonData['last_password_update'] = last_password_update
		if last_picture_update:
			jsonData['last_picture_update'] = last_picture_update
		if failed_attempts:
			jsonData['failed_attempts'] = failed_attempts
		if mfa_active:
			jsonData['mfa_active'] = mfa_active
		if mfa_secret:
			jsonData['mfa_secret'] = mfa_secret
		return self.post('/users/update', jsonData)

	def updateUserRole(self, user_id, team_id, roles):
		jsonData = {'user_id': user_id, 'roles': roles}
		if team_id:
			jsonData['team_id'] = team_id
		return self.post('/users/update_roles', jsonData)

	def setUserState(self, user_id, active):
		jsonData = {'user_id': user_id, 'active': active}
		return self.post('/users/update_active', jsonData)

	def updateUserNotify(self, notify_props):
		return self.post('/users/update_notify', notify_props)

	def sendPasswordResetMail(self, email):
		return self.post('/users/send_password_reset', {'email': email})

	def autocompleteUser(self, term):
		query = parse.urlencode({'term' : term})
		return self.get('/users/autocomplete?{}'.format(query))

	def autocompleteUsersInTeam(self, team_id, term):
		query = parse.urlencode({'term' : term})
		return self.get('/teams/{}/users/autocomplete?{}'.format(team_id, query))

	def autocompleteUsersInChannel(self, team_id, channel_id, term):
		query = parse.urlencode({'term' : term})
		return self.get('/teams/{}/channels/{}/users/autocomplete?{}'.format(
			team_id,
			channel_id,
			query
		))

	def createNewTeam(self, name, display_name, type='O'):
		if type != 'O' and type != 'I':
			return False
		jsonData = {'name': name, 'display_name': display_name, 'type': type}
		return self.post('/teams/create', jsonData)

	def getAllTeams(self):
		return self.get('/teams/all')

	def getAllTeamsWithMembership(self):
		return self.get('/teams/members')

	def getUnreadCount(self, id=None):
		if id:
			query = parse.urlencode({'id': id})
			return self.get('/teams/unread?{}'.format(id))
		else:
			return self.get('/teams/unread')

	def getTeamMembers(self, team_id, offset=0, limit=50):
		return self.get('/teams/{}/members/{}/{}'.format(
			team_id,
			offset,
			limit
		))

	def getSingleTeamMember(self, team_id, user_id):
		return self.get('/teams/{}/members/{}'.format(team_id, user_id))

	def getTeamMembersById(self, team_id, userIds):
		"""
		Get all given userIds from team_id
		:param team_id: string
		:param userIds: array
		:return:
		"""
		jsonData = json.dumps(userIds, ensure_ascii=False, sort_keys=False).encode('utf8')
		return self.post('/teams/{}/members/ids'.format(team_id), data=jsonData)

	def getTeamObjectById(self, team_id):
		return self.get('/teams/{}/me'.format(team_id))

	def getTeamObjectByName(self, teamName):
		return self.get('/teams/name/{}'.format(teamName))

	def updateTeamObject(self, team_id, id=None, create_at=None, update_at=None, delete_at=None,
			display_name=None, name=None, description=None, email=None, type=None,
			allowed_domains=None, invite_id=None, allow_open_invite=None):
		jsonData = {}
		if id:
			jsonData['id'] = id
		if create_at:
			jsonData['create_at'] = create_at
		if update_at:
			jsonData['update_at'] = update_at
		if delete_at:
			jsonData['delete_at'] = delete_at
		if display_name:
			jsonData['display_name'] = display_name
		if name:
			jsonData['name'] = name
		if description:
			jsonData['description'] = description
		if email:
			jsonData['email'] = email
		if type:
			jsonData['type'] = type
		if allowed_domains:
			jsonData['allowed_domains'] = allowed_domains
		if invite_id:
			jsonData['invite_id'] = invite_id
		if allow_open_invite:
			jsonData['allow_open_invite'] = allow_open_invite
		return self.post('/teams/{}/update'.format(team_id), jsonData)

	def getTeamStats(self, team_id):
		return self.get('/teams/{}/stats'.format(team_id))

	def addUserToTeam(self, team_id, user_id):
		jsonData = {'user_id': user_id}
		return self.post('/teams/{}/add_user_to_team'.format(team_id), jsonData)

	def removeUserFromTeam(self, team_id, user_id):
		jsonData = {'user_id': user_id}
		return self.post('/teams/{}/remove_user_from_team'.format(team_id), jsonData)

	def getAllSlashCommandsForTeam(self, team_id):
		return self.get('/teams/{}/commands/list_team_commands'.format(team_id))

	def createChannel(self, team_id, name, display_name, purpose=None, header=None, type='O'):
		if type != 'O' and type != 'P':
			return False
		jsonData = {'team_id': team_id, 'name': name, 'display_name': display_name, 'type': type}
		if purpose:
			jsonData['purpose'] = purpose
		if header:
			jsonData['header'] = header
		return self.post('/teams/{}/channels/create'.format(team_id), jsonData)

	def updateChannel(self, team_id, id=None, create_at=None, update_at=None, delete_at=None,
			type=None, display_name=None, name=None, header=None, purpose=None, last_post_at=None,
			total_msg_count=None, extra_update_at=None, creator_id=None):
		jsonData = {'team_id': team_id}
		if id:
			jsonData['id'] = id
		if create_at:
			jsonData['create_at'] = create_at
		if update_at:
			jsonData['update_at'] = update_at
		if delete_at:
			jsonData['delete_at'] = delete_at
		if type:
			jsonData['type'] = type
		if display_name:
			jsonData['display_name'] = display_name
		if name:
			jsonData['name'] = name
		if header:
			jsonData['header'] = header
		if purpose:
			jsonData['purpose'] = purpose
		if last_post_at:
			jsonData['last_post_at'] = last_post_at
		if total_msg_count:
			jsonData['total_msg_count'] = total_msg_count
		if extra_update_at:
			jsonData['extra_update_at'] = extra_update_at
		if creator_id:
			jsonData['creator_id'] = creator_id
		return self.post('/teams/{}/channels/update'.format(team_id), jsonData)

	def joinChannel(self, team_id, channel_id):
		return self.post('/teams/{}/channels/{}/join'.format(team_id, channel_id))

	def joinChannelByName(self, team_id, channel_name):
		return self.post('/teams/{}/channels/name/{}/join'.format(team_id, channel_name))

	def leaveChannel(self, team_id, channel_id):
		return self.post('/teams/{}/channels/{}/leave'.format(team_id, channel_id))

	def leaveChannelByName(self, team_id, channel_name):
		return self.post('/teams/{}/channels/name/{}/leave'.format(team_id, channel_name))

	def viewChannel(self, team_id, channel_id, prev_channel_id='', time=time.time()):
		jsonData = {
			'channel_id': channel_id,
			'time': time,
			'prev_channel_id': prev_channel_id
		}
		return self.post('/teams/{}/channels/view'.format(team_id), jsonData)

	def getChannelsForUserInTeam(self, team_id):
		return self.get('/teams/{}/channels/'.format(team_id))

	def getChannelByName(self, team_id, channel_name):
		return self.get('/teams/{}/channels/name/{}'.format(team_id, channel_name))

	def getChannelsUserHasNotJoined(self, team_id):
		return self.get('/teams/{}/channels/more'.format(team_id))

	def getChannelsPageUserHasNotJoined(self, team_id, offset=0, limit=50):
		return self.get('/teams/{}/channels/more/{}/{}'.format(
			team_id,
			offset,
			limit
		))

	def getChannelMembersForUser(self, team_id):
		return self.get('/teams/{}/channels/members'.format(team_id))

	def getChannel(self, team_id, channel_id):
		return self.get('/teams/{}/channels/{}/'.format(team_id, channel_id))

	def getChannelStats(self, team_id, channel_id):
		return self.get('/teams/{}/channels/{}/stats'.format(team_id, channel_id))

	def deleteChannel(self, team_id, channel_id):
		return self.post('/teams/{}/channels/{}/delete'.format(team_id, channel_id))

	def addUserToChannel(self, team_id, channel_id, user_id):
		jsonData = {'user_id': user_id}
		return self.post('/teams/{}/channels/{}/add'.format(team_id, channel_id), jsonData)

	def getChannelMembers(self, team_id, channel_id):
		return self.get('/teams/{}/channels/{}/members'.format(
			team_id,
			channel_id
		))

	def getChannelMember(self, team_id, channel_id, user_id):
		return self.get('/teams/{}/channels/{}/members/{}'.format(
			team_id,
			channel_id,
			user_id
		))

	def createDirectChannel(self, team_id, user_id):
		jsonData = {'user_id': user_id}
		return self.post('/teams/{}/channels/create_direct'.format(team_id), jsonData=jsonData)

	def getChannelMembersById(self, team_id, channel_id, userIds):
		jsonData = json.dumps(userIds, ensure_ascii=False, sort_keys=False).encode('utf8')
		return self.post('/teams/{}/channels/{}/members/ids'.format(team_id, channel_id), data=jsonData)

	def updateRoleOfUserInChannel(self, team_id, channel_id, user_id, new_roles):
		jsonData = {'user_id': user_id, 'new_roles': new_roles}
		return self.post('/teams/{}/channels/{}/update_member_roles'.format(
			team_id,
			channel_id
		), jsonData)

	def autocompleteChannelsInTeam(self, team_id, term):
		query = parse.urlencode({'term' : term})
		return self.get('/teams/{}/channels/autocomplete?{}'.format(team_id, query))

	def searchMoreChannels(self, team_id, term):
		query = parse.urlencode({'term' : term})
		return self.get('/teams/{}/channels/more/search?{}'.format(team_id, query))

	def searchPosts(self, team_id, terms, is_or_search=False):
		jsonData = {'terms': terms, 'is_or_search': is_or_search}
		return self.post('/teams/{}/posts/search'.format(team_id), jsonData)

	def getAllFlaggedPostsForUser(self, team_id, offset=0, limit=50):
		return self.get('/teams/{}/flagged/{}/{}'.format(team_id, offset, limit))

	def createPost(self, team_id, channel_id, id=None, create_at=None, update_at=None, delete_at=None,
			user_id=None, root_id=None, parent_id=None, original_id=None, message=None,
			type=None, props=None, hashtag=None, filenames=None, pending_post_id=None):
		jsonData = {'team_id': team_id, 'channel_id': channel_id}
		if id:
			jsonData['id'] = id
		if create_at:
			jsonData['create_at'] = create_at
		if update_at:
			jsonData['update_at'] = update_at
		if delete_at:
			jsonData['delete_at'] = delete_at
		if type:
			jsonData['type'] = type
		if user_id:
			jsonData['user_id'] = user_id
		if root_id:
			jsonData['root_id'] = root_id
		if parent_id:
			jsonData['parent_id'] = parent_id
		if original_id:
			jsonData['original_id'] = original_id
		if message:
			jsonData['message'] = message
		if props:
			jsonData['props'] = props
		if hashtag:
			jsonData['hashtag'] = hashtag
		if filenames:
			jsonData['filenames'] = filenames
		if pending_post_id:
			jsonData['pending_post_id'] = pending_post_id
		return self.post('/teams/{}/channels/{}/posts/create'.format(
			team_id,
			channel_id
		), jsonData)

	def updatePost(self, team_id, channel_id, id=None, create_at=None, update_at=None, delete_at=None,
			user_id=None, root_id=None, parent_id=None, original_id=None, message=None,
			type=None, props=None, hashtag=None, filenames=None, pending_post_id=None):
		jsonData = {'team_id': team_id, 'channel_id': channel_id}
		if id:
			jsonData['id'] = id
		if create_at:
			jsonData['create_at'] = create_at
		if update_at:
			jsonData['update_at'] = update_at
		if delete_at:
			jsonData['delete_at'] = delete_at
		if type:
			jsonData['type'] = type
		if user_id:
			jsonData['user_id'] = user_id
		if root_id:
			jsonData['root_id'] = root_id
		if parent_id:
			jsonData['parent_id'] = parent_id
		if original_id:
			jsonData['original_id'] = original_id
		if message:
			jsonData['message'] = message
		if props:
			jsonData['props'] = props
		if hashtag:
			jsonData['hashtag'] = hashtag
		if filenames:
			jsonData['filenames'] = filenames
		if pending_post_id:
			jsonData['pending_post_id'] = pending_post_id
		return self.post('/teams/{}/channels/{}/posts/update'.format(
			team_id,
			channel_id
		), jsonData)

	def getPostsForChannel(self, team_id, channel_id, offset=0, limit=50):
		return self.get('/teams/{}/channels/{}/posts/page/{}/{}'.format(
			team_id,
			channel_id,
			offset,
			limit
		))

	def getPostsSinceTime(self, team_id, channel_id, time):
		return self.get('/teams/{}/channels/{}/posts/since/{}'.format(
			team_id,
			channel_id,
			time
		))

	def getPost(self, team_id, channel_id, post_id):
		return self.get('/teams/{}/channels/{}/posts/{}/get'.format(
			team_id,
			channel_id,
			post_id
		))

	def deletePost(self, team_id, channel_id, post_id):
		return self.get('/teams/{}/channels/{}/posts/{}/delete'.format(
			team_id,
			channel_id,
			post_id
		))

	def getPostsBeforePost(self, team_id, channel_id, post_id, offset=0, limit=50):
		return self.get('/teams/{}/channels/{}/posts/{}/before/{}/{}'.format(
			team_id,
			channel_id,
			post_id,
			offset,
			limit
		))

	def getPostsAfterPost(self, team_id, channel_id, post_id, offset=0, limit=50):
		return self.get('/teams/{}/channels/{}/posts/{}/after/{}/{}'.format(
			team_id,
			channel_id,
			post_id,
			offset,
			limit
		))

	def getPostReactions(self, team_id, channel_id, post_id):
		return self.get('/teams/{}/channels/{}/posts/{}/reactions'.format(
			team_id,
			channel_id,
			post_id
		))

	def reactToPost(self, team_id, channel_id, post_id, user_id=None, emoji_name=None, create_at=None):
		jsonData = {'post_id': post_id}
		if user_id:
			jsonData['user_id'] = user_id
		if emoji_name:
			jsonData['emoji_name'] = emoji_name
		if create_at:
			jsonData['create_at'] = create_at
		return self.post('/teams/{}/channels/{}/posts/{}/reactions/save'.format(
			team_id,
			channel_id,
			post_id
		), jsonData)

	def removeReactionFromPost(self, team_id, channel_id, post_id, user_id=None, emoji_name=None,
			create_at=None):
		jsonData = {'post_id': post_id}
		if user_id:
			jsonData['user_id'] = user_id
		if emoji_name:
			jsonData['emoji_name'] = emoji_name
		if create_at:
			jsonData['create_at'] = create_at
		return self.post('/teams/{}/channels/{}/posts/{}/reactions/delete'.format(
			team_id,
			channel_id,
			post_id
		), jsonData)

	def uploadFile(self, team_id, channel_id, files, client_ids):
		jsonData = {'channel_id': channel_id}
		if client_ids:
			jsonData['client_ids'] = client_ids
		return self.post('/teams/{}/files/upload'.format(team_id), jsonData=jsonData, files=files)

	def getFile(self, file_id):
		return self.get('/files/{}/get'.format(file_id))

	def getImageThumbnail(self, file_id):
		return self.get('/files/{}/get_thumbnail'.format(file_id))

	def getImagePreview(self, file_id):
		return self.get('/files/{}/get_preview'.format(file_id))

	def getFileMetadata(self, file_id):
		return self.get('/files/{}/get_info'.format(file_id))

	def getPublicFileLink(self, file_id):
		return self.get('/files/{}/get_public_link'.format(file_id))

	def saveUserPreferences(self, preferences):
		""" preferences needs to be correct JSON, when you pass it! """
		return self.post('/preferences/save', data=preferences)

	def deleteUserPreferences(self, preferences):
		""" preferences needs to be correct JSON, when you pass it! """
		return self.post('/preferences/delete', data=preferences)

	def listUserPreferences(self, category):
		return self.get('/preferences/{}'.format(category))

	def getSpecificPreference(self, category, name):
		return self.get('/preferences/{}/name'.format(category, name))

	def listIncomingWebhooksForTeam(self, team_id):
		return self.get('/teams/{}/hooks/incoming/list'.format(team_id))

	def createIncomingWebhookForTeam(self, team_id, channel_id, display_name=None, description=None):
		jsonData = {'channel_id': channel_id}
		if display_name:
			jsonData['display_name'] = display_name
		if description:
			jsonData['description'] = description
		return self.post('/teams/{}/hooks/incoming/create'.format(team_id), jsonData)

	def deleteIncomingWebhookForTeam(self, team_id, webhook_id):
		jsonData = {'id': webhook_id}
		return self.post('/teams/{}/hooks/incoming/delete'.format(team_id), jsonData)

