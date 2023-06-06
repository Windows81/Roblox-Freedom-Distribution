return function()
	local RequestsStatus = require(script.Parent.RequestsStatus)

	it("has the expected fields, and only the expected fields", function()
		local state = RequestsStatus(nil, {})

		local expectedKeys = {
			GameSortTokenFetchingStatus = true,
			GameSortsStatus = true,
			SearchesInGamesStatus = true,
		}

		for key in pairs(expectedKeys) do
			assert(state[key] ~= nil, string.format("Expected field %q", key))
		end

		for key in pairs(state) do
			assert(expectedKeys[key] ~= nil, string.format("Did not expect field %q", key))
		end
	end)
end