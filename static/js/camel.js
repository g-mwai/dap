//===== Camel animation ==== //

//IIFE
(function($,TweenMax) {

    // wait for document ready
    $(function() {

        // selectors
        var master =  new TimelineMax(), //my master time line
            head = $('#Head'),
            straw = $('#straw'),
            earLeft = $('.Ear-left'),
            earRight = $('.Ear-right'),
            eye = $('.eye'),
            eyeWhite = $('.eye-white'),
            eyeOrange = $('.eye-orange'),
            nose = $('#nose'),
            upperMouth = $('#upper-mouth'),
            lowerMouth = $('#lower-mouth'),
            neck = $('#neck')
        ;


        // do not apply animation if on mobile (for better performance)
        if( !/Android|webOS|iPhone|iPod|iPad|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)  &&  $(window).width() >= 768) {


          // All animations on time line//===== Camel animation ==== //

          //IIFE
          (function($, TweenMax) {
            // wait for document ready
            $(function() {
              // selectors
              var master = new TimelineMax(), //my master time line
                  head = $("#Head"),
                  straw = $("#straw"),
                  earLeft = $(".Ear-left"),
                  earRight = $(".Ear-right"),
                  eye = $(".eye"),
                  eyeWhite = $(".eye-white"),
                  eyeOrange = $(".eye-orange"),
                  nose = $("#nose"),
                  upperMouth = $("#upper-mouth"),
                  lowerMouth = $("#lower-mouth"),
                  neck = $("#neck");

              // do not apply animation if on mobile (for better performance)
              if (
                !/Android|webOS|iPhone|iPod|iPad|BlackBerry|IEMobile|Opera Mini/i.test(
                  navigator.userAgent
                ) &&
                $(window).width() >= 768
              ) {
                // All animations on time line
                master
                  .add(headAnimation())
                  .add(eyeBlinkAnimation(), 0)
                  .add(MouthAnimation(), 0)
                  .add(strawAnimation(), 0)
                  .add(earsAnimation(), 0)
                  .add(neckAnimation(), 0);

                // Head Animation
                function headAnimation() {
                  var tl = new TimelineMax();
                  tl.to(
                    head,
                    0.7,
                    { y: "+=6", ease: Power1.easeInOut, repeat: -1, yoyo: true },
                    0
                  );
                  return tl;
                }

                // eye blink Animation
                function eyeBlinkAnimation() {
                  var tl = new TimelineMax({ repeat: -1, repeatDelay: 4 });
                  tl
                    .to(
                    eyeOrange,
                    0.6,
                    {
                      rotationX: 180,
                      transformOrigin: "50% 50%",
                      ease: Power1.easeInOut
                    },
                    0
                  )
                    .to(
                    eyeWhite,
                    0.23,
                    {
                      y: "-=3",
                      scale: 0.85,
                      transformOrigin: "50% 0",
                      ease: Power1.easeInOut,
                      repeat: 1,
                      yoyo: true
                    },
                    0
                  )
                    .to(
                    eye,
                    0.23,
                    { y: "+=6", ease: Power1.easeInOut, repeat: 1, yoyo: true },
                    0
                  );
                  return tl;
                }

                // mouth Animation
                function MouthAnimation() {
                  var tl = new TimelineMax();
                  tl
                    .to(
                    lowerMouth,
                    1.5,
                    {
                      bezier: {
                        type: "quadratic",
                        values: [
                          { x: 0, y: 0 },
                          { x: 4, y: 0 },
                          { x: 7, y: 4 },
                          { x: 10, y: 6 },
                          { x: 0, y: 6 },
                          { x: -4, y: 6 },
                          { x: -5, y: 4 },
                          { x: -4, y: 0 },
                          { x: 0, y: 0 }
                        ]
                      },
                      ease: Power1.easeInOut,
                      repeat: -1
                    },
                    0
                  )
                    .to(
                    lowerMouth,
                    0.74,
                    {
                      rotation: "-=10",
                      transformOrigin: "50% 50%",
                      ease: Power1.easeInOut,
                      yoyo: true,
                      repeat: -1
                    },
                    0
                  )
                    .to(
                    upperMouth,
                    1.5,
                    {
                      bezier: {
                        type: "quadratic",
                        values: [
                          { x: 0, y: 0 },
                          { x: 1, y: 0 },
                          { x: 1, y: 1 },
                          { x: 1, y: 3 },
                          { x: 0, y: 3 },
                          { x: -1, y: 3 },
                          { x: -1, y: 1 },
                          { x: -1, y: 0 },
                          { x: 0, y: 0 }
                        ]
                      },
                      ease: Power1.easeInOut,
                      repeat: -1
                    },
                    0
                  )
                    .to(
                    nose,
                    0.74,
                    { y: "+=3", ease: Power1.easeInOut, repeat: -1, yoyo: true },
                    0
                  );
                  return tl;
                }

                // Straw Animation
                function strawAnimation() {
                  var tl = new TimelineMax();
                  tl
                    .to(
                    straw,
                    1.5,
                    {
                      bezier: {
                        type: "quadratic",
                        values: [
                          { x: 0, y: 0 },
                          { x: 4, y: 0 },
                          { x: 4, y: 4 },
                          { x: 4, y: 8 },
                          { x: 0, y: 8 },
                          { x: -4, y: 8 },
                          { x: -4, y: 4 },
                          { x: -4, y: 0 },
                          { x: 0, y: 0 }
                        ]
                      },
                      ease: Power1.easeInOut,
                      repeat: -1
                    },
                    0
                  )
                    .to(
                    straw,
                    0.5,
                    {
                      rotation: "-=20",
                      transformOrigin: "100% 0",
                      ease: Power1.easeInOut,
                      yoyo: true,
                      repeat: -1,
                      repeatDelay: 0.25
                    },
                    0
                  );
                  return tl;
                }

                // ears Animation
                function earsAnimation() {
                  var tl = new TimelineMax({});
                  tl
                    .to(
                    earRight,
                    0.7,
                    {
                      rotation: "+=7",
                      transformOrigin: "0 100%",
                      ease: Power1.easeInOut,
                      yoyo: true,
                      repeat: -1
                    },
                    0.2
                  )
                    .to(
                    earLeft,
                    0.7,
                    {
                      rotation: "-=7",
                      transformOrigin: "100% 100%",
                      ease: Power1.easeInOut,
                      yoyo: true,
                      repeat: -1
                    },
                    0.2
                  );
                  return tl;
                }

                // neck Animation
                function neckAnimation() {
                  var tl = new TimelineMax({ yoyo: true, repeat: -1 });
                  tl.fromTo(
                    neck,
                    3,
                    { rotation: "-=2", transformOrigin: "50% 100%" },
                    {
                      rotation: "+=4",
                      transformOrigin: "50% 100%",
                      ease: Power1.easeInOut
                    },
                    0.2
                  );
                  return tl;
                }
              }
            });
          })(jQuery, TweenMax);

            master
                .add(headAnimation())
                .add(eyeBlinkAnimation(), 0)
                .add(MouthAnimation(), 0)
                .add(strawAnimation(),0)
                .add(earsAnimation(),0)
                .add(neckAnimation(),0)
            ;


            // Head Animation
            function headAnimation() {
                var tl = new TimelineMax();
                    tl.to(head, .7, { y:'+=6',ease: Power1.easeInOut, repeat: -1, yoyo: true }, 0)
                ;
                return tl;
            }


            // eye blink Animation
            function eyeBlinkAnimation() {
                var tl = new TimelineMax({repeat: -1, repeatDelay:4});
                tl.to(eyeOrange, .6, {rotationX:180,transformOrigin:"50% 50%",ease: Power1.easeInOut}, 0)
                  .to(eyeWhite,.23,{ y:'-=3',scale:.85,transformOrigin:"50% 0",ease: Power1.easeInOut, repeat: 1, yoyo: true },0)
                  .to(eye,.23,{ y:'+=6',ease: Power1.easeInOut, repeat: 1, yoyo: true },0)
                ;
                return tl;
            }


            // mouth Animation
            function MouthAnimation() {
                var tl = new TimelineMax();
                tl
                    .to(lowerMouth,1.5, { bezier:{ type:'quadratic', values:[ {x:0, y:0}, {x:4, y:0}, {x:7, y:4}, {x:10, y:6}, {x:0, y:6}, {x:-4, y:6}, {x:-5, y:4}, {x:-4, y:0},{x:0, y:0} ] },ease: Power1.easeInOut, repeat: -1},0)
                    .to(lowerMouth,.74, {rotation:'-=10',transformOrigin:"50% 50%",ease: Power1.easeInOut, yoyo:true, repeat: -1},0)
                    .to(upperMouth,1.5, { bezier:{type:'quadratic', values:[ {x:0, y:0}, {x:1, y:0}, {x:1, y:1}, {x:1, y:3}, {x:0, y:3}, {x:-1, y:3}, {x:-1, y:1}, {x:-1, y:0},{x:0, y:0} ] },ease: Power1.easeInOut, repeat: -1},0)
                    .to(nose,.74,{ y:'+=3',ease: Power1.easeInOut, repeat: -1, yoyo: true },0)
                ;
                return tl;
            }


            // Straw Animation
            function strawAnimation() {
                var tl = new TimelineMax();
                tl
                    .to(straw,1.5, { bezier:{ type:'quadratic', values:[ {x:0, y:0}, {x:4, y:0}, {x:4, y:4}, {x:4, y:8}, {x:0, y:8}, {x:-4, y:8}, {x:-4, y:4}, {x:-4, y:0},{x:0, y:0} ] },ease: Power1.easeInOut, repeat: -1},0)
                    .to(straw,.5, {rotation:'-=20',transformOrigin:"100% 0",ease: Power1.easeInOut, yoyo:true, repeat: -1, repeatDelay:.25},0)
                ;
                return tl;
            }


            // ears Animation
            function earsAnimation() {
                var tl = new TimelineMax({});
                tl
                    .to(earRight,.7, {rotation:'+=7',transformOrigin:"0 100%",ease: Power1.easeInOut, yoyo:true, repeat: -1},.2)
                    .to(earLeft,.7, {rotation:'-=7',transformOrigin:"100% 100%",ease: Power1.easeInOut, yoyo:true, repeat: -1},.2)
                ;
                return tl;
            }


            // neck Animation
            function neckAnimation() {
                var tl = new TimelineMax({ yoyo:true, repeat: -1});
                tl
                    .fromTo(neck,3, {rotation:'-=2',transformOrigin:"50% 100%"},{rotation:'+=4',transformOrigin:"50% 100%",ease: Power1.easeInOut},.2)
                ;
                return tl;
            }

        }

    });


})(jQuery,TweenMax);















