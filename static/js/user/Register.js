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
};
(function(jq,jw){
	jq(function(){
		jq('#register_form').submit(function(){
			var v = jw.validate_and_error_all( this );
			if( false == v ){
				return false;
			}
			var form = jq(this);
			form.ajaxSubmit({
				'success':function(){
					alert('注册成功');
					window.location = WEB_ROOT + form.attr('redirect');
				},
				'failed':function(msg){
					alert('注册失败:'+msg);
				}
			});
			return false;
		});
	});
})(jQuery,jdmd_widget);
