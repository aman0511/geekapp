var availableTags = [];
$('document').ready(function () {
	var $loading = $('#spinner').hide();
	$(document)
		.ajaxStart(function () {
			$loading.show();
		})
		.ajaxStop(function () {
			$loading.hide();
		});
	$('[data-toggle=offcanvas]').click(function () {
		$('.row-offcanvas').toggleClass('active');
	});
	
	
});
var search = function (parameter,value){
	 console.log('hello');
	if(value){
		data={
          value: value,
          parameter: parameter
        }
   $.ajax({  
            url: '/search/page/' ,
            type: "POST",
            data: data,
            success: function(data) {
              console.log(data['html']);
              $("#result").html("");
              $("#result").html(data['html']);
            }
        
      });

  }
	
}


function person(url){
	console.log(url);
	$.ajax({  
            url:  url,
            type: "POST",
            data: data,
            success: function(data) {
				html=data;
              console.log(html['html']);
              $("#table").html("");
              $("#table").html(html['html']);
            }
        
      });
}

$('#searchbox').change(function(){
	search($('#search_param').val(), this.value);

});