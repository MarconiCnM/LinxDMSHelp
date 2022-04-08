$('#recipeCarousel').carousel({
    interval: 10000
    })

$('.carousel .carousel-item').each(function(){
    var minPerSlide = 5;
    var next = $(this).next();
    if (!next.length) {
    next = $(this).siblings(':first');
    }

    next.children(':first-child').clone().appendTo($(this));
    
    for (var i=0;i<minPerSlide;i++) {
        next=next.next();
        if (!next.length) {
            next = $(this).siblings(':first');
        }
        
        next.children(':first-child').clone().appendTo($(this));
    }
});

jQuery(document).ready(function($) {
   var bsDefaults = {
         offset: false,
         overlay: true,
         width: '300px'
      },
      bsMain = $('.bs-offset-main'),
      bsOverlay = $('.bs-canvas-overlay');

   $('[data-toggle="canvas"][aria-expanded="false"]').on('click', function() {
      var canvas = $(this).data('target'),
         opts = $.extend({}, bsDefaults, $(canvas).data()),
         prop = $(canvas).hasClass('bs-canvas-right') ? 'margin-right' : 'margin-left';

      if (opts.width === '100%')
         opts.offset = false;
      
      $(canvas).css('width', opts.width);
      if (opts.offset && bsMain.length)
         bsMain.css(prop, opts.width);

      $(canvas + ' .bs-canvas-close').attr('aria-expanded', "true");
      $('[data-toggle="canvas"][data-target="' + canvas + '"]').attr('aria-expanded', "true");
      if (opts.overlay && bsOverlay.length)
         bsOverlay.addClass('show');
      return false;
   });

   $('.bs-canvas-close, .bs-canvas-overlay').on('click', function() {
      var canvas, aria;
      if ($(this).hasClass('bs-canvas-close')) {
         canvas = $(this).closest('.bs-canvas');
         aria = $(this).add($('[data-toggle="canvas"][data-target="#' + canvas.attr('id') + '"]'));
         if (bsMain.length)
            bsMain.css(($(canvas).hasClass('bs-canvas-right') ? 'margin-right' : 'margin-left'), '');
      } else {
         canvas = $('.bs-canvas');
         aria = $('.bs-canvas-close, [data-toggle="canvas"]');
         if (bsMain.length)
            bsMain.css({
               'margin-left': '',
               'margin-right': ''
            });
      }
      canvas.css('width', '');
      aria.attr('aria-expanded', "false");
      if (bsOverlay.length)
         bsOverlay.removeClass('show');
      return false;
   });
});

var analise = document.getElementsByClassName("analise-btn");
var i;

for (i = 0; i < analise.length; i++) {
  analise[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var analiseContent = this.nextElementSibling;
    if (analiseContent.style.display === "block") {
      analiseContent.style.display = "none";
    } else {
      analiseContent.style.display = "block";
    }
  });
}

var treinamento = document.getElementsByClassName("treinamento-btn");
var i;

for (i = 0; i < treinamento.length; i++) {
  treinamento[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var treinamentoContent = this.nextElementSibling;
    if (treinamentoContent.style.display === "block") {
      treinamentoContent.style.display = "none";
    } else {
      treinamentoContent.style.display = "block";
    }
  });
}

var ferramentas = document.getElementsByClassName("ferramentas-btn");
var i;

for (i = 0; i < ferramentas.length; i++) {
  ferramentas[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var ferramentasContent = this.nextElementSibling;
    if (ferramentasContent.style.display === "block") {
      ferramentasContent.style.display = "none";
    } else {
      ferramentasContent.style.display = "block";
    }
  });
}

var cadastro = document.getElementsByClassName("cad-btn");
var i;

for (i = 0; i < cadastro.length; i++) {
  cadastro[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var cadastroContent = this.nextElementSibling;
    if (cadastroContent.style.display === "block") {
      cadastroContent.style.display = "none";
    } else {
      cadastroContent.style.display = "block";
    }
  });
}


var externos = document.getElementsByClassName("externos-btn");
var i;

for (i = 0; i < externos.length; i++) {
  externos[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var externosContent = this.nextElementSibling;
    if (externosContent.style.display === "block") {
      externosContent.style.display = "none";
    } else {
      externosContent.style.display = "block";
    }
  });
}

