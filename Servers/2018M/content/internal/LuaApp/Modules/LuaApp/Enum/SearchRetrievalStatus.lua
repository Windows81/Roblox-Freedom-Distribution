local SearchRetrievalStatus = {}

local EnumValues =
{
	Fetching = "Fetching",
	Done = "Done",
	Failed = "Failed",
	Removed = "Removed",
}

setmetatable(SearchRetrievalStatus,
	{
		__newindex = function(t, key, index)
		end,
		__index = function(t, index)
			assert(EnumValues[index] ~= nil, ("SearchRetrievalStatus Enum has no value: " .. tostring(index)))
			return EnumValues[index]
		end
	})

return SearchRetrievalStatus