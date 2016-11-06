var webpack = require('webpack');

module.exports = {
    entry: {
        app: './jsx/app.jsx'
    },
    output: {
        path:     '../../web/static/widgets/schedule/',
        filename: '[name].js',
    },
    module: {
        loaders: [
            { test: /\.json$/, loader: 'json'},
            {
                test: /\.jsx$/,
                loader: 'babel-loader',
                exclude: /node_modules/,
                query: {
                    presets: ['es2015', 'react']
                }
            }
        ]
    },
    stats: {
        colors: true
    },
    devtool: 'source-map'
};
