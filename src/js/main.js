import "./htmx.js";
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

window.Alpine = Alpine;

Alpine.store("themeSwitcher", {
  theme: Alpine.$persist("auto"),
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
    } else {
      this.theme = (this.theme === "dark" ? "light" : "dark");
    }
  },
});

Alpine.store("responsiveNav", {
  show: false,
  top: false,
  init() {
    this.show = this.top = window.matchMedia("(min-width: 1024px)").matches;
    this.resizeToggle();
  },
  toggle() {
    this.show = !this.show;
  },
  resizeToggle() {
    addEventListener("resize", () => {
      this.show = this.top = window.matchMedia("(min-width: 1024px)").matches;
    });
  },
});

Alpine.bind("burger", () => ({
  cross: false,
  "@click"() {
    this.cross = !this.cross;
  },
  ":class"() {
    return this.cross ? "is-active" : "";
  },
}));

Alpine.store("cardData", {
  deck: [],
  current: 0,
  total: 0,
  correct: 0,
  incorrect: 0,
  init() {
    if (document.getElementById("card-data")) {
      this.deck = JSON.parse(
        JSON.parse(document.getElementById("card-data").textContent)
      );
      this.current = 1;
      this.total = this.deck.length;
    } else {
      this.deck = null;
    }
  },
  get id() {
    return this.deck[this.current - 1].id;
  },
  get front() {
    return this.deck[this.current - 1].front;
  },
  get back() {
    return this.deck[this.current - 1].back;
  },
  next() {
    this.current += 1;
  },
  get score() {
    window.htmx.trigger("#play-section", "score", {
      name: document.title,
      correct: this.correct,
      incorrect: this.incorrect,
      total: this.total,
    });
  },
});

Alpine.data("card", () => ({
  cardData: Alpine.store("cardData"),
  index: 0,
  flip: false,
  button: false,
  id: "",
  front: "",
  back: "",
  init() {
    if (Alpine.$data("skipInit") === true) {
      //pass
    } else {
      this.button = Alpine.$data("showButton");
      this.id = this.cardData.id;
      this.index = this.cardData.current;
      this.front = this.cardData.front;
      this.back = this.cardData.back;
    }
  },
  cardid(ogid){
    return ogid || this.id;
  },
  frontside(ogtext) {
    return ogtext || this.front;
  },
  backside(ogtext) {
    return ogtext || this.back;
  },
  nextCard() {
    if (this.cardData.current === this.cardData.total) {
      this.cardData.score();
    } else {
      this.cardData.next();
      this.front = this.cardData.front;
      this.back = this.cardData.back;
    }
  },
}));
Alpine.data("dropdown", () => ({
  show: false,
  init() {},
  toggle() {
    this.show = !this.show;
  },
}));
window.processHeaders = () => {
  let element = document.getElementById('headers');
  if (element) {
    return JSON.parse(element.textContent);
  }
  else {
    return {};
  }
};

Alpine.start();
