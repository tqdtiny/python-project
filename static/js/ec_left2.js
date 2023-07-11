var ec_left2 = echarts.init(document.getElementById("l2"),"dark");

var ec_left2_option = {
	title : {
	        text: '震级与震源深度的关系',
	    },
	    grid: {
	        left: '3%',
	        right: '4%',
	        bottom: '3%',
	        containLabel: true
	    },
	    tooltip : {
	        trigger: 'item',
	        showDelay : 0,
	        formatter : function (params) {
	            if (params.value.length > 1) {
	                return params.seriesName + ' :<br/>'
	                   + params.value[0] + '千米 '
	                   + params.value[1] + '级 ';
	            }
	            else {
	                return params.seriesName + ' :<br/>'
	                   + params.name + ' : '
	                   + params.value + '级 ';
	            }
	        },
	        axisPointer:{
	            show: true,
	            type : 'cross',
	            lineStyle: {
	                type : 'dashed',
	                width : 1
	            }
	        }
	    },
	    xAxis : [
	        {
	            type : 'value',
	            scale:true,
	            axisLabel : {
	                formatter: '{value} 千米'
	            },
	            splitLine: {
	                lineStyle: {
	                    type: 'dashed'
	                }
	            }
	        }
	    ],
	    yAxis : [
	        {
	            type : 'value',
	            scale:true,
	            axisLabel : {
	                formatter: '{value} 级'
	            },
	            splitLine: {
	                lineStyle: {
	                    type: 'dashed'
	                }
	            }
	        }
	    ],
	    series : [
	        {
	            name:"深度-震级",
	            type:'scatter',
	            data: [[17.0, 5.6], [17.3, 7.8]
	            ],
	            markLine : {
	                data : [
	                    {type : 'average', name: '平均值'}
	                ]
	            }
	        }
	    ]
};

ec_left2_option && ec_left2.setOption(ec_left2_option);
