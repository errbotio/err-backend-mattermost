import logging
from errbot.backends.base import Person

log = logging.getLogger("errbot.backends.mattermost.person")


class MattermostPerson(Person):
    """
    A Person in Mattermost
    """

    def __init__(self, driver, userid=None, channelid=None, teamid=None):
        self._userid = userid
        self._channelid = channelid
        self._teamid = teamid
        self._driver = driver

    @property
    def userid(self) -> str:
        return self._userid

    @property
    def username(self) -> str:
        user = self._driver.users.get_user(user_id=self.userid)
        if "username" not in user:
            log.error("Can't find username for user with ID {}".format(self._userid))
            return "<{}>".format(self._userid)
        return user["username"]

    @property
    def email(self) -> str:
        user = self._driver.users.get_user(user_id=self.userid)
        return user.get("email", "")

    @property
    def teamid(self) -> str:
        return self._teamid

    @property
    def channelid(self) -> str:
        return self._channelid

    @property
    def nick(self) -> str:
        return self.username

    @property
    def client(self) -> str:
        return self._channelid

    @property
    def domain(self) -> str:
        return self._driver.client.url

    @property
    def fullname(self):
        user = self._driver.users.get_user(user_id=self.userid)

        fullname = user.get("first_name", "")
        if fullname == "":
            log.warning("No first name for user with ID {}".format(self._userid))

        fullname += " {}".format(user.get("last_name", ""))
        if fullname == "{} ".format(user.get("first_name", "")):
            log.warning("No surname for user with ID {}".format(self._userid))
            fullname.strip()

        return f"{fullname}"

    @property
    def person(self):
        return "@{}".format(self.username)

    @property
    def aclattr(self):
        return "@{}".format(self.username)

    def __unicode__(self):
        return "@{}".format(self.username)

    def __str__(self):
        return self.__unicode__()

    def __eq__(self, other):
        if not isinstance(other, MattermostPerson):
            log.warning("Tried to compare a MattermostPerson with a %s", type(other))
            return False
        return other.userid == self.userid
