/**
 * boxesFx.js v1.0.0
 * http://www.codrops.com
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Copyright 2014, Codrops
 * http://www.codrops.com
 */
;((window) => {
  'use strict';

  // based on http://responsejs.com/labs/dimensions/
  const getViewport = (axis) => {
    let client, inner;
    if (axis === 'x') {
      client = docElem['clientWidth'];
      inner = window['innerWidth'];
    } else if (axis === 'y') {
      client = docElem['clientHeight'];
      inner = window['innerHeight'];
    }
    return client < inner ? inner : client;
  };

  let docElem = window.document.documentElement,
    transEndEventNames = {
      'WebkitTransition': 'webkitTransitionEnd',
      'MozTransition': 'transitionend',
      'OTransition': 'oTransitionEnd',
      'msTransition': 'MSTransitionEnd',
      'transition': 'transitionend'
    },
    transEndEventName = transEndEventNames[Modernizr.prefixed('transition')],
    support = {transitions: Modernizr.csstransitions},
    win = {width: getViewport('x'), height: getViewport('y')};


  class BoxesFx {
    constructor (el) {
      this.el = el;
      this.auto = 0;
      this.automateInterval = 6000;
      this._init()
    };

    _init () {
      // set transforms configuration
      this._setTransforms();
      // which effect
      this.effect = this.el.getAttribute('data-effect') || 'effect-1';
      // check if animating
      this.isAnimating = false;
      // the panels
      this.panels = this.el.querySelectorAll('.panel');
      // total number of panels (4 for this demo)
      this.panelsCount = 16;
      // current panel´s index
      this.current = 0;
      classie.add(this.panels[0], 'current');
      // replace image with 4 divs, each including the image
      this.panels.forEach((panel) => {
        const img = panel.querySelector('img');
        let imgReplacement = '';
        for (let i = 0; i < this.panelsCount; ++i) {
          imgReplacement += '<div class="bg-tile"><div class="bg-img"><img src="' + img.src + '"  alt=""/></div></div>'
        }
        panel.removeChild(img);
        panel.innerHTML = imgReplacement + panel.innerHTML;
      }, this);
      // add navigation element
      this.nav = document.createElement('nav');
      this.nav.innerHTML = '<span class="prev"><i></i></span><span class="next"><i></i></span>';
      this.el.appendChild(this.nav);
      // initialize events
      this._initEvents();
    }

    // set the transforms per effect
    // we have defined both the next and previous action transforms for each panel
    _setTransforms () {
      this.transforms = {
        'effect-1-2': {
          'next': [
            `translate3d(0, ${win.height / 4 + 5}px, 0)`,
            `translate3d(-${win.width / 4 + 5}px, 0, 0)`,
            `translate3d(0, ${win.height / 4 + 5}px, 0)`,
            `translate3d(-${win.width / 4 + 5}px, 0, 0)`,

            `translate3d(${win.width / 4 + 5}px, 0, 0)`,
            `translate3d(0, -${win.height / 4 + 5}px, 0)`,
            `translate3d(${win.width / 4 + 5}px, 0, 0)`,
            `translate3d(0, -${win.height / 4 + 5}px, 0)`,

            `translate3d(0, ${win.height / 4 + 5}px, 0)`,
            `translate3d(-${win.width / 4 + 5}px, 0, 0)`,
            `translate3d(0, ${win.height / 4 + 5}px, 0)`,
            `translate3d(-${win.width / 4 + 5}px, 0, 0)`,

            `translate3d(${win.width / 4 + 5}px, 0, 0)`,
            `translate3d(0, -${win.height / 4 + 5}px, 0)`,
            `translate3d(${win.width / 4 + 5}px, 0, 0)`,
            `translate3d(0, -${win.height / 4 + 5}px, 0)`,
          ],
          'prev': [
            `translate3d(0, -${win.height / 4 + 5}px, 0)`,
            `translate3d(${win.width / 4 + 5}px, 0, 0)`,
            `translate3d(0, -${win.height / 4 + 5}px, 0)`,
            `translate3d(${win.width / 4 + 5}px, 0, 0)`,

            `translate3d(-${win.width / 4 + 5}px, 0, 0)`,
            `translate3d(0, ${win.height / 4 + 5}px, 0)`,
            `translate3d(-${win.width / 4 + 5}px, 0, 0)`,
            `translate3d(0, ${win.height / 4 + 5}px, 0)`,

            `translate3d(0, -${win.height / 4 + 5}px, 0)`,
            `translate3d(${win.width / 4 + 5}px, 0, 0)`,
            `translate3d(0, -${win.height / 4 + 5}px, 0)`,
            `translate3d(${win.width / 4 + 5}px, 0, 0)`,

            `translate3d(-${win.width / 4 + 5}px, 0, 0)`,
            `translate3d(0, ${win.height / 4 + 5}px, 0)`,
            `translate3d(-${win.width / 4 + 5}px, 0, 0)`,
            `translate3d(0, ${win.height / 4 + 5}px, 0)`,
          ]
        },
      };
    }

    _initEvents () {
      const navctrls = this.nav.children;
      // previous action
      navctrls[0].addEventListener('click', () => {
        this.automate('prev', this.automateInterval)
      });
      // next action
      navctrls[1].addEventListener('click', () => {
        this.automate('next', this.automateInterval)
      });
      // window resize
      window.addEventListener('resize', () => {
        this._resizeHandler();
      });
      window.onload = () => {
        this.automate('next', this.automateInterval)
      }
    }

    // goto next or previous slide
    _navigate (dir) {
      if (this.isAnimating) return false;
      this.isAnimating = true;

      const currentPanel = this.panels[this.current];

      if (dir === 'next') {
        this.current = this.current < this.panels.length - 1 ? this.current + 1 : 0;
      } else {
        this.current = this.current > 0 ? this.current - 1 : this.panels.length - 1;
      }

      // next panel to be shown
      const nextPanel = this.panels[this.current];
      // add class active to the next panel to trigger its animation
      classie.add(nextPanel, 'active');
      // apply the transforms to the current panel
      this._applyTransforms(currentPanel, dir);

      // let´s track the number of transitions ended per panel
      let cntTransTotal = 0;
      // transition end event function
      const onEndTransitionFn = (ev) => {
        if (ev && !classie.has(ev.target, 'bg-img')) return false;

        // return if not all panel transitions ended
        ++cntTransTotal;
        if (cntTransTotal < this.panelsCount) return false;

        if (support.transitions) {
          currentPanel.removeEventListener(transEndEventName, onEndTransitionFn);
        }

        // remove current class from current panel and add it to the next one
        classie.remove(currentPanel, 'current');
        classie.add(nextPanel, 'current');
        // reset transforms for the currentPanel
        this._resetTransforms(currentPanel);
        // remove class active
        classie.remove(nextPanel, 'active');
        this.isAnimating = false;
      };

      if (support.transitions) {
        currentPanel.addEventListener(transEndEventName, onEndTransitionFn);
      } else {
        onEndTransitionFn();
      }
    }

    _applyTransforms (panel, dir) {
      panel.querySelectorAll('div.bg-img').forEach((tile, pos) => {
        tile.style.WebkitTransform = this.transforms[this.effect][dir][pos];
        tile.style.transform = this.transforms[this.effect][dir][pos];
      });
    }

    _resetTransforms (panel) {
      panel.querySelectorAll('div.bg-img').forEach((tile) => {
        tile.style.WebkitTransform = 'none';
        tile.style.transform = 'none';
      });
    }

    _resizeHandler () {

      const delayed = () => {
        this._resize();
        this._resizeTimeout = null;
      };

      if (this._resizeTimeout) {
        clearTimeout(this._resizeTimeout);
      }
      this._resizeTimeout = setTimeout(delayed, 50);
    }

    _resize () {
      win.width = getViewport('x');
      win.height = getViewport('y');
      this._setTransforms();
    }

    automate (dir, time) {
      this.auto = setInterval(() => {
        this._navigate(dir)
      }, time)
    }

    Automate () {
      clearInterval(this.auto)
    }
  }

  // add to global namespace
  window.BoxesFx = BoxesFx;
})(window);
