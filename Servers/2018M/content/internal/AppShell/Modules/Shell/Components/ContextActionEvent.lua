--[[
		A simple component that allows you to bind to ContextActionService at CoreScript level

		Props
			name - the name of the binded action
			callback - the function that is invoked
			binds - the input that triggers the action
				this is a table - example { Enum.KeyCode.ButtonA, Enum.KeyCode.ButtonX }
			actionPriority - the action priority
		Usage:
			ContextActionCn = Roact.createElement(ContextActionEvent, {
				name = "MyContextActionBind",
				callback = function() print("context event") end,
				binds = { Enum.KeyCode.Thumbstick2, Enum.KeyCode.ButtonB, Enum.KeyCode.A },
				actionPriority = 1,
			}),

		Note: Cannot currently write a unit test for this component because it uses functions that
		are RobloxScript security. LuaCore team is looking into a solution for this
]]
local ContextActionService = game:GetService("ContextActionService")
local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)

local ContextActionEvent = Roact.Component:extend("ContextActionEvent")

local DEFAULT_ACTION_PRIORITY = 2000

function ContextActionEvent:render()
	return nil
end

function ContextActionEvent:didMount()
	if self.props.actionPriority then
		ContextActionService:BindCoreActionAtPriority(self.props.name, self.props.callback, false, DEFAULT_ACTION_PRIORITY + self.props.actionPriority, unpack(self.props.binds))
	else
		ContextActionService:BindCoreAction(self.props.name, self.props.callback, false, unpack(self.props.binds))
	end
end

function ContextActionEvent:didUpdate(oldProps)
	if self.props.callback ~= oldProps.callback or self.props.name ~= oldProps.name then
		ContextActionService:UnbindCoreAction(oldProps.name)
		if self.props.actionPriority then
			ContextActionService:BindCoreActionAtPriority(self.props.name, self.props.callback, false, DEFAULT_ACTION_PRIORITY + self.props.actionPriority, unpack(self.props.binds))
		else
			ContextActionService:BindCoreAction(self.props.name, self.props.callback, false, unpack(self.props.binds))
		end
	end
end

function ContextActionEvent:willUnmount()
	ContextActionService:UnbindCoreAction(self.props.name)
end

return ContextActionEvent
