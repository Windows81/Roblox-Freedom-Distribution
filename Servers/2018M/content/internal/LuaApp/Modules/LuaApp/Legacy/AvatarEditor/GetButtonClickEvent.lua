local luaAppLegacyInputDisabledGlobally = settings():GetFFlag('LuaAppLegacyInputDisabledGlobally2')

return function(component)
	if luaAppLegacyInputDisabledGlobally then
		return component.Activated
	else
		return component.MouseButton1Click
	end
end
