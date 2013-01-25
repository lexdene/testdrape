var topic = {};
topic.reply_id = -1;
topic.sendReply = function(){
	var c = document.getElementById('reply_content');
	var b = document.getElementById('reply_button');
	topic.reply_begin([c,b]);
	
	if( c.value == '' ){
		alert('请输入回复内容');
		topic.reply_complete([c,b]);
		return;
	}
	if( my_userid < 0 ){
		alert('请先登录');
		topic.reply_complete([c,b]);
		return;
	}
	var data = {
		tid: topic_id,
		reply_to_id: topic.reply_id,
		text: c.value
	}
	jQuery.post(
		'/discuss/PostReplyResult',
		data,
		function(){},
		'json'
	)
	.success(function(data){
		if(data.result){
			alert('回复成功');
			location.reload();
		}else{
			alert('回复失败，请重试');
		}
	})
	.error(function(){
		alert('回复失败，请重试');
	})
	.complete(function(){
		topic.reply_complete([c,b]);
	})
}
topic.reply_begin = function(l){
	var i;
	for( i in l ){
		l[i].disabled = true;
	}
}
topic.reply_complete = function(l){
	var i;
	for( i in l ){
		l[i].disabled = false;
	}
}
