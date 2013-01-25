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
