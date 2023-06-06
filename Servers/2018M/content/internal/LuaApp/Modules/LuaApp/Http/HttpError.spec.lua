return function()
	local HttpError = require(script.Parent.HttpError)

	describe("new", function()
		it("should construct without a problem", function()
			local err = HttpError.new("testUrl", HttpError.Kind.Unknown, "testMessage")
			expect(err).to.be.ok()
		end)

		it("should just pass data through", function()
			local testUrl = "testUrl"
			local testErrKind = HttpError.Kind.RequestFailure
			local testMessage = "test"

			local err = HttpError.new("testUrl", testErrKind, testMessage)

			expect(err.targetUrl).to.equal(testUrl)
			expect(err.kind).to.equal(testErrKind)
			expect(err.message).to.equal(testMessage)
		end)

		it("should validate its inputs", function()
			local validUrl = "test"
			local validKind = HttpError.Kind.Unknown
			local validMsg = "test"

			local function createHttpError(url, kind, msg)
				-- helper function for checking if the constructor throws errors
				return function()
					HttpError.new(url, kind, msg)
				end
			end

			expect(createHttpError(validUrl, validKind, validMsg)).to.be.ok()

			-- invalid Url values
			expect(createHttpError(nil, validKind, validMsg)).to.throw()
			expect(createHttpError(1, validKind, validMsg)).to.throw()
			expect(createHttpError(true, validKind, validMsg)).to.throw()
			expect(createHttpError({}, validKind, validMsg)).to.throw()
			expect(createHttpError(function() end, validKind, validMsg)).to.throw()

			-- invalid Kind values
			expect(createHttpError(validUrl, nil, validMsg)).to.throw()
			expect(createHttpError(validUrl, 1, validMsg)).to.throw()
			expect(createHttpError(validUrl, true, validMsg)).to.throw()
			expect(createHttpError(validUrl, {}, validMsg)).to.throw()
			expect(createHttpError(validUrl, function() end, validMsg)).to.throw()

			-- invalid Message values
			expect(createHttpError(validUrl, validKind, nil)).to.throw()
			expect(createHttpError(validUrl, validKind, 1)).to.throw()
			expect(createHttpError(validUrl, validKind, true)).to.throw()
			expect(createHttpError(validUrl, validKind, {})).to.throw()
			expect(createHttpError(validUrl, validKind, function() end)).to.throw()
		end)
	end)

	describe("Kind", function()
		it("should return a table", function()
			expect(type(HttpError.Kind)).to.equal("table")
		end)
	end)
end