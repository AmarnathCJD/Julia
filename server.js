#!/usr/bin/env node

// julia/modules/__init__.py
const app_name = process.env.HEROKU_APP_NAME;
const app_url = `${appname}.herokuapp.com`;

var http = require('http'); //importing http

function startKeepAlive() {
    setInterval(function() {
        var options = {
            host: app_url,
            port: 80,
            path: '/'
        };
        http.get(options, function(res) {
            res.on('data', function(chunk) {
                try {
                    // optional logging... disable after it's working
                    console.log("HEROKU RESPONSE: " + chunk);
                } catch (err) {
                    console.log(err.message);
                }
            });
        }).on('error', function(err) {
            console.log("Error: " + err.message);
        });
    }, 20 * 60 * 1000); // load every 20 minutes
}

startKeepAlive();
