"use strict";

import { home } from './../views/home.js';
import { searchInIris } from './controllers/apicalls.js';
import { error }  from './../views/error.js';

const router = async () => {

   var pathName = window.location.pathname;
   
   if(pathName === '/'){
      const params = new URLSearchParams(window.location.search);
      
      // no results
      if(!params.has("q")){
         // load the page with no results
         home(params);
      }

      // show results
      else{
         // load as per params
         searchInIris(params);
      }
   }

   // 404
   else{
      error();
   }
}

$(function () {
   router();   
});

$(window).on('popstate', router);
