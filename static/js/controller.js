function gettime(){
	$.ajax({
		url:"/time",
			timeout:1000, //超出数据设置为10秒
			success:function(data){
				$("#tim").html(data)
			},
			error:function(xhr,type,errorThrown){

			}
		});
	}

function get_all(){
$.ajax({
	url:"/get_all",
	dataType:"json",
	success:function loop_ajax4(data) {
		// var h1 = $("<ul ></ul>");
		// console.log(data)
		for (let i = 0; i <= data.length; i++) {
			var alls = data[i]
			$(".line h1").eq(i).text(alls)
			// var li = "<li>"+data[i]+"</li>"
			// h1.append(li)
		}
		// console.log(ul)
		// $(".line").append(h1)
	},
	error:function(xhr,type,errorThrown){

	}
})
}
	
function get_c2_data() {
	$.ajax({
		url:"/c2",
		success:function(data){
		// console.log(data)
			ec_center_option.series[0].data=data.data
			ec_center.setOption(ec_center_option)
		},
		error:function(xhr,type,errorThrown){
		
		}
	})
}

function get_l1_data() {
	$.ajax({
		url:"/l1",
		success:function(data){
			// console.log(data)
//			ec_left1_option.xAxis[0].data=data.day
			ec_left1_option.series[0].data=data.level
			ec_left1_option.xAxis.data=data.time
			ec_left1.setOption(ec_left1_option)
		},
		error:function(xhr,type,errorThrown){
		
		}
	})
}

function get_l2_data() {
	$.ajax({
	  url: "/l2", // Flask 路由
	  type: "GET",
	  dataType: "json",
	  success: function(data) {
	    // 从响应中获取 citydata 数据
		ec_left2_option.series[0].data=data.data
		ec_left2.setOption(ec_left2_option)
	  },
	  error: function(xhr,type,errorThrown) {
	    // alert("数据获取失败，请刷新页面重试！");
	  }
	});

}


function get_r1_data() {
	$.ajax({
		url:"/r1",
		success:function(data){
			ec_right1_option.series[0].data=data.data
			ec_right1.setOption(ec_right1_option)
		},
		error:function(xhr,type,errorThrown){
		
		}
	})
}

function get_r2_data() {
	$.ajax({
		url:"/r2",
		success:function(data){
		console.log(data)
			ec_right2_option.series[0].data=data.data
			ec_right2.setOption(ec_right2_option)
		},
		error:function(xhr,type,errorThrown){
		
		}
	})
}



// get_c2_data()
// setInterval(gettime,1000)
// setInterval(get_all,1000)