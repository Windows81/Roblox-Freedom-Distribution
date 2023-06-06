return function()
	local MockRequest = require(script.Parent.MockRequest)

	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local HttpError = require(Modules.LuaApp.Http.HttpError)

	describe("simpleSuccessRequest", function()
		it("should return a function", function()
			local request = MockRequest.simpleSuccessRequest("this is a test")

			expect(type(request)).to.equal("function")
		end)

		it("should return the provided response as the resolution to a promise", function()
			local testBodyMatches = false

			local testBody = "this is a test"
			local request = MockRequest.simpleSuccessRequest(testBody)

			local httpPromise = request("testUrl", "GET")
			httpPromise:andThen(function(httpResponse)
				testBodyMatches = httpResponse.responseBody == testBody
			end)
			expect(testBodyMatches).to.equal(true)
		end)
	end)


	describe("simpleFailRequest", function()
		it("should return a function", function()
			local request = MockRequest.simpleFailRequest(HttpError.Kind.Unknown)

			expect(type(request)).to.equal("function")
		end)

		it("should return the provided error code as the rejection to a promise", function()
			local testErrMatches = false

			local testErrKind = HttpError.Kind.Unknown
			local request = MockRequest.simpleFailRequest(testErrKind)

			local httpPromise = request("testUrl", "GET")
			httpPromise:catch(function(httpError)
				testErrMatches = httpError.kind == testErrKind
			end)

			expect(testErrMatches).to.equal(true)
		end)
	end)
end