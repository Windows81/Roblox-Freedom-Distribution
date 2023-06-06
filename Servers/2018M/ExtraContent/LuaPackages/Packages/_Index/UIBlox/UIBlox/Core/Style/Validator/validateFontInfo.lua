local Validator = script.Parent
local Style = Validator.Parent
local App = Style.Parent
local UIBlox = App.Parent
local Packages = UIBlox.Parent

local t = require(Packages.t)

export type FontInfo = {
	RelativeSize: number,
	RelativeMinSize: number,
	Font: Enum.Font,
}

return t.strictInterface({
	RelativeSize = t.numberMinExclusive(0),
	RelativeMinSize = t.numberMinExclusive(0),
	Font = t.EnumItem,
})
