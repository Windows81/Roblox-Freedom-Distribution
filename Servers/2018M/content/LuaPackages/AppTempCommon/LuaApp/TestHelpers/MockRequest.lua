--[[
	A hub for faking networking responses for tests
]]

local CorePackages = game:GetService("CorePackages")
local AppTempCommon = CorePackages.AppTempCommon

local Promise = require(AppTempCommon.LuaApp.Promise)
local HttpError = require(AppTempCommon.LuaApp.Http.HttpError)
local HttpResponse = require(AppTempCommon.LuaApp.Http.HttpResponse)
local StatusCodes = require(AppTempCommon.LuaApp.Http.StatusCodes)


local MockRequest = {}

-- responseBody : (string)
function MockRequest.simpleSuccessRequest(responseBody)
	assert(responseBody ~= nil, "Expected responseBody not to be nil")

	-- create a simple network handler that only needs a response body specified
	return function(url, requestMethod, options)
		return Promise.resolve(HttpResponse.new(url, responseBody, 0, StatusCodes.OK))
	end
end

-- errMsg : (HttpError.Kind)
function MockRequest.simpleFailRequest(errKind)
	assert(errKind ~= nil, "Expected errKind not to be nil")

	-- create a simple network handler that only needs an error kind specified
	return function(url, requestMethod, options)
		return Promise.reject(HttpError.new(url, errKind, "Fake request failed"))
	end
end

return MockRequest