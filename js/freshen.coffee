$ ->
	if not window.hasOwnProperty('freshenReceive')
		window.freshenReceive = (data) ->
			document.location = document.location

		$.ajax
			url: 'http://localhost:9020/'
			dataType: 'jsonp'
			jsonp: false
			jsonpCallback: 'window.freshenReceive'
			cache: true
			data:
				callback: 'window.freshenReceive'
