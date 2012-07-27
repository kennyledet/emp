$(".slideshow").each(function() {
  $(this).find(".slides").cycle({
      fx:     'fade',
      speed:   .3,
      timeout: 280,
      next:   '#next',
      prev:   '#prev'
  }).cycle("pause").end().hover(
      function() { $(this).find('.slides').cycle('resume'); },
      function() { $(this).find('.slides').cycle('pause'); }
  );
});
// enable relative video link (on click) to video thumbnail slideshow
$('.slides img').click(function (){
  document.location.href = $(this).attr('rel');
}).css('cursor', 'pointer');
