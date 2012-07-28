$(document).ready(function() {
    // when the add to playlist form is submitted
    $("#playlistForm").submit(function(event){
        event.preventDefault();
        // if the user wants to create a new playlist
        if ( $('#playlist_id').val() == 'new_playlist' ) {
            $('#createPlaylistModal').modal('show'); // show the modal for new playlist creation
        } else { // otherwise, go through the add to playlist AJAX process
            $.ajax({
                type:"POST",
                url:"/videos/playlist/add/",
                data: {
                    // pass in current video id as well as playlist id to add video to
                    'video_id': $("#video_id").val(),
                    'playlist_id': $("#playlist_id").val()
                },
                success: function(data){ // upon success
                    if(data == 'Added') { // if video was added
                        $("#playlistButton").prop('value', 'Added to Playlist!');
                    } else if(data == 'Exists') { // if video already exists in playlist
                        $("#playlistButton").prop('value', 'Video already in playlist')
                    }
                }
            });
        }

    });
    // when the create new playlist form is submitted
    $("#createPlaylistForm").submit(function(event){
        event.preventDefault();
        $.ajax({ // send the necessary VideoPlaylist model form data to playlist creation view through AJAX
            type:"POST",
            url:"/videos/playlist/create/",
            data: {
                'title': $('#createPlaylistForm #id_title').val(),
            },
            success: function(data){ // upon success
                if(data) {
                    $('#createPlaylistModal').modal('hide'); // hide the modal form
                    $('#playlist_id').append(data); // append newly created playlist to list of options, selected
                }
            }
        });
    });
    // make sure the add to playlist button reverts to 'Add to Playlist' on each option change event
    $('#playlist_id').change(function(event){
        event.preventDefault();
        $("#playlistButton").prop('value', 'Add to Playlist');
    });
    return false;
});