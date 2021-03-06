(function(jq){
	function showError(text){
		jq('.msg_block').find('.msg').html(text);
	}
	function setAvatar(avatar){
		var form = jq('#edituserinfo_form');
		form.find('input[name=avatar]').val(avatar);
		jq('.avatar_preview').find('.avatar').attr('src',avatar);
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
		var dialog = jq('#dialog').dialog();
		jq('#upload_avatar_btn').click(function(){
			jq('#dialog').find('iframe').attr('src','../common/UploadImage?accept=image/gif,image/jpeg,image/png');
			dialog.show();
		});
		jq('#dialog').find('.close_button').click(function(){
			jq('#dialog').find('iframe').attr('src','');
			dialog.close();
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
		window.uploadCallBack = function(result,savepath){
			if( 'success' == result ){
				setAvatar(savepath);
			}
		}
	});
})(jQuery);
