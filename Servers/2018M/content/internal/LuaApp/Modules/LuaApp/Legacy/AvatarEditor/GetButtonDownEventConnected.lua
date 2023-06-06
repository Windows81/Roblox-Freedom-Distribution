--[[
	This module will never be called in console platforms
	That is, console will never use the modules which are related to MouseButton1Down
	So this patch is safe for consoles
]]

local luaAppLegacyInputDisabledGlobally = settings():GetFFlag('LuaAppLegacyInputDisabledGlobally2')

return function(component, toDoFunc)
	if luaAppLegacyInputDisabledGlobally then
		component.InputBegan:connect(function(inputObject)
			if inputObject.UserInputState == Enum.UserInputState.Begin then
				local inputType = inputObject.UserInputType
				if inputType == Enum.UserInputType.Touch or inputType == Enum.UserInputType.MouseButton1 then
					toDoFunc(inputObject.Position.x, inputObject.Position.y)
				end
			end
		end)
	else
		component.MouseButton1Down:connect(toDoFunc)
	end
end

