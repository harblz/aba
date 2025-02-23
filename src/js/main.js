import "htmx-ext-response-targets/response-targets";
import "htmx-ext-alpine-morph/alpine-morph";
import "htmx-ext-head-support/head-support";

import Alpine from "alpinejs";
import morph from "@alpinejs/morph";
import persist from "@alpinejs/persist";

Alpine.plugin(morph);
Alpine.plugin(persist);

window.alpine = Alpine;

Alpine.store("themeSwitcher", {
  theme: window.alpine.$persist("auto").as("theme"),
  init() {
    if (
      window.matchMedia("(prefers-color-scheme: dark)").matches ||
      window.matchMedia("(prefers-color-scheme: light)").matches
    ) {
      this.theme = "auto";
    } else {
      this.theme = "dark";
    }
    console.log("initialized successfully");
  },
  toggle() {
    this.theme = this.theme === "dark" ? "light" : "dark";
  }
});

Alpine.store("extensions", {
  extensions: "response-targets alpine-morph head-support",
  init() {
  }
});

Alpine.start();