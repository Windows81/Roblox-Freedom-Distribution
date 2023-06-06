return function()
	local HttpResponse = require(script.Parent.HttpResponse)
	local StatusCodes = require(script.Parent.StatusCodes)

	describe("new", function()
		it("should construct without a problem", function()
			local hr = HttpResponse.new("testUrl", "testBody", 0, StatusCodes.OK)
			expect(hr).to.be.ok()
		end)

		it("should just pass data through", function()
			local testUrl = "testUrl"
			local testBody = "testBody"
			local testTime = 203
			local testCode = StatusCodes.OK

			local response = HttpResponse.new(testUrl, testBody, testTime, testCode)

			expect(response.requestUrl).to.equal(testUrl)
			expect(response.responseBody).to.equal(testBody)
			expect(response.responseTimeMs).to.equal(testTime)
			expect(response.responseCode).to.equal(testCode)
		end)

		it("should validate its inputs", function()
			local validUrl = "test"
			local validBodyString = "test"
			local validBodyTable = {}
			local validTime = 0
			local validCode = StatusCodes.OK


			local function createHttpResponse(url, body, responseTime, status)
				-- helper function for checking if the constructor throws errors
				return function()
					HttpResponse.new(url, body, responseTime, status)
				end
			end

			expect(createHttpResponse(validUrl, validBodyString, validTime, validCode)).to.be.ok()
			expect(createHttpResponse(validUrl, validBodyTable, validTime, validCode)).to.be.ok()

			-- invalid Url values
			expect(createHttpResponse(nil, validBodyString, validTime, validCode)).to.throw()
			expect(createHttpResponse(1, validBodyString, validTime, validCode)).to.throw()
			expect(createHttpResponse(true, validBodyString, validTime, validCode)).to.throw()
			expect(createHttpResponse({}, validBodyString, validTime, validCode)).to.throw()
			expect(createHttpResponse(function() end, validBodyString, validTime, validCode)).to.throw()

			-- invalid ResponseBody values
			expect(createHttpResponse(validUrl, nil, validTime, validCode)).to.throw()
			expect(createHttpResponse(validUrl, 1, validTime, validCode)).to.throw()
			expect(createHttpResponse(validUrl, true, validTime, validCode)).to.throw()
			expect(createHttpResponse(validUrl, function() end, validTime, validCode)).to.throw()

			-- invalid ResponseTime values
			expect(createHttpResponse(validUrl, validBodyString, nil, validCode)).to.throw()
			expect(createHttpResponse(validUrl, validBodyString, "test", validCode)).to.throw()
			expect(createHttpResponse(validUrl, validBodyString, true, validCode)).to.throw()
			expect(createHttpResponse(validUrl, validBodyString, {}, validCode)).to.throw()
			expect(createHttpResponse(validUrl, validBodyString, function() end, validCode)).to.throw()

			-- invalid ResponseCode values
			expect(createHttpResponse(validUrl, validBodyString, validTime, nil)).to.throw()
			expect(createHttpResponse(validUrl, validBodyString, validTime, "test")).to.throw()
			expect(createHttpResponse(validUrl, validBodyString, validTime, true)).to.throw()
			expect(createHttpResponse(validUrl, validBodyString, validTime, {})).to.throw()
			expect(createHttpResponse(validUrl, validBodyString, validTime, function() end)).to.throw()
		end)
	end)
end