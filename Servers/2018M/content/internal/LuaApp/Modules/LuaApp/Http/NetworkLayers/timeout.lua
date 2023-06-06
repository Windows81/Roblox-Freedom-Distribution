--[[
	Times out a request if it has not resolved within the expected time limit
]]

local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Promise = require(Modules.LuaApp.Promise)
local HttpError = require(Modules.LuaApp.Http.HttpError)

-- requestFunc - (function<promise<HttpResponse>>(url, requestMethod, options))
-- timeout - (number, optional) number of seconds before the request should fail
return function(requestFunc, timeout)
	assert(type(requestFunc) == "function", "Expected requestFunc to be a function")

	local expectedTimeout = 30
	if timeout then
		assert(type(timeout) == "number", "Expected timout to be a number")
		assert(timeout > 0, "Expected timeout to be greater than or equal to 0")
		expectedTimeout = timeout
	end

	return function(url, requestMethod, options)
		-- make the request
		local httpPromise = requestFunc(url, requestMethod, options)

		-- wrap the callbacks that in a promise that will fail if the request takes too long

		-- Should the network request succeed after the lua imposed timeout,
		--  the promise will not call the resolve callback.
		--  Once a promise is resolved or rejected, it stays that way.
		-- The inverse is true as well, if the promise is resolved or rejected before the delay completes,
		--  the promise will not call the timeout rejection callback.
		local timeoutPromise = Promise.new(function(resolve, reject)
			-- succeed if the promise succeeds, pass the results through.
			httpPromise:andThen(resolve, reject)

			-- escape if the promise has not resolved within the expected timeout
			delay(expectedTimeout, function()
				local errMsg = string.format("Lua Timeout of %s seconds reached.", tostring(expectedTimeout))
				reject(HttpError.new(url, HttpError.Kind.LuaTimeout, errMsg))
			end)
		end)

		return timeoutPromise
	end
end