return function()
	local json = require(script.Parent.json)

	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local HttpError = require(Modules.LuaApp.Http.HttpError)
	local MockRequest = require(Modules.LuaApp.TestHelpers.MockRequest)

	it("should return an HttpResponse object with a parsed table", function()
		local testBody = [[{ "foo": 123, "bar": "hello world" }]]
		local request = MockRequest.simpleSuccessRequest(testBody)
		request = json(request)

		local matchesType = false
		local matchesValueFoo = false
		local matchesValueBar = false

		local httpPromise = request("fakeUrl", "GET")
		httpPromise:andThen(function(result)
			matchesType = type(result.responseBody) == "table"
			matchesValueFoo = result.responseBody.foo == 123
			matchesValueBar = result.responseBody.bar == "hello world"
		end)

		expect(matchesType).to.equal(true)
		expect(matchesValueFoo).to.equal(true)
		expect(matchesValueBar).to.equal(true)
	end)

	it("should return an HttpError when invalid json is returned", function()
		local testBody = "this isn't json"
		local request = MockRequest.simpleSuccessRequest(testBody)
		request = json(request)

		local matchesKind = false

		local httpPromise = request("fakeUrl", "GET")
		httpPromise:catch(function(httpError)
			matchesKind = httpError.kind == HttpError.Kind.InvalidJson
		end)

		expect(matchesKind).to.equal(true)
	end)

	it("should pass errors through from a lower level", function()
		local testErrKind = HttpError.Kind.RequireExternalRetry
		local request = MockRequest.simpleFailRequest(testErrKind)
		request = json(request)

		local matchesKind = false

		local httpPromise = request("fakeUrl", "GET")
		httpPromise:catch(function(httpError)
			matchesKind = httpError.kind == testErrKind
		end)

		expect(matchesKind).to.equal(true)
	end)
end