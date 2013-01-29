(function(j,jw){
	j(function(){
		j('.valcode_btn').click(jw.refresh_valcode_img);
		document.getElementById('submit_form').onsubmit=function(){
			var v = jdmd_widget.validate_and_error_all( this );
			if( false == v ){
				return false;
			}
			var form = j(this);
			form.ajaxSubmit({
				'success':function(){
					alert('登录成功');
					window.location = WEB_ROOT + form.attr('redirect');
				},
				'failed':function(msg){
					alert('登录失败:'+msg);
				}
			});
			form.find('input[name=valcode]').val('');
			jw.refresh_valcode_img();
			return false;
		}
	});
})(jQuery,jdmd_widget);
