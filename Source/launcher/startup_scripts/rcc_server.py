import data_transfer
import game_storer
import textwrap

BASE_SCRIPT_FORMAT = """\
%(rcc_snippet)s
local BaseUrl = game:GetService("ContentProvider").BaseUrl:lower()
local HttpRbxApiService = game:GetService("HttpRbxApiService")
local HttpService = game:GetService("HttpService")

spawn(function()
    local Url = BaseUrl .. "rfd/data-transfer"
    local Results = {}
    local Calls = {}

    while true do
    	Calls = HttpRbxApiService:PostAsync(Url, HttpService:JSONEncode(Results))
    	Results = {}
    	for guid, data in next, HttpService:JSONDecode(Calls) do
    		local path, args = data.path, data.args
    		Results[guid] = _G.RFD[path](unpack(args))
            warn(path, unpack(args), Results[guid])
    	end
    end
end)

game.Players.PlayerAdded:connect(function(Player)
    local Url = "rfd/is-player-allowed?userId=" .. Player.UserId
    if HttpRbxApiService:GetAsync(Url) == 'true' then
        return
    end
    Player:Kick('Player is not allowed.')
end)

do
%(startup_script)s
end

print('Initialised RFD server scripts.')
"""


def get_script(game_data: game_storer.obj_type) -> str:
    return BASE_SCRIPT_FORMAT % {
        'rcc_snippet': data_transfer.get_rcc_snippet(game_data),
        'startup_script': game_data.config.server_core.startup_script,
    }
