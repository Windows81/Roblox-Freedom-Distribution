return function(title, pageView, configs)
	return {
		title = title,
		content = {
			component = pageView,
			options = configs
		},
	}
end