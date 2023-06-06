return function()
	local request = require(script.Parent.requestDataModel)

	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local HttpError = require(Modules.LuaApp.Http.HttpError)
	local StatusCodes = require(Modules.LuaApp.Http.StatusCodes)

	local function createTestRequestFunc(testResponse)
		local requestService = {}
		function requestService:HttpGetAsync()
			return testResponse
		end
		function requestService:HttpPostAsync()
			return testResponse
		end

		return request(requestService)
	end

	it("should return a function", function()
		expect(request()).to.be.ok()
		expect(type(request())).to.equal("function")
	end)

	it("should validate its inputs", function()
		local testRequest = createTestRequestFunc()
		local function testParams(url, requestMethod, args)
			return function()
				testRequest(url, requestMethod, args)
			end
		end

		local validUrl = "testUrl"
		local validMethod = "GET"
		local validArgs = {}

		-- url checks
		expect(testParams(nil, validMethod, validArgs)).to.throw()
		expect(testParams(123, validMethod, validArgs)).to.throw()
		expect(testParams({}, validMethod, validArgs)).to.throw()
		expect(testParams(true, validMethod, validArgs)).to.throw()
		expect(testParams(function() end, validMethod, validArgs)).to.throw()

		-- request method checks
		expect(testParams(validUrl, nil, validArgs)).to.throw()
		expect(testParams(validUrl, 123, validArgs)).to.throw()
		expect(testParams(validUrl, {}, validArgs)).to.throw()
		expect(testParams(validUrl, true, validArgs)).to.throw()
		expect(testParams(validUrl, function() end, validArgs)).to.throw()

		-- args checks
		expect(testParams(validUrl, validMethod, 123)).to.throw()
		expect(testParams(validUrl, validMethod, "Test")).to.throw()
		expect(testParams(validUrl, validMethod, true)).to.throw()
		expect(testParams(validUrl, validMethod, function() end)).to.throw()
	end)

	it("should throw an error if the requestMethod isn't supported", function()
		local testRequest = createTestRequestFunc("foo")

		expect(function()
			testRequest("testUrl", "GIVEANDTAKE")
		end).to.throw()
	end)

	describe("the request interface", function()
		-- request yields when it attempts the request
		HACK_NO_XPCALL()

		it("should return a promise that resolves to an HttpResponse", function()
			local responseUpval

			local testRequest = createTestRequestFunc("foo")
			local httpPromise = testRequest("testUrl", "GET")
			httpPromise:andThen(function(response)
				responseUpval = response
			end)

			wait()

			expect(responseUpval.requestUrl).to.equal("testUrl")
			expect(responseUpval.responseBody).to.equal("foo")
			expect(responseUpval.responseCode).to.equal(StatusCodes.OK)
		end)

		it("should return the error code when a request fails for non-server reasons", function()
			local failingTestService = {}
			function failingTestService:HttpGetAsync()
				error("HTTP 404 (HTTP/1.1 404 Not Found)")
			end

			local errUpval

			local testRequest = request(failingTestService)
			testRequest("testUrl", "GET"):catch(function(httpError)
				errUpval = httpError
			end)

			wait()

			expect(errUpval.kind).to.equal(HttpError.Kind.RequestFailure)
			expect(errUpval.message).to.equal("404")
		end)

		it("should parse out an http error message when a request fails", function()
			local failingTestService = {}
			function failingTestService:HttpGetAsync()
				error("HTTP 500 (HTTP/1.1 500 Internal Server Error)")
			end

			local errUpval

			local testRequest = request(failingTestService)
			testRequest("testUrl", "GET"):catch(function(httpError)
				errUpval = httpError
			end)

			wait()

			expect(errUpval.kind).to.equal(HttpError.Kind.RequireExternalRetry)
			expect(errUpval.message).to.equal("Internal Server Error")
		end)

		it("should return an unknown error when the error is bonkers", function()
			local failingTestService = {}
			function failingTestService:HttpGetAsync()
				error("BAD_TLS")
			end

			local errUpval

			local testRequest = request(failingTestService)
			testRequest("testUrl", "GET"):catch(function(httpError)
				errUpval = httpError
			end)

			wait()

			expect(errUpval.kind).to.equal(HttpError.Kind.Unknown)
			expect(string.find(errUpval.message, "BAD_TLS") > 0).to.equal(true)
		end)
	end)
end