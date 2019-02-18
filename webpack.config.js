const webpack = require('webpack');

module.exports = {
  entry: './projectQ/web/App.jsx',
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },
  output: {
    path: __dirname + '/projectQ/server/static',
    publicPath: '/',
    filename: 'bundle.js'
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin()
  ],
  devServer: {
    publicPath: 'http://localhost:8081/static/',
    hot: true,
    proxy: {
      '/': 'http://localhost:8080'
    }
  }
};
