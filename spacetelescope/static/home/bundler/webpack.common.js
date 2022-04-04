const CopyWebpackPlugin = require('copy-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const MiniCSSExtractPlugin = require('mini-css-extract-plugin')
const path = require('path')

module.exports = {
    entry: path.resolve(__dirname, '../src/script.js'),
    output:
    {
        filename: 'bundle.[contenthash].js',
        path: path.resolve(__dirname, '../dist')
    },
    devtool: 'source-map',
    plugins:
        [
            new CopyWebpackPlugin({
                patterns: [
                    { from: path.resolve(__dirname, '../static') }
                ]
            }),
            new HtmlWebpackPlugin({
                template: path.resolve(__dirname, '../src/home.html'),
                minify: true
            }),
            
            new MiniCSSExtractPlugin()
        ],
    module:
    {
        rules:
            [
                // HTML
                {
                    test: /\.(html)$/,
                    use: ['html-loader']
                },

                // JS
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use:
                        [
                            'babel-loader'
                        ]
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
            ]
    }
}
