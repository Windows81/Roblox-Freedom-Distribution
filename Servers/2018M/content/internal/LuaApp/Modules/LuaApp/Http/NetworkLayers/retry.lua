--[[
	Implements exponential backoff HTTP request retry.
]]
local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Promise = require(Modules.LuaApp.Promise)
local HttpError = require(Modules.LuaApp.Http.HttpError)


-- seconds : (number) the number of seconds to wait before resuming
local function defer(seconds)
	return Promise.new(function(resolve)
		delay(seconds, function()
			resolve()
		end)
	end)
end

-- httpFunc : (function<promise<HttpResponse>>()) a function that fires a network request until it succeeds
-- options : (table) retry configuration parameters
--	options.remainingAttempts : (number) a counter for determining when we've failed
--	options.maxAttempts : (number) a value to let us know how many attempts we started with
--	options.backoffRate : (number)
--	options.shouldRetryFunc : (function<bool>(HttpError)) custom logic
--	options.shouldImmediateRetry : (bool, TESTING ONLY) when true, disregards backoff rate
local function retryRequest(httpFunc, options)
	return httpFunc():catch(function(httpError)
		options.remainingAttempts = options.remainingAttempts - 1

		-- decide whether to retry
		local shouldRetry = options.remainingAttempts > 0 and
			(httpError.kind == HttpError.Kind.RequireExternalRetry or
			httpError.kind == HttpError.Kind.LuaTimeout)

		if not shouldRetry then
			return Promise.reject(httpError)
		end

		if options.shouldImmediateRetry then
			-- In tests, resolve the retry logic immediately.
			-- This functionality should one day be replaced with a service that mocks the passage of time,
			--  that way, tests will be able to resolve synchronously.
			return retryRequest(httpFunc, options)
		else
			-- wait for an increasing amount of time before retrying
			local nextDelay = options.backoffRate ^ (options.maxAttempts - options.remainingAttempts)
			return defer(nextDelay):andThen(function()
				return retryRequest(httpFunc, options)
			end)
		end
	end)
end

-- requestFunc : (function<promise<HttpResponse>>(url, requestMethod, options))
-- options : (table, optional)
--	shouldImmediateRetry : (bool) when true, disregards backoff rate
return function(requestFunc, options)

	-- default retry delays are 2, 4, 8 seconds
	local retryConfigParams = {
		maxAttempts = 3,
		backoffRate = 2,
		shouldImmediateRetry = false
	}

	if options then
		if options.shouldImmediateRetry then
			assert(type(options.shouldImmediateRetry) == "boolean", "shouldImmediateRetry must be a bool")
			retryConfigParams.shouldImmediateRetry = options.shouldImmediateRetry
		end
	end

	retryConfigParams.remainingAttempts = retryConfigParams.maxAttempts

	return function(url, requestMethod, options)
		-- wrap the request into a function that can be called multiple times until we succeed
		local function makeRequest()
			return requestFunc(url, requestMethod, options)
		end

		local httpPromise = retryRequest(makeRequest, retryConfigParams)
		return httpPromise
	end
end