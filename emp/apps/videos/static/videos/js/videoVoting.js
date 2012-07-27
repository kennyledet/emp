// pass like/dislike up/downvote to Django-voting generic view '/videos/vote/object_id/up|down|clear'
$(document).ready(function() {
    $('.vote-btn').click(function(event) {
        $.ajax({
          url: '/videos/vote/' + $('#video_id').val() + '/' + $(this).val(),
          type: 'POST',
          //data: {param1: 'value1'},
          complete: function(xhr, textStatus) {
            //called when complete
          },
          success: function(data, textStatus, xhr) {
            //called when successful
          },
          error: function(xhr, textStatus, errorThrown) {
            //called when there is an error
          }
        });
        
    });
});
