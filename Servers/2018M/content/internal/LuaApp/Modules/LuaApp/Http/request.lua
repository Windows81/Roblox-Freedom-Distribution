--[[
	Provides a configured networking stack to store in the ServiceProvider
]]--
local Modules = game:GetService("CoreGui").RobloxGui.Modules

local json = require(Modules.LuaApp.Http.NetworkLayers.json)
local requestDataModel = require(Modules.LuaApp.Http.NetworkLayers.requestDataModel)
local retry = require(Modules.LuaApp.Http.NetworkLayers.retry)
local timeout = require(Modules.LuaApp.Http.NetworkLayers.timeout)

-- construct the networking stack
local request = requestDataModel()
request = timeout(request) -- the timeout default configuration is fine
request = retry(request) -- the retry default configuration is fine
request = json(request)

-- RETURNS : function<promise<HttpResponse>>(url, requestMethod, args)
return request