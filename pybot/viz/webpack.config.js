const HtmlWebpackPlugin = require("html-webpack-plugin");
const path = require("path");

module.exports = {
  plugins: [
    new HtmlWebpackPlugin({
      template: path.resolve(__dirname, "src", "index.html")
    })
  ],
  devServer: {
    proxy: {
      'ws://localhost:8080/ws': {
         target: 'ws://localhost:3000',
         ws: true
      },
    },
  }
};
