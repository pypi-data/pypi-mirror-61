SHARD_LIST = ["steam", "kakao", "tournament",  "psn", "xbox", "console"]
PLATFORM_REGION = ["pc-as", "pc-eu", "pc-jp", "pc-kakao", "pc-krjp"]
DEFAULT_SHARD = SHARD_LIST[0] # move to client initialization 
# make default shard changeable by a temp file or something similar?
BASE_URL = "https://api.pubg.com/shards/"
DEBUG_URL = "https://api.pubg.com/status"
MATCHES_ROUTE = "matches"
PLAYERNAME_ROUTE = "players?filter[playerNames]="
PLAYERID_ROUTE = "players"
PLAYERIDLIST = "players?filter[playerIds]="
SAMPLE_ROUTE = "samples"
