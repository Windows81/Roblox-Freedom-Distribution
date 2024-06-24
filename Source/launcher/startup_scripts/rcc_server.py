import data_transfer
import config

BASE_SCRIPT_FORMAT = """
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
"""


def get_script(game_config: config.obj_type) -> str:
    return '\n\n'.join([
        data_transfer.get_rcc_snippet(game_config),

        BASE_SCRIPT_FORMAT % {
        },

        game_config.game_setup.startup_script,
        "print('Initialised RFD server scripts.')",
    ])
