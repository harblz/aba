const path = require("path");

module.exports = {
  entry: "./staticfiles/js/main.js",
  output: {
    filename: "aba.js",
    path: path.resolve(__dirname, "./staticfiles/js"),
  },
  module: {},
};
