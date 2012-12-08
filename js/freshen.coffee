$ ->
	# bind a global function to the window
	window.freshenReceive = (data) ->
		# when data > 0, there is at least 1 file change event
		if parseInt(data) > 0
			location.reload()
		else
			# asynchronous jsonp request
			$.ajax
				url: 'http://localhost:9020/'
				dataType: 'jsonp'
				jsonp: false
				jsonpCallback: 'window.freshenReceive'
				# prevent jQuery from appending timestamp _
				cache: true
				data:
					callback: 'window.freshenReceive'

	# prevent window from reloading uncontrollably
	window.setTimeout (->
		window.freshenReceive(0)), 1000
