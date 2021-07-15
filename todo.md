# TODO

## Endpoints found

### Get ranks in every category of a user

Endpoint: `CodinGamer/findRankingPoints`  
JSON: `[user id]`  
Additional info: none  
[Source](https://github.com/tbali0524/codingame_api/blob/6d2bf1a8d10da552304eb1d4bee5cf75771c294b/cg_api.php#L581)

### Get basic info about a challenge

Endpoint: `Challenge/findChallengeMinimalInfoByChallengePublicId`  
JSON: `[challenge public id]`  
Additional info: none  
[Source](https://github.com/tbali0524/codingame_api/blob/6d2bf1a8d10da552304eb1d4bee5cf75771c294b/cg_api.php#L367)

### Get info about a challenge

Endpoint: `Challenge/findWorldCupByPublicId`  
JSON: `[challenge public id, user id/null]`  
Additional info: none  
Source: network tab while searching on codingame

### Get info about all challenges

Endpoint: `Challenge/findAllChallenges`  
JSON: `[]`  
Additional info: some attributes like `finished` are always false  
[Source](https://github.com/tbali0524/codingame_api/blob/6d2bf1a8d10da552304eb1d4bee5cf75771c294b/cg_api.php#L354)

### Get number of done achievments of a user and number of total achievments

Endpoint: `CodinGamer/findTotalAchievementProgress`  
JSON: `[user public handle]`  
Additional info: none  
[Source](https://github.com/tbali0524/codingame_api/blob/6d2bf1a8d10da552304eb1d4bee5cf75771c294b/cg_api.php#L597)

### Get all done challenges and puzzles of a user

Endpoint: `CodinGamer/getMyConsoleInformation`  
JSON: `[user id]`  
Additional info: none  
[Source](https://github.com/tbali0524/codingame_api/blob/6d2bf1a8d10da552304eb1d4bee5cf75771c294b/cg_api.php#L621)

### Get n last activities (challenges, clashes, ...) of a user

Endpoint: `LastActivities/getLastActivities`  
JSON: `[user id, number of activities]`  
Additional info: Login needed  
[Source](https://github.com/tbali0524/codingame_api/blob/6d2bf1a8d10da552304eb1d4bee5cf75771c294b/cg_api.php#L762)

### Get basic information about every puzzle

Endpoint: `Leaderboards/findAllPuzzleLeaderboards`  
JSON: `[]`  
Additional info: none  
[Source](https://github.com/tbali0524/codingame_api/blob/6d2bf1a8d10da552304eb1d4bee5cf75771c294b/cg_api.php#L781)

### Get ranking of a user in a challenge

Endpoint: `Leaderboards/getCodinGamerChallengeRanking`  
JSON: `[user id, challenge public id, "global"]`  
Additional info: none  
[Source](https://github.com/tbali0524/codingame_api/blob/6d2bf1a8d10da552304eb1d4bee5cf75771c294b/cg_api.php#L794)

### Get public clash of code ranking of a user

Endpoint: `Leaderboards/getCodinGamerClashRanking`  
JSON: `[user id, "global", null]`  
Additional info: none  
[Source](https://github.com/tbali0524/codingame_api/blob/6d2bf1a8d10da552304eb1d4bee5cf75771c294b/cg_api.php#L826)

### Get global ranking of a user

Endpoint: `Leaderboards/getCodinGamerGlobalRankingByHandle`  
JSON: `[user public handle, "GENERAL", "global", null]`  
Additional info: none  
[Source](https://github.com/tbali0524/codingame_api/blob/6d2bf1a8d10da552304eb1d4bee5cf75771c294b/cg_api.php#L851)

### Get number of solved puzzles by programming language

Endpoint: `Puzzle/countSolvedPuzzlesByProgrammingLanguage`  
JSON: `[user id]`  
Additional info: Login needed  
[Source](https://github.com/tbali0524/codingame_api/blob/6d2bf1a8d10da552304eb1d4bee5cf75771c294b/cg_api.php#L949)

### Get puzzles info by ids

Endpoint: `Puzzle/findProgressByIds`  
JSON: `[[puzzle ids], user id, language id]`  
Additional info: Language id: 1 for french, 2 for english  
[Source](https://github.com/tbali0524/codingame_api/blob/6d2bf1a8d10da552304eb1d4bee5cf75771c294b/cg_api.php#L984)

### Get puzzle info by pretty id

Endpoint: `Puzzle/findProgressByPrettyId`  
JSON: `[puzzle pretty id, user id]`  
Additional info: Login needed  
[Source](https://github.com/tbali0524/codingame_api/blob/6d2bf1a8d10da552304eb1d4bee5cf75771c294b/cg_api.php#L1003)

### Register

Endpoint: `CodinGamer/registerSite`  
JSON: `[{"email": email, "password": password, "recaptchaResponse": recaptcha}, "CODINGAME", whether to subscribe to the newsletter]`  
Additional info: need recaptcha  
Source: network tab while searching on codingame
