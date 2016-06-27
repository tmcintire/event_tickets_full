$(function() {
    $( ".datepicker" ).datepicker({
      changeMonth: true,
      changeYear: true,
      yearRange: "1900:2017",
      // You can put more options here.

    });
});


$(".add-btn").click(function() {
    typeid = $(this).attr("data-typeid");
    $.get('/event/admission/{{ name.id }}/addone/' + typeid, { admission_type: typeid }, function(data) {
        console.log(data['attendance'])
        console.log(data['count'])
        $('#count-' + typeid).html(data['count']);
        $('#total-' + typeid).html("$" + data['total']);
        $('#attendance').html(data['attendance']);
    });
});

$(".delete-btn").click(function() {
    typeid = $(this).attr("data-typeid");

    $.confirm({
        text: "You are about to remove an entry. Are you sure?",
        title: "Confirmation required",
        confirm: function(button) {
            $.get('/event/admission/{{ name.id }}/deleteone/' + typeid, {
                admission_type: typeid
            }, function(data) {
                $('#count-' + typeid).html(data['count']);
                $('#total-' + typeid).html("$" + data['total']);
            });
        },
    });
});