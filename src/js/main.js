import "htmx-ext-response-targets/response-targets";
import "htmx-ext-alpine-morph/alpine-morph";
import "htmx-ext-head-support/head-support";

import Alpine from "alpinejs";
import morph from "@alpinejs/morph";
import persist from "@alpinejs/persist";
import collapse from "@alpinejs/collapse";

Alpine.plugin(morph);
Alpine.plugin(persist);
Alpine.plugin(collapse);

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
  },
  toggle() {
    if (this.theme === "auto") {
      if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
        this.theme = "light";
      } else if (window.matchMedia("(prefers-color-scheme: light)").matches) {
        this.theme = "dark";
      }
    }
    this.theme = this.theme === "dark" ? "light" : "dark";
  },
});

Alpine.store("extensions", {
  extensions: "response-targets alpine-morph head-support",
  init() {},
});

Alpine.store("showMenu", {
  show: false,
  init() {
    this.show = window.matchMedia("(min-width: 1024px)").matches;
    this.resizeToggle();
  },
  toggle() {
    this.show = !this.show;
  },
  resizeToggle() {
    addEventListener("resize", () => {
      this.show = window.matchMedia("(min-width: 1024px)").matches;
    });
  },
});

Alpine.bind("burger", {
  cross: false,
  "@click"() {
    this.cross = !this.cross;
  },
  ":class"() {
    return this.cross ? "is-active" : "";
  },
});

Alpine.data("cards", () => ({
  front: "",
  back: "",
  currentIndex: 0,
  total: 0,
  deck: [],
  init() {
    try {
      this.deck = JSON.parse(
        JSON.parse(document.getElementById("cards").textContent),
      );
    } catch {
      this.deck = [];
    }
    this.total = this.deck.length;
    const card = this.deck[0] || {};
    this.current = 1;
    this.front = card.front || "";
    this.back = card.back || "";
  },
  frontside(ogtext) {
    return ogtext || this.front;
  },
  backside(ogtext) {
    return ogtext || this.back;
  },
  nextCard() {
    this.current += 1;
    const card = this.deck[this.current];
    this.front = card.front;
    this.back = card.back;
  },
}));

Alpine.start();
