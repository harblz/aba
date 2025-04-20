const path = require("path");
delete require.cache[require.resolve("path")];
const webpack = require("webpack");

module.exports = {
  mode: "development",
  devtool: "source-map",
  optimization: {
    minimize: false, // Disable minification
  },
  entry: path.resolve(__dirname,"src/js/main.js"),
  target: "web",
  output: {
    path: path.resolve(__dirname, "staticfiles/js"),
    filename: "aba.js",
  },
  plugins: [
    new webpack.ProvidePlugin({
       htmx: 'htmx.org',
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
  }
};
