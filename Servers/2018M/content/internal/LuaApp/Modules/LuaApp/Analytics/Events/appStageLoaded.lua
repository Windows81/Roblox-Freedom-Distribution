-- appStageLoaded : fires when the app loads and passes a milestone (otherwise known as an `appStage`)
-- eventContext : (string) the location or context in which the event is occurring.
-- appStage : (string) the name of the appStage that has been completed
return function(eventStreamImpl, eventContext, appStage)
	assert(type(eventContext) == "string", "Expected eventContext to be a string")
	assert(type(appStage) == "string", "Expected appStage to be a string")

	local eventName = "appStageLoaded"
	local additionalArgs = {
		stage = appStage
	}

	eventStreamImpl:setRBXEventStream(eventContext, eventName, additionalArgs)
end