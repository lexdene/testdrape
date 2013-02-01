(function(jq){
	function showError(text){
		jq('.msg_block').find('.msg').html(text);
	}
	jq(function(){
		var form = jq('#edituserinfo_form');
		form.find('input[name=avatar]').keyup(function(){
			console.log(jq(this).val());
			jq('.avatar_preview').find('.avatar').attr('src',jq(this).val());
		});
		jq('.avatar_preview').find('.avatar').error(function(){
			showError('无法载入图片');
		});
		jq('.avatar_preview').find('.avatar').load(function(){
			showError('');
		});
		form.submit(function(){
			form.ajaxSubmit({
				'success':function(){
					alert('修改成功');
					location.reload();
				},
				'failed':function(msg){
					alert('修改失败:'+msg);
				}
			});
		});
	});
})(jQuery);