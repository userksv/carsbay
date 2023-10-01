$("#id_make").change(function () {
    var url = $("#postForm").attr("data-models-url");  // get the url of the `load_models` view
    var makeId = $(this).val();  // get the selected make ID from the HTML input

    $.ajax({                       // initialize an AJAX request
      url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
      data: {
        'make': makeId       // add the make id to the GET parameters
      },
      success: function (data) {   // `data` is the return of the `load_models` view function
        console.log(data);
        $("#id_model").html(data);  // replace the contents of the city input with the data that came from the server
      }
    });

  });