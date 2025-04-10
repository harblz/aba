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

Alpine.store("cardData", {
  deck: [],
  current: 0,
  total: 0,
  correct: 0,
  incorrect: 0,
  init() {
    if (document.getElementById("card-data")) {
      this.deck = JSON.parse(
        JSON.parse(document.getElementById("card-data").textContent),
      );
      this.total = this.deck.length;
      this.current = 1;
    } else {
      this.deck = null;
    }
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
    console.log("Results");
    console.log("Correct: " + this.correct);
    console.log("Incorrect: " + this.incorrect);
    const score = this.correct / this.total;
    console.log("Score: " + score);
    console.log("Thanks for Playing!");
  }
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
    this.alpine = window.alpine.$data("useAlpine");
    this.button = window.alpine.$data("showButton");
    if (this.alpine) {
      this.index = this.cardData.current;
      this.front = this.cardData.front;
      this.back = this.cardData.back;
    }
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

Alpine.start();
