(function(j) {
	function ajaxSubmit(form,options){
		var form = j(form);
		var senddata = {};
		var inputlist = form.find('input,textarea');
		inputlist.each(function(){
			var name = j(this).attr('name');
			if( name == undefined ){
				return ;
			}
			var value = j(this).val();
			var type = j(this).attr('type');
			switch(type){
			case 'text':
			case 'password':
			default:
				senddata[name] = value;
				break;
			case 'radio':
			case 'checkbox':
				if( j(this).attr('checked') == 'checked'){
					senddata[name] = value;
				}else{
					senddata[name] = '';
				}
				break;
			}
		});
		inputlist.attr('disabled',true);
	
		var url = form.attr('action');
		j.post(
			url,
			senddata,
			function(){},
			'json'
		)
		.success(function(rspdata){
			switch(rspdata.result){
			case 'success':
				if( typeof options.success == 'function' ){
					options.success(rspdata);
				}
				break;
			case 'failed':
				if( typeof options.failed == 'function' ){
					if( rspdata.msg ){
						options.failed(rspdata.msg);
					}else{
						options.failed('no message');
					}
				}
				break;
			default:
				break;
			}
			inputlist.attr('disabled',false);
		})
		.error(function(){
			if( typeof options.failed == 'function' ){
				options.failed('network error');
			}
			inputlist.attr('disabled',false);
		})
	}
	j.fn.extend({
		ajaxSubmit: function(options) {
			return this.each(function(){
				ajaxSubmit(this,options);
			});
		}
	});
})(jQuery); 
