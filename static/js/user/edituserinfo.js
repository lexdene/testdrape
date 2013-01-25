var edituserinfo = {};
edituserinfo.getObjectURL = function(file) {
	var url = null ;
	if (window.createObjectURL!=undefined) { // basic
		url = window.createObjectURL(file) ;
	} else if (window.URL!=undefined) { // mozilla(firefox)
		url = window.URL.createObjectURL(file) ;
	} else if (window.webkitURL!=undefined) { // webkit or chrome
		url = window.webkitURL.createObjectURL(file) ;
	}
	return url ;
}

edituserinfo.avatarChanged = function(o){
	var url = this.getObjectURL(o.files[0]);
	var avatarImg = document.getElementById('avatar');
	avatarImg.src = url;
}
