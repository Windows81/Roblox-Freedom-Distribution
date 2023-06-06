local ScreenItem = {}

ScreenItem.Priority = {
	Default = 1,
	Overlay = 2,
	Elevated = 3,
	Immediate = 4,
}

function ScreenItem.new(id, priority, data)
	local self = {}

	self.id = id
	self.priority = priority
	self.createdAt = tick()
	self.data = data

	return self
end

return ScreenItem
