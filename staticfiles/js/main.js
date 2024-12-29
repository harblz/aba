import "./htmx.js";
import "htmx.org/dist/ext/debug.js";
import "htmx.org/dist/ext/response-targets";
import "htmx.org/dist/ext/alpine-morph.js";
import "htmx.org/dist/ext/head-support.js";

import Alpine from "alpinejs";
window.Alpine = Alpine;
Alpine.start();
