"use strict";

import {getInput}  from "./controllers/takeInput.js";
import {navbarItems} from "./components/navbarItems.js";

$(function () {
   getInput();
   navbarItems();
});

