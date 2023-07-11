// 神经网络预测内容前后端交互设置
$(document).ready(function(){
	  			$('#prediction-form').submit(function(event){
	  				event.preventDefault();
	  				var formData = {
						'time': $('#time').val(),
	  					'longitude': $('#longitude').val(),
	  					'latitude': $('#latitude').val()
	  				};
	  				$('#loader').show();
	  				$('#result').html('');
	  				$.ajax({
	  					url: '/predict',
	  					type: 'POST',
	  					data: formData,
	  					success: function(response){
	  						$('#loader').hide();
	  						$('#result').html('预测结果为: ' + '震级：' + response.magnitude + '级，' + '深度：' + response.deep + '千米');
	  					},
	  					error: function(error){
	  						console.log(error);
	  					}
	  				});
	  			});
	  		});