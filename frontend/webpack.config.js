// webpack.config.js
const path = require('path');

module.exports = {
    entry: './src/content_scripts/main.js', // Entry point
    output: {
    filename: 'content.js', // Output file
    path: path.resolve(__dirname, 'extension'), // Output directory
    },
    mode: 'production',
};