const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    entry: './src/js/index.js',
    output: {
        filename: 'index.js',
        path: 'C:/Users/User/Desktop/Django/projects/bug_tracker_project/bug_tracker/bug_tracker/static/js',
    },
    module: {
        rules:[
            {
                test: /\.(scss)$/,
                use: [
                MiniCssExtractPlugin.loader,
                'css-loader',
                'sass-loader']
            }
        ],
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: '../css/index.css',
        }),
    ]
};