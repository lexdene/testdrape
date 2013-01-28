(function(j){
	j.fn.extend({
		count_down: function(options) {
			return this.each(function(){
				var numObj = j(this).find('.'+options['num_class']);
				var locationObj = j(this).find('.'+options['location_class']);
				var location = locationObj.attr('href');
				var time = options['time'];
				numObj.html( time );
				var timer = setInterval(
					function(){
						--time;
						numObj.html( time );
						if( time <= 0 ){
							clearInterval( timer );
							window.location = location;
						}
					},
					1000
				);
			});
		}
	});
})(jQuery);
