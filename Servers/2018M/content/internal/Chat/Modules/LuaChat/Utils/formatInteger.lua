return function(num, sep, sepCount)
	assert(type(num) == "number", "formatInteger expects a number; was given type: " .. type(num))

	sep = sep or ","
	sepCount = sepCount or 3

	local parsedInt = string.format("%.0f", math.abs(num))
	local firstSeperatorIndex = #parsedInt % sepCount
	if firstSeperatorIndex == 0 then
		firstSeperatorIndex = sepCount
	end

	local seperatorPattern = "(" .. string.rep("%d", sepCount) .. ")"
	local seperatorReplacement = sep .. "%1"
	local result = parsedInt:sub(1, firstSeperatorIndex) ..
			parsedInt:sub(firstSeperatorIndex+1):gsub(seperatorPattern, seperatorReplacement)
	if num < 0 then
		result = "-" .. result
	end

	return result
end
