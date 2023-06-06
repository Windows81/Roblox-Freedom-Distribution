--[[
	A function to return a unique ID, used for search results
]]

local lastId = 0

return function()
	lastId = lastId + 1
	return lastId
end