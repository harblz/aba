import "htmx-ext-debug/debug";
import "htmx-ext-response-targets/response-targets";
import "htmx-ext-alpine-morph/alpine-morph";
import "htmx-ext-head-support/head-support";

import Alpine from "alpinejs";
import morph from "@alpinejs/morph";
window.Alpine = Alpine;
Alpine.plugin(morph);
Alpine.start();
