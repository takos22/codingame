from enum import Enum

__all__ = (
    "NotificationTypeGroup",
    "NotificationType",
    "ContributionType",
    "CommentType",
    "ContributionModeratedActionType",
)


class NotificationTypeGroup(str, Enum):
    """Enumeration for the :attr:`Notification.type_group`.

    .. warning::
        There might be some missing type groups.
    """

    achievement = "achievement"
    arena = "arena"
    blog = "blog"
    clash = "clash"
    comment = "comment"
    contest = "contest"
    contribution = "contribution"
    feature = "feature"
    hints = "hints"
    moderation = "moderation"
    puzzle = "puzzle"
    quest = "quest"
    social = "social"
    xp = "xp"
    generic = "generic"
    custom = "custom"
    other = "other"


class NotificationType(str, Enum):
    """Enumeration for the :attr:`Notification.type`."""

    # achievement
    achievement_unlocked = "achievement-unlocked"
    """When a new achievement is unlocked."""

    # arena
    new_league = "new-league"
    """When a new league is added to an arena.

    If the new league is higher than your current one, you will get demoted,
    otherwise your league will stay the same."""
    eligible_for_next_league = "eligible-for-next-league"
    """When you are better than the boss of your current league.

    This means you will be promoted soon."""
    promoted_league = "promoted-league"
    """When you are promoted to a higher league."""

    # blog
    new_blog = "new-blog"
    """When a new blog entry is created."""

    # clash
    clash_invite = "clash-invite"
    """When you are invited to a Clash of Code."""
    clash_over = "clash-over"
    """When a Clash of Code you participated in is over."""

    # comment
    new_comment = "new-comment"
    """When someone comments your contribution or your solution."""
    new_comment_response = "new-comment-response"
    """When someone replies to your commeny."""

    # contest
    contest_scheduled = "contest-scheduled"
    """When a contest is scheduled."""
    contest_soon = "contest-soon"
    """When a contest is starting soon."""
    contest_started = "contest-started"
    """When a contest has started."""
    contest_over = "contest-over"
    """When a contest is over."""

    # contribution
    contribution_received = "contribution-received"
    """When your contribution is received."""
    contribution_accepted = "contribution-accepted"
    """When your contribution is accepted."""
    contribution_refused = "contribution-refused"
    """When your contribution is refused."""
    contribution_clash_mode_removed = "contribution-clash-mode-removed"
    """When your contribution is modified."""

    # feature
    feature = "feature"
    """When a new feature is available on CodinGame."""

    # hints
    new_hint = "new-hint"
    """When a new hint is revealed."""

    # moderation
    contribution_moderated = "contribution-moderated"
    """When your contribution is validated or denied."""

    # puzzle
    new_puzzle = "new-puzzle"
    """When a new puzzle is available."""
    puzzle_of_the_week = "puzzle-of-the-week"
    """When the puzzle of the week is available."""
    new_league_opened = "new-league-opened"
    """When a new league is opened.

    I don't know why this isn't in :attr:`NotificationTypeGroup.arena` like
    :attr:`NotificationType.new_league`,
    :attr:`NotificationType.eligible_for_next_league` and
    :attr:`NotificationType.promoted_league`."""

    # quest
    quest_completed = "quest-completed"
    """When a quest is completed."""

    # social
    following = "following"
    """When a CodinGamer starts following you."""
    friend_registered = "friend-registered"
    """When a friend registers on CodinGame."""
    invitation_accepted = "invitation-accepted"
    """When a friend accepts your invitation and registers on CodinGame."""

    # xp
    new_level = "new-level"
    """When you reach a new level."""

    # generic
    info_generic = "info-generic"
    """When you get a generic information notification."""
    warning_generic = "warning-generic"
    """When you get a generic warning notification."""
    important_generic = "important-generic"
    """When you get a generic important notification."""

    # custom
    custom = "custom"
    """When you get a custom notification."""

    # other
    career_new_candidate = "career-new-candidate"
    career_update_candidate = "career-update-candidate"

    # didn't find a category
    test_finished = "test-finished"
    job_accepted = "job-accepted"
    job_expired = "job-expired"
    new_work_blog = "new-work-blog"
    offer_apply = "offer-apply"
    recruiter_contact = "recruiter-contact"


class ContributionType(str, Enum):
    clash_of_code = "CLASHOFCODE"
    puzzle_in_out = "PUZZLE_INOUT"
    puzzle_solo = "PUZZLE_SOLO"
    puzzle_multiplayer = "PUZZLE_MULTI"
    puzzle_optimization = "PUZZLE_OPTI"


class CommentType(str, Enum):
    contribution = "CONTRIBUTION"
    solution = "SOLUTION"


class ContributionModeratedActionType(str, Enum):
    validate = "validate"
    deny = "deny"
