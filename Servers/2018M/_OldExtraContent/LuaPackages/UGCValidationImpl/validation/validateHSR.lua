local function validateHSR(wrapLayer: WrapLayer): (boolean, {string}?)
	if not (wrapLayer :: any):IsHSRReady() then
		return false, { "HSR data not ready!" }
	end
	return true
end

return validateHSR
