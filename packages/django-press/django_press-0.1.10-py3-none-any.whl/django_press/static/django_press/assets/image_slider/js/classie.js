/*!
 * classie - class helper functions
 * from bonzo https://github.com/ded/bonzo
 * 
 * classie.has( elem, 'my-class' ) -> true/false
 * classie.add( elem, 'my-new-class' )
 * classie.remove( elem, 'my-unwanted-class' )
 * classie.toggle( elem, 'my-class' )
 */

/*jshint browser: true, strict: true, undef: true */
/*global define: false */

(function (window) {
  'use strict';
  // class helper functions from bonzo https://github.com/ded/bonzo

  const classReg = (className) => {
    return new RegExp("(^|\\s+)" + className + "(\\s+|$)");
  };

  // classList support for class management
  // altho to be fair, the api sucks because it won't accept multiple classes at once
  let hasClass, addClass, removeClass;

  if ('classList' in document.documentElement) {
    hasClass = (elem, c) => {
      return elem.classList.contains(c);
    };
    addClass = (elem, c) => {
      elem.classList.add(c);
    };
    removeClass = (elem, c) => {
      elem.classList.remove(c);
    };
  } else {
    hasClass = (elem, c) => {
      return classReg(c).test(elem.className);
    };
    addClass = (elem, c) => {
      if (!hasClass(elem, c)) {
        elem.className = elem.className + ' ' + c;
      }
    };
    removeClass = (elem, c) => {
      elem.className = elem.className.replace(classReg(c), ' ');
    };
  }

  const toggleClass = (elem, c) => {
    const fn = hasClass(elem, c) ? removeClass : addClass;
    fn(elem, c);
  };

  const classie = {
    // full names
    hasClass: hasClass,
    addClass: addClass,
    removeClass: removeClass,
    toggleClass: toggleClass,
    // short names
    has: hasClass,
    add: addClass,
    remove: removeClass,
    toggle: toggleClass
  };

// transport
  if (typeof define === 'function' && define.amd) {
    // AMD
    define(classie);
  } else {
    // browser global
    window.classie = classie;
  }

})(window);
