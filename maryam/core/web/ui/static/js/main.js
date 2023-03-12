"use strict";

import { home } from './../views/home.js';
import { results } from './../views/results.js'
import { error }  from './../views/error.js';

import { getInput } from './controllers/takeInput.js';
import { navbarItems } from './components/navbarItems.js'

const router = async () => {

   var pathName = window.location.pathname;
   
   if(pathName === '/'){
      const params = new URLSearchParams(window.location.search);
      const paramsLength = Array.from(params).length;
      
      // no results
      if(paramsLength === 0){
         // load the page with no results
         $('#root').html(home);
         getInput();
      }

      // show results
      else{
         // load as per params
         $('#root').html(results(params));
         getInput();
         navbarItems();
      }
   }

   // 404
   else{
      // render the 404 page;
      $('#root').html(error());
   }
}

$(function () {
   router();   
});

$(window).on('popstate', router);
