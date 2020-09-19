class Endpoints:
    BASE = "https://www.codingame.com/services/"

    image = "https://static.codingame.com/servlet/fileservlet?id={}"

    # CodinGamer
    CodinGamer = BASE + "CodinGamer/findCodingamePointsStatsByHandle"
    CodinGamer_login = BASE + "CodinGamer/loginSiteV2"
    CodinGamer_followers = BASE + "CodinGamer/findFollowers"
    CodinGamer_following = BASE + "CodinGamer/findFollowing"

    # Clash of Code
    ClashOfCode = BASE + "ClashOfCode/findClashByHandle"
    Solution = BASE + "Solution/findSolution"
