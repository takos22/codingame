class CodinGamer:
    """Represents a CodinGamer.

    Do not create this class yourself. Only get it through :meth:`Client.codingamer()`.

    Attributes
    ----------
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
            You can use :attr:`student` and :attr:`professional` to get a :class:`bool` that describes the CodinGamer's category.

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

    def __init__(self, **kwargs):
        self.public_handle: str = kwargs["publicHandle"]
        self.id: int = kwargs["userId"]
        self.rank: int = kwargs["rank"]
        self.level: int = kwargs["level"]
        self.country_id: str = kwargs["countryId"]

        self.category: str or None = kwargs["category"] if kwargs["category"] != "UNKNOWN" else None
        self.student: bool = self.category == "STUDENT"
        self.professional: bool = self.category == "PROFESSIONAL"

        self.pseudo: str or None = kwargs.get("pseudo", None) or None
        self.tagline: str or None = kwargs.get("tagline", None) or None
        self.biography: str or None = kwargs.get("biography", None) or None
        self.company: str or None = kwargs.get("company", None) or None
        self.school: str or None = kwargs["formValues"].get("school", None) or None

        self.avatar: int or None = kwargs.get("avatar", None)
        self.cover: int or None = kwargs.get("cover", None)

        self.avatar_url: str or None = f"https://static.codingame.com/servlet/fileservlet?id={self.avatar}" if self.avatar else None
        self.cover_url: str or None = f"https://static.codingame.com/servlet/fileservlet?id={self.cover}" if self.cover else None

    def __repr__(self):
        return "<CodinGamer public_handle={0.public_handle!r} user_id={0.user_id!r}>".format(self)
