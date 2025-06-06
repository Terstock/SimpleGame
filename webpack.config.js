const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const BrowserSyncPlugin = require('browser-sync-webpack-plugin');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'static/dist'),
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader'],
      },
      {
        test: /\.(png|jpe?g|gif|ico|svg)$/i,
        type: 'asset/resource',
        generator: {
          filename: 'img/[name][ext]',
        },
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({ filename: 'styles.css' }),
    new BrowserSyncPlugin(
      {
        proxy: 'localhost:5000',
        files: ['templates/*.html', 'static/dist/*.css', 'static/dist/*.js'],
        port: 3000,
        open: true,
      },
      { reload: true },
    ),
  ],
  mode: 'development',
  watch: true,
};
