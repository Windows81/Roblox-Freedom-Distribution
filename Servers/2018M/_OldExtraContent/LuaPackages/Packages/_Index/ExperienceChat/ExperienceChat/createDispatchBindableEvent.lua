local function createDispatchBindableEvent(store)
	local bindableEvent = Instance.new("BindableEvent")

	bindableEvent.Event:Connect(function(action)
		store:dispatch(action)
	end)

	return bindableEvent
end

return createDispatchBindableEvent
