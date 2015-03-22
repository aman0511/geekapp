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
				for(key in html){
					$('#table-'+key).html("");
					$('#table-'+key).html(html[key]);
				}
            }
        
      });
}

$('#searchbox').change(function(){
	search($('#search_param').val(), this.value);

});