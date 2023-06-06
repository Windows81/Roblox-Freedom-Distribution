--[[
	Encapsulates the response from an http request. Nothing fancy
]]


local HttpResponse = {}
HttpResponse.__index = HttpResponse

function HttpResponse.new(url, response, responseTime, statusCode)
	assert(type(url) == "string", "Expected url to be a string")
	assert(type(response) == "string" or type(response) == "table" , "Expected response to be a string or table")
	assert(type(responseTime) == "number", "Expected responseTimeMs to be a number")
	assert(type(statusCode) == "number", "Expected statusCode to be a number")

	local responseObj = {
		requestUrl = url,
		responseTimeMs = responseTime,
		responseCode = statusCode,
		responseBody = response
	}
	setmetatable(responseObj, HttpResponse)

	return responseObj
end

function HttpResponse:__tostring()
	return table.concat({
		"HttpResponse :",
		string.format("\tRequested Url - %s", self.requestUrl),
		string.format("\tCode - %s", tostring(self.responseCode)),
		string.format("\tBody - %s", tostring(self.responseBody)),
		string.format("\tTime(ms) - %s", tostring(self.responseTimeMs))
	}, "\n")
end

return HttpResponse