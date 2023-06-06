local GuiService = game:GetService("GuiService")
local UserInputService = game:GetService("UserInputService")

local function getScreenBottomInset()
	if not _G.__TESTEZ_RUNNING_TEST__ then
		local nativeBottomBarHeight = UserInputService.BottomBarSize.Y
		local bottomSafeZoneHeight = GuiService:GetSafeZoneOffsets().bottom
		-- When nativeBottomBar is hidden(nativeBottomBarHeight == 0), we need to fall back to bottomSafeZoneHeight
		return nativeBottomBarHeight == 0 and bottomSafeZoneHeight or nativeBottomBarHeight
	else
		return 0
	end
end

return getScreenBottomInset