$(document).ready(function(){
   $('.next').on('click', function(){
       console.log('clicked');
       var currentImg = $('.active');
       var nextImg = currentImg.next();
       
       if(nextImg.length){
           currentImg.removeClass('active').css('z-index', -10);
           nextImg.addClass('active').css('z-index',10);
       }
   });
});