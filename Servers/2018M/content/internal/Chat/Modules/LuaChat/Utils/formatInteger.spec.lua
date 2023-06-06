return function()
	local formatInteger = require(script.Parent.formatInteger)

	describe("FormatIntegerString", function()
		it("should throw an error if called an a non-number type", function()
			local num = "123"
			expect(function()
				formatInteger(num)
			end).to.throw()
		end)

		it("Should format positive integer whose length less than or equal to sepCount with comma properly", function()
			local num = 123
			local expectedResult = "123"
			expect(formatInteger(num)).to.equal(expectedResult)
		end)
		it("Should format negative integer whose length less than or equal to sepCount with comma properly", function()
			local num = -123
			local expectedResult = "-123"
			expect(formatInteger(num)).to.equal(expectedResult)
		end)
		it("Should format positive integer whose length greater than sepCount with comma properly", function()
			local num = 1234
			local expectedResult = "1,234"
			expect(formatInteger(num)).to.equal(expectedResult)
		end)
		it("Should format negative integer whose length greater than sepCount with comma properly", function()
			local num = -1234
			local expectedResult = "-1,234"
			expect(formatInteger(num)).to.equal(expectedResult)
		end)

		it("Should format positive integer in the form for scientific notation with comma properly", function()
			local num = 4.5e21
			local expectedResult = "4,500,000,000,000,000,000,000"
			expect(formatInteger(num)).to.equal(expectedResult)
		end)
		it("Should format negative integer in the form for scientific notation with comma properly", function()
			local num = -4.5e21
			local expectedResult = "-4,500,000,000,000,000,000,000"
			expect(formatInteger(num)).to.equal(expectedResult)
		end)

		it("Should format positive and negative zero with comma properly ", function()
			local num1 = 0
			local num2 = -0
			local expectedResult = "0"
			expect(formatInteger(num1)).to.equal(expectedResult)
			expect(formatInteger(num2)).to.equal(expectedResult)
		end)

		it("Should format positive integer whose length less than or equal to sepCount with dot properly", function()
			local num = 12
			local expectedResult = "12"
			expect(formatInteger(num, ".", 2)).to.equal(expectedResult)
		end)
		it("Should format negative integer whose length less than or equal to sepCount with dot properly", function()
			local num = -12
			local expectedResult = "-12"
			expect(formatInteger(num, ".", 2)).to.equal(expectedResult)
		end)
		it("Should format positive integer whose length greater than sepCount with dot properly", function()
			local num = 123
			local expectedResult = "1.23"
			expect(formatInteger(num, ".", 2)).to.equal(expectedResult)
		end)
		it("Should format negative integer whose length greater than sepCount with comma properly", function()
			local num = -123
			local expectedResult = "-1.23"
			expect(formatInteger(num, ".", 2)).to.equal(expectedResult)
		end)

		it("Should format positive integer whose length less than or equal to sepCount with dot properly", function()
			local num = 123
			local expectedResult = "123"
			expect(formatInteger(num, ".", 4)).to.equal(expectedResult)
		end)
		it("Should format negative integer whose length less than or equal to sepCount with dot properly", function()
			local num = -123
			local expectedResult = "-123"
			expect(formatInteger(num, ".", 4)).to.equal(expectedResult)
		end)
		it("Should format positive integer whose length greater than sepCount with dot properly", function()
			local num = 12345
			local expectedResult = "1.2345"
			expect(formatInteger(num, ".", 4)).to.equal(expectedResult)
		end)
		it("Should format negative integer whose length greater than sepCount with comma properly", function()
			local num = -12345
			local expectedResult = "-1.2345"
			expect(formatInteger(num, ".", 4)).to.equal(expectedResult)
		end)
		it("Should format positive integer whose length greater than sepCount with dot properly", function()
			local num = 12345
			local expectedResult = "1.2345"
			expect(formatInteger(num, ".", 4)).to.equal(expectedResult)
		end)
	end)
end