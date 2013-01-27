var register = {};
register.validate_repassword = function(o,val,vil){
	var password = jQuery(o).closest('form').find('input[name=password]').val();
	if( password == val ){
		return {
			result:true
		}
	}else{
		return {
			result:false,
			msg:'两次输入密码不一致',
		}
	}
}
(function(jq,jw){
	jq(function(){
		jq('#register_form').submit(function(){
			var v = jdmd_widget.validate_and_error_all( this );
			if( false == v ){
				return false;
			}
			var form = jq(this);
			form.ajaxSubmit({
				'success':function(){
					alert('登录成功');
					window.location = WEB_ROOT + form.attr('redirect');
				},
				'failed':function(msg){
					alert('登录失败:'+msg);
				}
			});
			return false;
		});
	});
})(jQuery,jdmd_widget);
