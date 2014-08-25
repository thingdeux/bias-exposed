$(document).ready(function() {  
	not_relevants = $('.not-relevant-action')

	not_relevants.click(function(event) {
		wordDetailID = $(event.currentTarget).attr('data-word-id');
		$.ajax ({
			type: "POST",
			url: "/analyze/worddelete",
			data: { worddetail: wordDetailID },
			success: function() {
    			$(event.target).html("Deleted");
    			$(event.target).addClass('label-success');
    			$(event.target).removeClass('label-danger');
  			},
  			error: function() {
    			$(event.target).html("Not Deleted")
  			}
		});
	});
});