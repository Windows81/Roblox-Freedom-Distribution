local HttpError = {}
HttpError.__index = HttpError

HttpError.Kind = {
	-- A catch-all for all errors we can't otherwise classify
	Unknown = "Unknown",

	-- We could not resolve the request
	RequestFailure = "Request Failed",

	-- We could not resolve the request, but it's a server issue, go ahead and retry
	RequireExternalRetry = "Require External Retry",

	-- We bailed out before we got a response from the server
	LuaTimeout = "Lua Timeout",

	-- We expected JSON in the response body, but it was malformed
	InvalidJson = "Invalid Json",
}

function HttpError.new(targetUrl, errKind, errMessage)
	assert(type(targetUrl) == "string", "Expected targetUrl to be a string")
	assert(type(errKind) == "string", "Expected errKind to be a string")
	assert(type(errMessage) == "string", "Expected errMessage to be a string")

	local err = {
		targetUrl = targetUrl,
		kind = errKind,
		message = errMessage
	}
	setmetatable(err, HttpError)

	return err
end

function HttpError:__tostring()
	return table.concat({
		"HttpError :",
		string.format("\tTarget Url - %s", self.targetUrl),
		string.format("\tKind - %s", self.kind),
		string.format("\tMessage - %s", self.message),
	}, "\n")
end

return HttpError