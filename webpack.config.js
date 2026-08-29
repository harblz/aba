const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: {
    "entry" : path.resolve(__dirname,"src/js/entry.js"),
    "chart" : path.resolve(__dirname,"src/js/chart.js"),
  },
  target: "web",
  output: {
    path: path.resolve(__dirname, "staticfiles/js"),
    filename: "[name].js",
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

