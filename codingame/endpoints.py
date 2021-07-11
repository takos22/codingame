__all__ = ("Endpoints",)


class Endpoints:
    """Class for storing the CodinGame API endpoints."""

    BASE = "https://www.codingame.com/services/"

    image = "https://static.codingame.com/servlet/fileservlet?id={}"

    # general stuff
    login = BASE + "CodinGamer/loginSiteV2"
    language_ids = BASE + "ProgrammingLanguage/findAllIds"
    unseen_notifications = BASE + "Notification/findUnseenNotifications"
    search = BASE + "search/search"

    # CodinGamer
    codingamer_from_id = BASE + "CodinGamer/findCodinGamerPublicInformations"
    codingamer_from_handle = (
        BASE + "CodinGamer/findCodingamePointsStatsByHandle"
    )
    codingamer_followers = BASE + "CodinGamer/findFollowers"
    codingamer_followers_ids = BASE + "CodinGamer/findFollowerIds"
    codingamer_following = BASE + "CodinGamer/findFollowing"
    codingamer_following_ids = BASE + "CodinGamer/findFollowingIds"
    codingamer_clash_of_code_rank = (
        BASE + "ClashOfCode/getClashRankByCodinGamerId"
    )

    # Clash of Code
    clash_of_code = BASE + "ClashOfCode/findClashByHandle"
    clash_of_code_pending = BASE + "ClashOfCode/findPendingClashes"
    clash_of_code_solution = BASE + "Solution/findSolution"

    # Leaderboards
    global_leaderboard = BASE + "Leaderboards/getGlobalLeaderboard"
    challenge_leaderboard = (
        BASE + "Leaderboards/getFilteredChallengeLeaderboard"
    )
    puzzle_leaderboard = BASE + "Leaderboards/getFilteredPuzzleLeaderboard"
