$ ->
	window.freshenReceive = (data) ->
		if parseInt(data) > 0
			location.reload()
		else
			$.ajax
				url: 'http://localhost:9020/'
				dataType: 'jsonp'
				jsonp: false
				jsonpCallback: 'window.freshenReceive'
				cache: true
				data:
					callback: 'freshenReceive'
	
	window.setTimeout (->
		window.freshenReceive(0)), 1000
