$('document').ready(function () {
	var $loading = $('#spinner').hide();
	$(document)
		.ajaxStart(function () {
			$loading.show();
		})
		.ajaxStop(function () {
			$loading.hide();
		});
  $('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
  });
	var availableTags = [ "ActionScript",
      "AppleScript",
      "Asp",
      "BASIC",
      "C",
      "C++",
      "Clojure",
      "COBOL",
      "ColdFusion",
      "Erlang",
      "Fortran",
      "Groovy",
      "Haskell",
      "Java",
      "JavaScript",
      "Lisp",
      "Perl",
      "PHP",
      "Python",
      "Ruby",
      "Scala",
      "Scheme"
    ];
	$("#searchbox").autocomplete({
		source: availableTags
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
              console.log(data);
              }
        
      });

  }
	
}

$('#searchbox').change(function(){
	search($('#search_param').val(), this.value);
});