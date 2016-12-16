$.fn.editable.defaults.mode = 'inline';
//get rid of buttons
$.fn.editableform.buttons = '';       

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
// var mangas = null;
// $.ajax({
//   type: "GET",
//   url: "/manga/list/",
//   cache: false,
//   //pass the button as the context for ajax callback methods
//   context: this,
//   success: function (html) {
//     mangas = html.split("\n");
//     console.log("returned manga list",mangas);
//   }
// })

$(document).ready(function() {
  $('.bookmark_release').editable();

  $(".bookmark_button").click(function () {
    var tr = $(this).closest('tr');
    var location = "/bookmark/";
    $.ajax({
      type: "DELETE",
      url: location,
      data: tr.attr('id'),
      cache: false,
      //pass the button as the context for ajax callback methods
      context: this,
      success: function (html) {
        //find the tr in which the clicked button belongs to and delete it
        tr.remove()
      }
    });
  });

  // $('#id_multiple_manga').select2({
  //   sorter: function(results) {
  //     console.log("select2",results);
  //     return results.sort(function(a, b) {
  //       if (a.text > b.text) {
  //         return 1;
  //       } else if (a.text < b.text) {
  //         return -1;
  //       } else {
  //         return 0;
  //       }
  //     });
  //   }
  // });

});