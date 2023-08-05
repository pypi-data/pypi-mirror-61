import webpack from 'webpack'
import path from 'path'
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

const webpackConfig = {
    // this is needed to resolve imports from the js root
    resolve: {
        // always import from root (src and node_modules)
        modules: [
            path.join(__dirname, "src"),
            'node_modules'
        ],
        extensions: ['', '.js']
    },
    // let the loaders be found when parsing resources in all paths
    resolveLoader: {
        root: path.join(__dirname, 'node_modules')
    },
    // library entry point
    entry: './src/index.js',
    output: {
        path: path.join(__dirname, 'dist'),
        publicPath: '/dist',
        filename: 'baton.min.js',
    },
    // this for creating source maps
    devtool: 'source-map'
};
module.exports = {

    optimization: {
        minimizer: [
            // JavaScript minify
            new UglifyJsPlugin({
                sourceMap: true,
                extractComments: true
            })
        ]
    },
    module: {
        rules: [
            // SCSS Loader
            {
                test: /\.scss$/,
                use: [
                    {
                        loader: 'style-loader'
                    },
                    {
                        loader: 'css-loader'
                    },
                    {
                        loader: 'sass-loader'
                    },

                ]
            },
            // File loaders
            {
                test: /\.(eot|woff|woff2|ttf|svg|png|jpe?g|gif)(\?\S*)?$/,
                use: [
                    {
                        loader: "url-loader"
                    }
                ]
            },
        ],
    },
};

webpackConfig.plugins = [
    // new webpack.optimize.UglifyJsPlugin({minimize: true}),
    new webpack.ProvidePlugin({
        jQuery: 'jquery',
        $: 'jquery',
        jquery: 'jquery'
    })
];

webpackConfig.module = {
    loaders: []
};

// js loaders
webpackConfig.module.loaders.push({
    test: /\.(js)$/,
    exclude: /node_modules/,
    loader: 'babel-loader',
    query: {
        presets: ['es2015', 'stage-0']
    }
});

// css loaders
// webpackConfig.module.loaders.push({
//     test: /\.scss/,
//     rules: 'style!css!postcss!sass'
// }, {
//     test: /\.sass/,
//     rules: 'style!css!postcss!sass'
// });

// File loaders
webpackConfig.module.loaders.push(
    {
        test: /\.svg(\?.*)?$/,
        loader: 'url?prefix=fonts/&name=[path][name].[ext]&limit=10000&mimetype=image/svg+xml'
    },
    /*
    {
      test: /\.(png|jpg)$/,
      loader: 'url?limit=8192'
    },
    */
    {
        test: /\.(eot|woff|woff2|ttf|svg|png|jpe?g|gif)(\?\S*)?$/,
        loader: 'url?limit=100000&name=[name].[ext]'
    }
);

export default webpackConfig
