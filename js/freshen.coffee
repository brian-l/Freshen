$ ->
	if not window.hasOwnProperty('freshenReceive')
		window.freshenReceive = (data) ->
			document.location = document.location

		$.ajax
			url: 'http://localhost:9020/'
			dataType: 'jsonp'
			data:
				callback: 'window.freshenReceive'
