local Modules = game:GetService("CoreGui").RobloxGui.Modules
local LocalizationService = game:GetService("LocalizationService")

local Immutable = require(Modules.Common.Immutable)
local Roact = require(Modules.Common.Roact)
local ExternalEventConnection = require(Modules.Common.RoactUtilities.ExternalEventConnection)
local RoactServices = require(Modules.LuaApp.RoactServices)
local TableUtilities = require(Modules.LuaApp.TableUtilities)

local service = RoactServices.createService(script.Name)

-- connect() : given an array of props, create a wrapper that localizes those props from the stored locale
-- propsToLocalize : (array<string>) a list of props in the wrapped component to localize
function service.connect(propsToLocalizeList)
	local propsToLocalize = {}
	for _, propName in ipairs(propsToLocalizeList) do
		propsToLocalize[propName] = true
	end

	return function(component)
		assert(component ~= nil, "Expected component to be passed to connection, got nil.")

		local name = ("Localize(%s)"):format(tostring(component))
		local connection = Roact.PureComponent:extend(name)

		function connection:init()
			local localization = service.get(self._context)

			assert(localization ~= nil, table.concat({
				"Cannot initialize RoactLocalization component without being a descendent of ServiceProvider!",
				("Tried to wrap component %q"):format(tostring(component)),
				"Make sure there is a ServiceProvider above this component in the tree."
			}, "\n"))

			self.state = {
				locale = LocalizationService.RobloxLocaleId
			}
			self.localization = localization

			self.updateLocalization = function(newLocale)
				self:setState({
					locale = newLocale
				})
			end
		end

		function connection:render()
			local localization = service.get(self._context)

			local localizedProps = {}
			for propName in pairs(propsToLocalize) do
				local stringInfo = self.props[propName]
				assert(stringInfo ~= nil,
					("No localization string or table found for \"%s\""):format(propName))
				assert(type(stringInfo) == "table" or type(stringInfo) == "string",
					("Localized field \"%s\" is not a string or table."):format(propName))

				if type(stringInfo) == "table" then
					assert(type(stringInfo[1]) == "string",
						("Localization table \"%s\" requires a key of type string, got %s"):format(propName, type(stringInfo[1])))
					localizedProps[propName] = localization:Format(stringInfo[1], stringInfo)
				else
					localizedProps[propName] = localization:Format(stringInfo)
				end
			end

			local props = Immutable.JoinDictionaries(self.props, localizedProps)
			if type(component) == "string" then
				props.locale = nil
			end

			return Roact.createElement(ExternalEventConnection, {
				event = LocalizationService:GetPropertyChangedSignal("RobloxLocaleId"),
				callback = self.updateLocalization,
			}, {
				Roact.createElement(component, props)
			})
		end

		function connection:shouldUpdate(newProps, newState)
			if newState ~= self.state then
				return true
			end

			for propName in pairs(propsToLocalize) do
				local newProp = newProps[propName]
				local oldProp = self.props[propName]
				if newProp ~= nil and oldProp ~= nil then
					if type(newProp) == "table" and type(oldProp) == "table" then
						if not TableUtilities.ShallowEqual(newProp, oldProp) then
							return true
						end
					elseif newProp ~= oldProp then
						return true
					end
				elseif newProp ~= nil or oldProp ~= nil then
					return true
				end
			end

			return not TableUtilities.ShallowEqual(newProps, self.props, propsToLocalize)
		end

		return connection
	end
end

return service