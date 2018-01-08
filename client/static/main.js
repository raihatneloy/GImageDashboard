$(function() {
	var alert_success = $('<div class="alert alert-success alert-dismissible"></div>')
    var alert_error = $('<div class="alert alert-danger alert-dismissible"></div>')
    var close_button = $('<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>')
    var selected_images = [];
    var frm;
    var angle = 0;
    /*function refresh(node)
	{
	   var times = 1000; // gap in Milli Seconds;

	   (function startRefresh()
	   {
	      var address;
	      if(node.src.indexOf('?')>-1)
	       address = node.src.split('?')[0];
	      else 
	       address = node.src;
	      node.src = address+"?time="+new Date().getTime();

	      setTimeout(startRefresh,times);
	   })();

	}

	window.onload = function()
	{
	  var node = document.getElementById('preview');
	  refresh(node);
	  // you can refresh as many images you want just repeat above steps
	}*/
    var dns = 'http://163.53.149.166:5001'
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
			create_alert({'Error': 'Please Specify any search keyword'})
			return ;
		}

		window.location = Flask.url_for('search', {"keyword": keyword});
		return;
	};
	var search_page = function(){
		var keyword = $('#facebooksearch').val();
		var fb_info = {};

		$.ajax({
			url: Flask.url_for('get_fbinfo'),
			type: 'GET',
			success: function(fb_info){
				if (keyword === ''){
					create_alert({'Error': 'Please Specify any search keyword'})
					return;
				}

				if (!fb_info['facebook_id']){
					create_alert({'Error': 'Please Connect with your facebook account. Click the Connect button!'})
					
					$('#fbpage_div').load(' #fbpage_div');
					$('#fbpage_show').load(' #fbpage_show');
					
					return;
				}

				window.location = Flask.url_for('search_fb', {"keyword": keyword});
			},
			error: function(response){
				console.log('response');
			}
		});
	};
	var search_500px = function(){
		var keyword = $('#500pxsearch').val();
		
		if (keyword === ''){
			create_alert({'Error': 'Please Specify any search keyword'})
			return;
		}

		window.location = Flask.url_for('search_500px', {"keyword": keyword});
	};
	var search_flickr = function(){
		var keyword = $('#flickrsearch').val();

		if (keyword === ''){
			create_alert({'Error': 'Please Specify any search keyword'})
			return;
		}

		window.location = Flask.url_for('search_flickr', {"keyword": keyword});
	}
	$('#profile-picture').on('change', function(event){
		$('#preview').attr('src', URL.createObjectURL(event.target.files[0]));
		console.log(URL.createObjectURL(event.target.files[0]));
		frm = new FormData();
		frm.append('profile-picture', event.target.files[0]);
		// var preview = document.getElementById('preview');
		// preview.src = URL.createObjectURL(event.target.files[0]);
	});
	$('#certificate-submit').click(function(e){
		//$('#preview').attr('src', dns+ '/static/upload/' + $('#certified-to').val() + '.jpg');
		$('#certificate-div').removeAttr('style');
		$('#edit-button').removeAttr('style');
		$('#code-block').removeAttr('style');
		$('#description-form').attr('style', 'display: none;');
		$('#certified-name').text($('#certified-to').val());
		$('#certified-title').text($('#certification-title').val());
		console.log($('#certified-to').val());

		frm.append('name', $('#certified-to').val());
		frm.append('name', $('#certification-title').val());

		var code=`CSS:
.certificate-div {
    position: relative;
    width: 100%;
    padding-bottom: 55%;
}

.certificate-back {
    width: 100%;
    position: absolute;
}

.centered{
    position: absolute;
    top: 60%;
    left: 50%;
    width: 100%;
    transform: translate(-50%, -50%);
    text-align: center;
}

.preview {
    position: absolute;
    top: 30%;
    left: 80%;
    transform: translate(-50%, -50%);
    width: 20%;
    height: 40%;
    object-fit: cover; /* Do not scale the image */
    object-position: center; /* Center the image within the element */
    /*height: 200px;
    width: 200px;*/
}

HTML:
<div class="container">
	<div id="certificate-div" class="certificate-div">
	    <img class="certificate-back" src="` + dns + `/static/Certificate.png"/>
	    <img class="img-thumbnail preview" id="preview" src="` + dns + `/static/upload/` + $('#certified-to').val() +`.jpg">
	    <div class="centered">
	        <font color="white" size="5">Certified to</font><br/>
	        <font color="white" size="8">` + $('#certified-to').val() + `</font>
	        <font color="white" size="6">` + $('#certification-title').val() + `</font>
	    </div>
	</div>
</div>`;

		console.log(code);

		$.ajax({
	        method: 'POST',
	        url: Flask.url_for('save_file'),
	        data: frm,
	        contentType: false,
	        processData: false,
	        cache: false
	    });

		$('#code-preview').text(code);
	});

	var badge_no = "0";

    $("#badge-1").click(function(){ badge_no = "1"; $("#badge-title").html($("#badge-1").html()); console.log(badge_no);});
    $("#badge-2").click(function(){ badge_no = "2"; $("#badge-title").html($("#badge-2").html()); console.log(badge_no);});
    $("#badge-3").click(function(){ badge_no = "3"; $("#badge-title").html($("#badge-3").html()); console.log(badge_no);});
    $("#badge-4").click(function(){ badge_no = "4"; $("#badge-title").html($("#badge-4").html()); console.log(badge_no);});
    $("#badge-5").click(function(){ badge_no = "5"; $("#badge-title").html($("#badge-5").html()); console.log(badge_no);});
    $("#badge-6").click(function(){ badge_no = "6"; $("#badge-title").html($("#badge-6").html()); console.log(badge_no);});

    $("#badge-submit").click(function(){
        var badge_id = $("#badge-id").val();
        var badge_name = $("#badge-name").val();
        var badge_country = $("#badge-country").val();
        var badge_catagory = $("#badge-catagory").val();
        var badge_month = $("#badge-month").val();
        var badge_year = $("#badge-year").val();

        $.ajax({
            url: Flask.url_for('badge_info'),
            type: 'POST',
            data: {
                    "badge_id": badge_id,
                    "name": badge_name,
                    "title": badge_no,
                    "country": badge_country,
                    "catagory": badge_catagory,
                    "month": badge_month,
                    "year": badge_year
                },
            success: function(response){
                $.ajax({
	                url: dns + '/badge/' + badge_id,
	                type: 'GET',
	                success: function(response){
	                	console.log(response);
	                	info = response;
	                	var size = 300;
	                	var country_size = size/100; country_size = (size < 400 && info['country'].length > 8? country_size = country_size - 1: country_size);
	                	var catagory_size = size/100; catagory_size = (size < 400 && info['catagory'].length > 8? catagory_size = catagory_size - 1: catagory_size);
	                	var month_size = size/100; month_size = (size < 400 && info['month'].length > 8? month_size = month_size - 1: month_size);
	                	var year_size = size/100; year_size = (size < 400 && info['year'].length > 8? year_size = year_size - 1: year_size);

	                	$("#show-badge").empty();
	                	$("#show-badge").attr('style', 'float: left; position:relative;width:' + size + 'px; height:' + size + 'px; background-image: url(' + info['img'] + ');' + 'background-size: 100% 100%');

	                	var country_text = $('<p style="position:absolute;top:71%;left:50%; transform: translate(-50%,-50%);"><font face="Arial" size="' + country_size + 'px">' + info['country'] + '</font></p>');
	                	var catagory_text = $('<p style="position:absolute;top:79%;left:50%; transform: translate(-50%,-50%);"><font face="Arial" size="' + catagory_size + 'px">' + info['catagory'] + '</font></p>');
	                	var month_text = $('<p style="position:absolute;top:89%;left:50%; transform: translate(-50%,-50%);"><font face="Arial" size="' + month_size + 'px">' + info['month'] + '</font></p>');
	                	var year_text = $('<p style="position:absolute;top:95%;left:50%; transform: translate(-50%,-50%);"><font face="Arial" size="' + year_size + 'px">' + info['year'] + '</font></p>');
	                	$("#show-badge").append(country_text);
	                	$("#show-badge").append(catagory_text);
	                	$("#show-badge").append(month_text);
	                	$("#show-badge").append(year_text);

	                	$("#badge-code").text(
`
	<div>
		<iframe src="` + dns + `/getbadge/` + badge_id + `/200" style="height: 350px; width: 350px" frameborder="0"></iframe>
	</div>
`	           
	                	);

	                	$("#badge-code").attr('style', 'style="float: right;"');
	                },
	                error: function(err){
	                	console.log(err);
	                }
	            });
            },
            error: function(response){
                console.log(response);
            }
        });
    });

	$('#edit-form').click(function(){
		$('#certificate-div').attr('style', 'display: none');
		$('#edit-button').attr('style', 'display: none');
		$('#code-block').attr('style', 'display: none');
		$('#description-form').removeAttr('style');
	});
	$('#anti-clockwise').click(function(){
		rotate_frm = new FormData();
		rotate_frm.append('name', $('#certified-to').val());
		rotate_frm.append('angle', 90);
		$.ajax({
	        method: 'POST',
	        url: Flask.url_for('rotate'),
	        data: rotate_frm,
	        contentType: false,
	        processData: false,
	        cache: false
	    });
	    angle -= 90;
		$('#preview').attr('style', 'transform: rotate('+ (angle) +'deg);');
	});
	$('#clockwise').click(function(){
		rotate_frm = new FormData()
		rotate_frm.append('name', $('#certified-to').val())
		rotate_frm.append('angle', -90);
		$.ajax({
	        method: 'POST',
	        url: Flask.url_for('rotate'),
	        data: rotate_frm,
	        contentType: false,
	        processData: false,
	        cache: false
	    });
		angle += 90;
		$('#preview').attr('style', 'transform: rotate('+ (angle) +'deg);');
	});
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
	$('#facebooksearch').keypress(function(e){
		if (e.keyCode == 13){
			search_page();
		}
	});
	$('#500pxsearch').keypress(function(e){
		if (e.keyCode == 13){
			search_500px();
		}
	});
	$('#flickrsearch').keypress(function(e){
		if (e.keyCode == 13){
			search_flickr();
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
	});
	$("#add_facebookpage").click(function(e){
		if (selected_images.length === 0){
			create_alert({
				'Error': 'Please select facebook page(s) to pin to your dashboard!'
			});
			return ;
		}
		console.log(JSON.stringify(selected_images));

		$.ajax({
			url: Flask.url_for('add_page'),
			data: JSON.stringify({"pages": selected_images}),
			type: 'POST',
			success: function(response){
				window.location = Flask.url_for('dashboard');
			},
			error: function(response){
				console.log(response);
			}
		});
	});
	$("#add_500px").click(function(e){
		if (selected_images.length === 0){
			create_alert({
				'Error': 'Please select 500px user(s) to pin to your dashboard!'
			});
			return ;
		}
		console.log(JSON.stringify(selected_images));

		$.ajax({
			url: Flask.url_for('add_500px'),
			data: JSON.stringify({"users": selected_images}),
			type: 'POST',
			success: function(response){
				window.location = Flask.url_for('dashboard');
			},
			error: function(response){
				console.log(response);
			}
		});
	});
	$("#add_flickr").click(function(e){
		if (selected_images.length === 0){
			create_alert({
				'Error': 'Please select Flickr user(s) to pin to your dashboard!'
			});
			return;
		}

		$.ajax({
			url: Flask.url_for('add_flickr'),
			data: JSON.stringify({"flickr": selected_images}),
			type: 'POST',
			success: function(response){
				window.location = Flask.url_for('dashboard');
			},
			error: function(response){
				console.log(response);
			}
		});
	});
	$(".fancybox").fancybox({
        openEffect: "none",
        closeEffect: "none"
    });
});
