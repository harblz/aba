const path = require("path");
const webpack = require("webpack");

module.exports = {
    mode: "production",
    entry: "./src/main.js",
    target: "web",
    output: {
        path: path.resolve(__dirname, "staticfiles/js"),
        filename: "aba.js"
    },
    plugins: [
        new webpack.ProvidePlugin({
            htmx: "htmx.org"
        })
    ]
};
