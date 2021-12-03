const Path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCSSExtractPlugin = require('mini-css-extract-plugin')

module.exports = {
  entry: {
    app: Path.resolve(__dirname, '../src/scripts/index.js'),
  },
  output: {
    path: Path.join(__dirname, '../build'),
    filename: 'js/[name].js',
  },
  optimization: {
    splitChunks: {
      chunks: 'all',
      name: 'vendors',
    },
  },
  plugins: [
    new CleanWebpackPlugin(),
    new CopyWebpackPlugin({ patterns: [{ from: Path.resolve(__dirname, '../public'), to: 'public' }] }),
    new HtmlWebpackPlugin({
      template: Path.resolve(__dirname, '../src/index.html'),
    }),
  ],
  resolve: {
    alias: {
      '~': Path.resolve(__dirname, '../src'),
    },
  },
  module: {
    rules: [

      // HTML
      {
        test: /\.(html)$/,
        use: ['html-loader']
    },

    // JS
    {
        test: /\.mjs$/,
        include: /node_modules/,
        type: 'javascript/auto',
      },

    // CSS
    {
        test: /\.css$/,
        use:
            [
                MiniCSSExtractPlugin.loader,
                'css-loader'
            ]
    },

    // Images
    {
        test: /\.(png|jpe?g|gif)$/i,
        use:
            [
                {
                    loader: 'file-loader',
                    options:
                    {
                        outputPath: 'assets/images/'
                    }
                }
            ]
    },

    // Fonts
    {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        use:
            [
                {
                    loader: 'file-loader',
                    options:
                    {
                        outputPath: 'assets/fonts/'
                    }
                }
            ]
    },

    {
        test: /\.(frag|vert|glsl)$/,
        use: [
            {
                loader: 'glsl-shader-loader',
                options: {}
            }
        ]
    },
    {
        test: /\.(gltf)$/,
        use: [
            {
                loader: "gltf-webpack-loader",
                options:
            {
                outputPath: 'assets/models/'
            }
            }
        ]
    },
    {
        test: /\.(bin)$/,
        use: [
            {
                loader: 'file-loader',
                options:
            {
                outputPath: 'assets/models/'
            }
            }
        ]
    }
    ],
  },
};
