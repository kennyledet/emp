$(document).ready(function() {
    // when the favorite button has been submitted
    $("#favoriteForm").submit(function(event){
        event.preventDefault();
        $.ajax({ // pass in the necessary data to favorite_video view through AJAX
            type:"POST",
            url:"/videos/favorite/",
            data: {
            	'video_id': $("#video_id").val(),
            	'fav_type': $("#favoriteButton").val()
            },
            success: function(data){
            	if(data == 'Added') { // if video successfully added to user's favorites 
            		$("#favoriteButton").prop('value', 'Remove from Favorites'); // change button val to allow reversal
            	} else { // if video removed from favorites
            		$("#favoriteButton").prop('value', 'Add to Favorites'); // change button val to allow reversal
		        }
            }
        });
    });
    return false;
});