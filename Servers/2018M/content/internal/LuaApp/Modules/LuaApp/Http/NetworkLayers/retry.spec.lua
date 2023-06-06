
return function()
	local retry = require(script.Parent.retry)

	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local HttpError = require(Modules.LuaApp.Http.HttpError)
	local HttpResponse = require(Modules.LuaApp.Http.HttpResponse)
	local StatusCodes = require(Modules.LuaApp.Http.StatusCodes)
	local Promise = require(Modules.LuaApp.Promise)

	it("should retry when the request fails up to the maximum", function()
		local numberOfRequests = 0
		local matchesErrorKind = false
		local matchesRetryCount = false

		local maxAttempts = 3
		local testErrKind = HttpError.Kind.RequireExternalRetry

		local request = function(url, requestMethod, options)
			numberOfRequests = numberOfRequests + 1
			return Promise.reject(HttpError.new(url, testErrKind, "retry.spec - retry maximum test"))
		end
		request = retry(request, {
			shouldImmediateRetry = true,
		})

		local httpPromise = request("fakeUrl", "GET")
		httpPromise:catch(function(httpError)
			matchesErrorKind = httpError.kind == testErrKind
			matchesRetryCount = numberOfRequests == maxAttempts
		end)

		expect(matchesErrorKind).to.equal(true)
		expect(matchesRetryCount).to.equal(true)
	end)

	it("should not retry if the request succeeds", function()
		local numberOfRequests = 0
		local requestCountCorrect = false

		local request = function(url, requestMethod, options)
			numberOfRequests = numberOfRequests + 1
			return Promise.resolve(HttpResponse.new(url, "retry.spec - successful request test", 0, StatusCodes.OK))
		end
		request = retry(request, {
			shouldImmediateRetry = true,
		})

		local httpPromise = request("fakeUrl", "GET")
		httpPromise:andThen(function(httpResponse)
			requestCountCorrect = numberOfRequests == 1
		end)

		expect(requestCountCorrect).to.equal(true)
	end)

	it("should not retry when an error isn't flagged for retry", function()
		-- make a helper function for testing a bunch of different errors
		local function testRetryLogicWithError(errKind)
			local numberOfRequests = 0
			local matchesErrorKind = false
			local requestCountCorrect = false

			local request = function(url, requestMethod, options)
				numberOfRequests = numberOfRequests + 1
				return Promise.reject(HttpError.new(url, errKind, "retry.spec - bad request test"))
			end
			request = retry(request, {
				shouldImmediateRetry = true,
			})

			local httpPromise = request("fakeUrl", "GET")
			httpPromise:catch(function(httpError)
				matchesErrorKind = httpError.kind == errKind
				requestCountCorrect = numberOfRequests == 1
			end)

			-- return these expectations to the caller
			return matchesErrorKind and requestCountCorrect
		end

		-- test different errors here...
		expect( testRetryLogicWithError(HttpError.Kind.RequestFailure) ).to.equal(true)
		expect( testRetryLogicWithError(HttpError.Kind.Unknown) ).to.equal(true)

		-- these should succeed ...
		expect( testRetryLogicWithError(HttpError.Kind.LuaTimeout) ).to.equal(false)
		expect( testRetryLogicWithError(HttpError.Kind.RequireExternalRetry) ).to.equal(false)
	end)
end