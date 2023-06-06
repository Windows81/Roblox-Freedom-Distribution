--A generic module to make safe async function calls for rodux async actions
--Similar to makeSafeAsync, but it requests the store whenever get called
--Will put the store as the first parameter for asyncFunc and callback
--Also provide a retry logic if set up retries(retry times), retryFunc(optional - whether retry) and waitFunc(optional - a wait function between retries)
local function makeSafeAsyncRodux(input)
	local this = {}
    local currentFuncState = nil

	--The asyncFunc should always be the same
	local asyncFunc = input.asyncFunc
	assert(type(asyncFunc) == "function", "Must init with an async function.")

	--Many async funtion calls are user related, so we add this attribute
	local userRelated = input.userRelated

	local callback = input.callback
	--By default, we don't have the retry logic
	local retries = input.retries or 0
	--By default, the retry function return false and will terminate retry
	local retryFunc = input.retryFunc or function() return false end
	--By default, the wait function will wait exponential of tryCount
	local waitFunc = input.waitFunc or function(tryCount) wait(tryCount * tryCount) end
	local cancelled = false
	--Add this cancel which enables us to cancel callback
	function this:Cancel()
		cancelled = true
	end

	setmetatable(this, {
		__call = function(self, store, ...)
			assert(type(store) == "table", "Must call with the store.")

			local lastFuncState = {}
			currentFuncState = lastFuncState

			local lastUserState = store:getState().RobloxUser

			local function terminate()
				if currentFuncState ~= lastFuncState then
					return true
				end

				if userRelated and lastUserState ~= store:getState().RobloxUser then
					return true
				end

				if cancelled then
					return true
				end
			end

			local results = {asyncFunc(store, ...)}
			local tryCount = 1
			local terminated = terminate()
			while not terminated and tryCount <= retries and retryFunc(store, unpack(results)) do
				waitFunc(tryCount)
				tryCount = tryCount + 1
				terminated = terminate()
				if not terminated then
					results = {asyncFunc(store, ...)}
					terminated = terminate()
				end
			end

			if not terminated then
				if type(callback) == "function" then
					callback(store, unpack(results))
				end
			end
		end
	})

	return this
end

return makeSafeAsyncRodux
