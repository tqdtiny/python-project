// 点击tab栏切换内容设置
$(function(){
			 $(".tab_list li").click(function(){
				$(".tab_list li").removeClass("current");  //干掉所有人
				 $(this).addClass("current");   //留下我自己
	
				var index = $(this).index();
				$(".tab_con .item").hide();   //干掉所有人
				$(".tab_con .item").eq(index).show();  //留下我自己
				});
		 });