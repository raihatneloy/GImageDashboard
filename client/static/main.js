$(function() {
	var alert_success = $('<div class="alert alert-success alert-dismissible"></div>')
    var alert_error = $('<div class="alert alert-danger alert-dismissible"></div>')
    var close_button = $('<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>')
    var selected_images = [];
    $('#login-form-link').click(function(e) {
		$("#login-form").delay(100).fadeIn(100);
 		$("#register-form").fadeOut(100);
		$('#register-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
	$('#register-form-link').click(function(e) {
		$("#register-form").delay(100).fadeIn(100);
 		$("#login-form").fadeOut(100);
		$('#login-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
	var create_alert = function(response){
		console.log('Creating alert')
		if (response['Success']){
			var success = $(`
				<div class="alert alert-success alert-dismissible">
					<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
					${response['Success']}
				</div>
				`
			);
			success.appendTo('#login_alert');
		}
		else{
			for (var key in response){
				var error = $(`
					<div class="alert alert-danger alert-dismissible">
						<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
						${key}: ${response[key]}
					</div>
				`)
				error.appendTo('#login_alert');
			}
		}
	};
	var register_submit = function(){
		$.ajax({
			url: Flask.url_for('register'),
			data: $('#register-form').serialize(),
			type: 'POST',
			success: function(response){
				var resp = $.parseJSON(response);

				create_alert(resp);

				if (resp['Success'])
					$('#login-form-link').click();
			},
			error: function(response){
				console.log(response);
			}
		})
	}
	var login_submit = function(){
		$.ajax({
			url: Flask.url_for('authenticate'),
			data: $('#login-form').serialize(),
			type: 'POST',
			success: function(response){
				var resp = $.parseJSON(response);

				create_alert(resp);

				if (resp['Success'])
					window.location = Flask.url_for('index');
			},
			error: function(response){
				console.log(response);
			}
		});
	};
	var search_image = function(){
		var keyword = $('#search').val();

		if (keyword === ''){
			return ;
		}

		window.location = Flask.url_for('search', {"keyword": keyword});
	}
	$('#login-submit').click(function(e){
		login_submit(e);
	});
	$('#login-form').keypress(function(e){
		if (e.keyCode == 13){
			$('#login-submit').click();
		}
	});
	$('#register-submit').click(function(e){
		register_submit(e);
	});
	$('#register-form').keypress(function(e){
		if (e.keyCode == 13){
			$('#register-submit').click();
		}
	});
	$('#search').keypress(function(e){
		if (e.keyCode == 13){
			search_image();
		}
	});
	$(".image-checkbox").each(function () {
	  if ($(this).find('input[type="checkbox"]').first().attr("checked")) {
	    $(this).addClass('image-checkbox-checked');
	  }
	  else {
	    $(this).removeClass('image-checkbox-checked');
	  }
	});

	// sync the state to the input
	$(".image-checkbox").on("click", function (e) {
	  $(this).toggleClass('image-checkbox-checked');
	  var $checkbox = $(this).find('input[type="checkbox"]');
	  $checkbox.prop("checked",!$checkbox.prop("checked"))
	  var image = $(this).find('img')[0];
	  
	  var image_info = {};
	  /*image_info['link'] = image['name'];
	  image_info['thumbnail'] = image['src'];*/

	  var image_index = -1;
	  var select_index = image['name'];

	  var index = 0
	  for (var index=0;index<selected_images.length;index++){
	  	if (selected_images[index] === select_index){
	  		image_index = index;
	  		break;
	  	}
	  }

	  if (image_index != -1){
	  	selected_images.splice(image_index, 1);
	  }else{
	  	selected_images.push(select_index);	
	  }

	  console.log(selected_images);

	  e.preventDefault();
	});
	$("#add_favorite").click(function(e){
		if (selected_images.length === 0){
			create_alert({
				'Error': 'Please select image for adding to your dashboard!'
			});
			return ;
		}
		console.log(JSON.stringify(selected_images));

		$.ajax({
			url: Flask.url_for('add_favorite'),
			data: JSON.stringify({"images": selected_images}),
			type: 'POST',
			success: function(response){
				window.location = Flask.url_for('dashboard');
			},
			error: function(response){
				console.log(response);
			}
		});
	})
});
