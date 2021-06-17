StarWars = (function() {

  /* 
   * Constructor
   */
  function StarWars(args) {
    // Context wrapper
    this.el = $(args.el);
    
    // Audio
    this.audio = this.el.find('audio').get(0);

    // Testo (lo nasconde all'inizio)
    this.testo = this.el.find('.fade').hide();
    this.testo2 = this.el.find('.crawl').hide();

    // Logo
    this.logo = this.el.find('.logo');




    // Start the animation on click
    this.logo.bind('click', $.proxy(function() {
      this.logo.hide();
      this.testo.show();
      this.testo2.show();
      this.audio.play();
    }, this));

  }
  


  return StarWars;
})();

new StarWars({
  el : '.starwars'
});




// ON LOAD
$( document ).ready(function() {
    console.log( "ready!" );
    $('.crawl').hide();

    // Quando finisce lo scroll del testo riappare il logo + link
    setTimeout(function() {
            $('.logo').show();
            $('.logo a').attr("href", "/home")
        }, 60000);

});

