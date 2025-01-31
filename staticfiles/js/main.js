import "htmx.org/dist/htmx";
import "htmx.org/dist/ext/debug.js";
import "htmx.org/dist/ext/response-targets";
import "htmx.org/dist/ext/alpine-morph.js";
import "htmx.org/dist/ext/head-support.js";

import Alpine from "alpinejs";
import morph from "@alpinejs/morph";
window.Alpine = Alpine;
Alpine.plugin(morph);
Alpine.start();
