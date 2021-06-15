from typing import Iterator, Optional

from .abc import BaseUser
from .endpoints import Endpoints
from .exceptions import LoginRequired


class CodinGamer(BaseUser):
    """Represents a CodinGamer.

    Do not create this class yourself. Only get it through :meth:`Client.get_codingamer()`.

    Attributes
    -----------
        public_handle: :class:`str`
            Public handle of the CodinGamer (hexadecimal str).

        id: :class:`int`
            ID of the CodinGamer. Last 7 digits of the :attr:`public_handle` reversed.

        rank: :class:`int`
            Worldwide rank of the CodinGamer.

        level: :class:`int`
            Level of the CodinGamer.

        xp: :class:`int`
            XP points of the CodinGamer.

        country_id: :class:`str`
            Country ID of the CodinGamer.

        category: Optional[:class:`str`]
            Category of the CodinGamer. Can be ``STUDENT`` or ``PROFESSIONAL``.

            .. note::
                You can use :attr:`student` and :attr:`professional` to get a :class:`bool` that
                describes the CodinGamer's category.

        student: :class:`bool`
            If the CodinGamer is a student.

        professional: :class:`bool`
            If the CodinGamer is a professional.

        pseudo: Optional[:class:`str`]
            Pseudo of the CodinGamer, if set else `None`.

        tagline: Optional[:class:`str`]
            Tagline of the CodinGamer, if set else `None`.

        biography: Optional[:class:`str`]
            Biography of the CodinGamer, if set else `None`.

        company: Optional[:class:`str`]
            Company of the CodinGamer, if set else `None`.

        school: Optional[:class:`str`]
            School of the CodinGamer, if set else `None`.

        avatar: Optional[:class:`int`]
            Avatar ID of the CodinGamer, if set else `None`.
            You can get the avatar url with :attr:`avatar_url`.

        cover: Optional[:class:`int`]
            Cover ID of the CodinGamer, if set else `None`.
            You can get the cover url with :attr:`cover_url`.

        avatar_url: Optional[:class:`str`]
            Avatar URL of the CodinGamer, if set else `None`.

        cover_url: Optional[:class:`str`]
            Cover URL of the CodinGamer, if set else `None`.
    """

    public_handle: str
    id: int
    rank: int
    level: int
    xp: int
    country_id: Optional[str]
    category: Optional[str]
    student: bool
    professional: bool
    pseudo: Optional[str]
    tagline: Optional[str]
    biography: Optional[str]
    company: Optional[str]
    school: Optional[str]
    avatar: Optional[int]
    cover: Optional[int]
    avatar_url: Optional[str]
    cover_url: Optional[str]

    def __init__(self, *, client, **data):
        self._client = client

        self.public_handle = data["publicHandle"]
        self.id = data["userId"]
        self.level = data["level"]
        self.country_id = data.get("countryId")

        self.category = (
            data["category"]
            if data.get("category", "UNKNOWN") != "UNKNOWN"
            else None
        )
        self.student = self.category == "STUDENT"
        self.professional = self.category == "PROFESSIONAL"

        self.xp = data.get("xp", None)
        self.rank = data.get("rank", None)
        self.pseudo = data.get("pseudo", None) or None
        self.tagline = data.get("tagline", None) or None
        self.biography = data.get("biography", None) or None
        self.company = (
            data.get("company", None) or data.get("companyField", None) or None
        )
        self.school = (
            data.get("schoolField", None)
            or data.get("formValues", {}).get("school", None)
            or None
        )

        self.avatar = data.get("avatar", None)
        self.cover = data.get("cover", None)

    @property
    def followers(self) -> Iterator:
        """Get all the followers of a CodinGamer.

        You need to be logged in as the CodinGamer to get its followers
        or else a :exc:`LoginRequired` will be raised. If you can't log in,
        you can use :meth:`CodinGamer.followers_ids`.

        .. note::
            This property is a generator.

        Raises
        ------
            :exc:`LoginRequired`
                The Client needs to log in. See :meth:`Client.login`.

        Yields
        -------
            :class:`CodinGamer`
                The follower.
        """

        if (
            not self._client.logged_in
            or self.public_handle != self._client.codingamer.public_handle
        ):
            raise LoginRequired()

        r = self._client._session.post(
            Endpoints.CodinGamer_followers, json=[self.id, self.id, None]
        )
        for follower in r.json():
            yield CodinGamer(client=self._client, **follower)

    @property
    def followers_ids(self) -> list:
        """Get all the followers ids of a CodinGamer.

        Returns
        -------
            :class:`list`
                A list of all the followers ids. See :attr:`CodinGamer.id`.
        """

        r = self._client._session.post(
            Endpoints.CodinGamer_followers_ids, json=[self.id]
        )
        return r.json()

    @property
    def following(self) -> Iterator:
        """Get all the followed CodinGamers.

        You need to be logged in as the CodinGamer to get its followed CodinGamers
        or else a :exc:`LoginRequired` will be raised. If you can't log in,
        you can use :meth:`CodinGamer.following_ids`.

        .. note::
            This property is a generator.

        Raises
        ------
            :exc:`LoginRequired`
                The Client needs to log in. See :meth:`Client.login`.

        Yields
        -------
            :class:`CodinGamer`
                The followed CodinGamer.
        """

        if (
            not self._client.logged_in
            or self.public_handle != self._client.codingamer.public_handle
        ):
            raise LoginRequired()

        r = self._client._session.post(
            Endpoints.CodinGamer_following, json=[self.id, self.id]
        )
        for followed in r.json():
            yield CodinGamer(client=self._client, **followed)

    @property
    def following_ids(self) -> list:
        """Get all the followed ids of a CodinGamer.

        Returns
        -------
            :class:`list`
                A list of all the followed ids. See :attr:`CodinGamer.id`.
        """

        r = self._client._session.post(
            Endpoints.CodinGamer_following_ids, json=[self.id]
        )
        return r.json()

    @property
    def clash_of_code_rank(self) -> int:
        """Get the Clash of Code rank of the CodinGamer.

        Returns
        -------
            :class:`int`
                The Clash of Code rank of the CodinGamer.
        """

        r = self._client._session.post(
            Endpoints.CodinGamer_coc_rank, json=[self.id]
        )
        return r.json()["rank"]
