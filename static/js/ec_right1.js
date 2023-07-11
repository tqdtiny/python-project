var ec_right1 = echarts.init(document.getElementById("r1"),"dark");

var ec_right1_option = {
	title: {
		text: '地震震级分段统计',
		textStyle: {
			color: 'white'
		},
		left: 'left'
	},
	// grid: {
	// 	left: 50,
	// 	top: 50,
	// 	right: 0,
	// 	width: '87%',
	// 	height: 320,
	// },
	color: ['#3398DB'],
	tooltip: {
		trigger: 'axis',
		axisPointer: {
			type: 'shadow'
		}
	},
	//全局字体样式
	// textStyle: {
	// 	fontFamily: 'PingFangSC-Medium',
	// 	fontSize: 12,
	// 	color: '#858E96',
	// 	lineHeight: 12
	// },
	xAxis: {
		type: 'category',
		//                              scale:true,
		data: ['0-1', '1-2', '2-3', '3-5', '5-7', '7-15']
	},
	yAxis: {
		type: 'value',
		//坐标轴刻度设置
		},
	series: [{
		type: 'bar',
		data: [],
		barMaxWidth: "50%"
	}]
};
ec_right1.setOption(ec_right1_option)
