(function(jq){
	jq(function(){
		jq('#count_down').count_down({
			'num_class':'num',
			'time':3,
			'location_class':'location'
		});
	});
})(jQuery);