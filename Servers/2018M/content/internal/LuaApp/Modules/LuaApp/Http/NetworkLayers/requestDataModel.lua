--[[
	Abstracts out the networking logic to provide a unified interface for request.lua.
	Exposes a single function to return a promise object with an HttpResponse.

	This implementation utilizes the networking functions on the DataModel.
]]
local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Promise = require(Modules.LuaApp.Promise)
local HttpError = require(Modules.LuaApp.Http.HttpError)
local HttpResponse = require(Modules.LuaApp.Http.HttpResponse)
local StatusCodes = require(Modules.LuaApp.Http.StatusCodes)


-- url : (string)
-- requestMethod : (string)
-- args : (table)
-- RETURNS : (HttpResponse)
local function makeRequest(url, httpFunc, args)
	-- this function handles the actual network request and any and all additional
	-- business logic around the request.

	-- fetch the raw response from the server and time how long it takes
	-- this pcall will prevent the server from throwing errors on a 404 or other server problem
	local startTime = tick()
	local success, responseString = pcall(httpFunc, unpack(args))
	local endTime = tick()

	-- package information about the response into a single object
	local responseTimeMs = (endTime - startTime) * 1000
	local statusCode
	if success then
		statusCode = StatusCodes.OK
	else
		statusCode = StatusCodes.UNKNOWN_ERROR
		-- The expected failure response should look like this :
		-- HTTP 404 (HTTP/1.1 404 Not Found)
		-- HTTP 500 (HTTP/1.1 500 Internal Server Error)

		-- capture all the text within the parentheses
		local parenText = string.match(responseString, ".*%((.*)%)")
		if parenText then
			local codeIndex = string.find(parenText, "%d%d%d")
			if codeIndex then
				-- capture the error code and the error message
				statusCode = tonumber(string.sub(parenText, codeIndex, codeIndex + 2))
				responseString = string.sub(parenText, codeIndex + 4)
			end
		end
	end

	return HttpResponse.new(url, responseString, responseTimeMs, statusCode)
end

-- httpResponse : (HttpResponse)
-- RETURNS : (HttpError)
local function getErrorFromResponse(httpResponse)
	local errorKind = HttpError.Kind.Unknown
	local message = httpResponse.responseBody

	if httpResponse.responseCode ~= StatusCodes.UNKNOWN_ERROR then
		local code = httpResponse.responseCode
		if code >= 500 then
			-- there was a server error, flag this request for retry
			errorKind = HttpError.Kind.RequireExternalRetry
		else
			-- the request simply failed for some reason or another, return the code so someone else can handle the error
			errorKind = HttpError.Kind.RequestFailure
			message = tostring(code)
		end
	end

	return HttpError.new(httpResponse.requestUrl, errorKind, message)
end

-- requestService : (table, optional) an object that implements the same http functions as the data model
return function(requestService)
	-- for tests, allow the object that makes the request to be mocked
	if not requestService then
		requestService = game
	end

	-- url : (string)
	-- requestMethod : (string) "GET", "POST", "PUT", etc.
	-- args : (table, optional)
	--     options.contentType : (Enum.HttpContentType, optional)
	--     options.postBody : (string, optional ("POST" only))
	-- RETURNS : (promise<HttpResponse or HttpError>)
	return function(url, requestMethod, options)
		assert(type(url) == "string", "Expected url to be a string")
		assert(type(requestMethod) == "string", "Expected requestMethod to be a string")
		requestMethod = string.upper(requestMethod)
		if options then
			assert(type(options) == "table", "Expected extra args to be a table")
		end
		if requestMethod == "POST" then
			assert(options.postBody, "Expected a postBody to be specified with this request")
			if not options.contentType then
				options.contentType = "application/json"
			end
		end

		-- assemble the arguments to make the request
		local httpFunc
		local httpFuncArgs
		if requestMethod == "GET" then
			httpFunc = requestService.HttpGetAsync
			httpFuncArgs = { requestService, url }

		elseif requestMethod == "POST" then
			httpFunc = requestService.HttpPostAsync
			httpFuncArgs = { requestService, url, options.postBody, options.contentType }

		else
			error(string.format("Unsupported requestMethod : %s", requestMethod or "nil"))
		end

		local httpPromise = Promise.new(function(resolve, reject)
			spawn(function()
				local httpResponse = makeRequest(url, httpFunc, httpFuncArgs)
				if httpResponse.responseCode == StatusCodes.OK then
					resolve(httpResponse)
				else
					local httpError = getErrorFromResponse(httpResponse)
					reject(httpError)
				end
			end)
		end)

		return httpPromise
	end
end