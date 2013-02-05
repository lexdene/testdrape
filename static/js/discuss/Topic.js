(function(jq){
	jq(function(){
		jq('#reply_form').submit(function(){
			var form = jq(this);
			form.ajaxSubmit({
				'success':function(){
					alert('回复成功');
					location.reload();
				},
				'failed':function(msg){
					alert('回复失败:'+msg);
				},
				'validate':{
					'form_area':[
						{
							'key' : 'text',
							'name' : '回复',
							'validates' : [
								['notempty'],
								['len',4,5000]
							]
						},
					]
					,
					'callback':function(result,msg){
						if( ! result ){
							alert(msg);
						}
					}
				}
			});
		});
	});
})(jQuery);
