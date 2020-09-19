from typing import List, Optional

from .abc import BaseUser
from .endpoints import Endpoints


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
            Avatar ID of the CodinGamer, if set else `None`. You can get the avatar url with :attr:`avatar_url`.

        cover: Optional[:class:`int`]
            Cover ID of the CodinGamer, if set else `None`. You can get the cover url with :attr:`cover_url`.

        avatar_url: Optional[:class:`str`]
            Avatar URL of the CodinGamer, if set else `None`.

        cover_url: Optional[:class:`str`]
            Cover URL of the CodinGamer, if set else `None`.
    """

    public_handle: str
    id: int
    rank: int
    level: int
    country_id: str
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
        self.rank = data["rank"]
        self.level = data["level"]
        self.country_id = data["countryId"]

        self.category = data["category"] if data.get("category", "UNKNOWN") != "UNKNOWN" else None
        self.student = self.category == "STUDENT"
        self.professional = self.category == "PROFESSIONAL"

        self.pseudo = data.get("pseudo", None) or None
        self.tagline = data.get("tagline", None) or None
        self.biography = data.get("biography", None) or None
        self.company = data.get("company", None) or data.get("companyField", None) or None
        self.school = data.get("schoolField", None) or data.get("formValues", {}).get("school", None) or None

        self.avatar = data.get("avatar", None)
        self.cover = data.get("cover", None)

    @property
    def followers(self):
        r = self._client._session.post(Endpoints.CodinGamer_followers, json=[self.id, self.id, None])
        for follower in r.json():
            yield CodinGamer(client=self._client, **follower)

    @property
    def following(self):
        r = self._client._session.post(Endpoints.CodinGamer_following, json=[self.id, self.id])
        for followed in r.json():
            yield CodinGamer(client=self._client, **followed)

    def __repr__(self):
        return "<CodinGamer public_handle={0.public_handle!r} id={0.id!r}>".format(self)
