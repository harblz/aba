const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: path.resolve(__dirname,"src/js/entry.js"),
  target: "web",
  output: {
    path: path.resolve(__dirname, "staticfiles/js"),
    filename: "aba.js",
  },
  plugins: [
    new webpack.ProvidePlugin({
      htmx: 'htmx.org',
      process: "process/browser",
    }),
    new webpack.ProvidePlugin({
      process: "process/browser",
    }),
  ],
  infrastructureLogging: {
    level: "verbose",
  },
  resolve: {
    extensions: ['.ts', '.js'],
    alias: {
      'htmx.org$': require.resolve('htmx.org/dist/htmx.js')
    }
  }
};

