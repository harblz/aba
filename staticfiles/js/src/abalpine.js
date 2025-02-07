window.Alpine.store("themeSwitcher", {
  theme: window.Alpine.persist("auto").as("theme"),
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
  },
});
