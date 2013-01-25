var posttopic = {
	submit:function(o){
		posttopic.submitBegin(o);
		var data = {};
		jQuery(o).find('input,textarea').each(function(){
			var name = jQuery(this).attr('name');
			var val = jQuery(this).val();
			if( name ){
				data[name] = val;
			}
			if( 'pnum' == name ){
				posttopic.pnum = val;
			}
		});
		var url = jQuery(o).attr('action');
		jQuery.post(
			url,
			data,
			function(){},
			'json'
		)
		.success(function(data){
			if(data.result){
				posttopic.submitSuccess();
			}else{
				posttopic.submitFailed(data.msg);
			}
		})
		.error(function(){
			posttopic.submitFailed();
		})
		.complete(function(){
			posttopic.submitCompleted(o);
		})
	},
	submitSuccess:function(){
		alert('发布成功');
		window.location = '/discuss/List?pnum='+posttopic.pnum;
	},
	submitFailed:function(){
		alert('发布失败，请重试');
	},
	submitBegin:function(o){
		jQuery(o).find('input,textarea').each(function(){
			this.disabled = true;
		});
	},
	submitCompleted:function(o){
		jQuery(o).find('input,textarea').each(function(){
			this.disabled = false;
		});
	}
};
