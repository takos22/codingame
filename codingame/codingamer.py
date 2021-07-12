import typing

from .abc import BaseUser
from .exceptions import LoginRequired

if typing.TYPE_CHECKING:
    from .state import ConnectionState

__all__ = ("CodinGamer",)


class CodinGamer(BaseUser):
    """Represents a CodinGamer.

    Attributes
    -----------
        public_handle: :class:`str`
            Public handle of the CodinGamer (hexadecimal str).

        id: :class:`int`
            ID of the CodinGamer. Last 7 digits of the :attr:`public_handle`
            reversed.

        rank: :class:`int`
            Worldwide rank of the CodinGamer.

        level: :class:`int`
            Level of the CodinGamer.

        xp: :class:`int`
            XP points of the CodinGamer.

        country_id: :class:`str`
            Country ID of the CodinGamer.

        category: Optional :class:`str`
            Category of the CodinGamer. Can be ``STUDENT`` or ``PROFESSIONAL``.

            .. note::
                You can use :attr:`student` and :attr:`professional` to get a
                :class:`bool` that describes the CodinGamer's category.

        student: :class:`bool`
            Whether the CodinGamer is a student.

        professional: :class:`bool`
            Whether the CodinGamer is a professional.

        pseudo: Optional :class:`str`
            Pseudo of the CodinGamer.

        tagline: Optional :class:`str`
            Tagline of the CodinGamer.

        biography: Optional :class:`str`
            Biography of the CodinGamer.

        company: Optional :class:`str`
            Company of the CodinGamer.

        school: Optional :class:`str`
            School of the CodinGamer.

        avatar: Optional :class:`int`
            Avatar ID of the CodinGamer.
            You can get the avatar url with :attr:`avatar_url`.

        cover: Optional :class:`int`
            Cover ID of the CodinGamer.
            You can get the cover url with :attr:`cover_url`.
    """

    public_handle: str
    id: int
    pseudo: typing.Optional[str]
    rank: int
    level: int
    xp: int
    country_id: typing.Optional[str]
    category: typing.Optional[str]
    student: bool
    professional: bool
    tagline: typing.Optional[str]
    biography: typing.Optional[str]
    company: typing.Optional[str]
    school: typing.Optional[str]
    avatar: typing.Optional[int]
    cover: typing.Optional[int]
    avatar_url: typing.Optional[str]
    cover_url: typing.Optional[str]

    __slots__ = (
        "rank",
        "level",
        "xp",
        "country_id",
        "category",
        "student",
        "professional",
        "tagline",
        "biography",
        "company",
        "school",
    )

    def __init__(self, state: "ConnectionState", data: dict):
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

        self.xp = data.get("xp")
        self.rank = data.get("rank")

        # account for empty strings and replace them by None
        self.pseudo = data.get("pseudo") or None
        self.tagline = data.get("tagline") or None
        self.biography = data.get("biography") or None
        self.company = (
            data.get("company")
            or data.get("companyField")
            or data.get("formValues", {}).get("company")
            or None
        )
        self.school = (
            data.get("school")
            or data.get("schoolField")
            or data.get("formValues", {}).get("school")
            or None
        )

        self.avatar = data.get("avatar")
        self.cover = data.get("cover")

        super().__init__(state)

    @property
    def profile_url(self) -> str:
        """:class:`str`: The URL of the CodinGamer profile."""
        return f"https://www.codingame.com/profile/{self.public_handle}"

    def get_followers(
        self,
    ) -> typing.Union[
        typing.Iterator["CodinGamer"], typing.AsyncIterator["CodinGamer"]
    ]:
        """|maybe_coro|

        Get all the followers of a CodinGamer.

        You need to be logged in as the CodinGamer to get its followers
        or else a :exc:`LoginRequired` will be raised. If you can't log in,
        you can use :meth:`CodinGamer.get_followers_ids` instead.

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
            not self._state.logged_in
            or self.public_handle != self._state.codingamer.public_handle
        ):
            raise LoginRequired()

        if self._state.is_async:

            async def _get_followers():
                followers = await self._state.http.get_codingamer_followers(
                    self.id
                )
                for follower in followers:
                    yield CodinGamer(self._state, follower)

        else:

            def _get_followers():
                followers = self._state.http.get_codingamer_followers(self.id)
                for follower in followers:
                    yield CodinGamer(self._state, follower)

        return _get_followers()

    def get_followers_ids(
        self,
    ) -> typing.Union[typing.List[int], typing.Awaitable[typing.List[int]]]:
        """|maybe_coro|

        Get all the IDs of the followers of a CodinGamer.

        Returns
        -------
            :class:`list`
                The CodinGamer's followers IDs. See :attr:`CodinGamer.id`.
        """

        return self._state.http.get_codingamer_follower_ids(self.id)

    def get_followed(
        self,
    ) -> typing.Union[
        typing.Iterator["CodinGamer"], typing.AsyncIterator["CodinGamer"]
    ]:
        """|maybe_coro|

        Get all the followed CodinGamers.

        You need to be logged in as the CodinGamer to get its followed
        CodinGamers or else a :exc:`LoginRequired` will be raised. If you can't
        log in, you can use :meth:`CodinGamer.get_followed_ids` instead.

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
            not self._state.logged_in
            or self.public_handle != self._state.codingamer.public_handle
        ):
            raise LoginRequired()

        if self._state.is_async:

            async def _get_followed():
                followeds = await self._state.http.get_codingamer_following(
                    self.id
                )
                for followed in followeds:
                    yield CodinGamer(self._state, followed)

        else:

            def _get_followed():
                followeds = self._state.http.get_codingamer_following(self.id)
                for followed in followeds:
                    yield CodinGamer(self._state, followed)

        return _get_followed()

    def get_followed_ids(
        self,
    ) -> typing.Union[typing.List[int], typing.Awaitable[typing.List[int]]]:
        """|maybe_coro|

        Get all the IDs of the followed CodinGamers.

        Returns
        -------
            :class:`list`
                The IDs of the followed CodinGamers. See :attr:`CodinGamer.id`.
        """

        return self._state.http.get_codingamer_following_ids(self.id)

    def get_clash_of_code_rank(
        self,
    ) -> typing.Union[int, typing.Awaitable[int]]:
        """|maybe_coro|

        Get the Clash of Code rank of the CodinGamer.

        Returns
        -------
            :class:`int`
                The Clash of Code rank of the CodinGamer.
        """

        if self._state.is_async:

            async def _get_clash_of_code_rank() -> int:
                data = await self._state.http.get_codingamer_clash_of_code_rank(
                    self.id
                )
                return data["rank"]

        else:

            def _get_clash_of_code_rank() -> int:
                data = self._state.http.get_codingamer_clash_of_code_rank(
                    self.id
                )
                return data["rank"]

        return _get_clash_of_code_rank()
