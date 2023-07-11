var ec_left1 = echarts.init(document.getElementById("l1"),"dark"); //初始化

var ec_left1_option = {
		// 标题样式
      	title: {
      		text: '2023年地震累计趋势',
			textStyle: {
				
			},
			left: 'left'
      	},
		// 设置图例
      	legend: {
      		data: ['累计震级'],
			left: 'right'
      	},

      	//  图表距边框的距离,可选值：'百分比'¦ {number}（单位px）
      	grid: {
      		top: 50, // 等价于 y: '16%'
      		left: '4%',
      		right: '6%',
      		bottom: '4%',
      		containLabel: true
      	},

      	// 提示框
      	tooltip: {
      		trigger: 'axis',
			axisPointer: {
				type: 'line',
				lineStyle: {
					color: '#7171C6'
				}
			}
      	},

      	xAxis: {
      		type: 'category',
      		data:[2000,2001,2002,2003]
      	},

      	yAxis: {
      		type: 'value',
      		axisLine: {
				show: true
      		},
			axisLabel: {
				show: true,
				color: 'white',
				fontSize: 12,
				formatter: function(value) {
					if (value >= 1) {
						value = value / 1 + '级';
					}
					return value;
				}
			},
			splitLine: {
				show: true,
				lineStyle: {
					color: '#172738',
					width: 1,
					type: 'solid'
				}
			}
      	},

      	series: [{
      			name: '累计震级',
      			data:[5,6,8,2],
      			type: 'line',
      			// 设置折线弧度，取值：0-1之间
      			smooth: true
      		}
      	]
      };
	  
	  ec_left1.setOption(ec_left1_option);
	  