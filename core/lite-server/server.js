const GuacamoleLite = require('guacamole-lite');
const fs = require('fs');
const logFile = fs.createWriteStream('guacamole-lite.log', { flags: 'a' });

const websocketOptions = {
    port: 3000 // Port for WebSocket server
};

const guacdOptions = {
    host: 'guacd',
    port: 4822
};

const clientOptions = {
    crypt: {
        cypher: 'AES-256-CBC',
        key: 'MySuperSecretKeyForParamsToken12'
    },
    log: {
        level: 'DEBUG', // Set log level to 'DEBUG' for maximum verbosity
        stdLog: (...args) => {
            logFile.write(new Date().toISOString() + ' - ' + args.join(' ') + '\n');
        },
        errorLog: (...args) => {
            logFile.write(new Date().toISOString() + ' - ERROR - ' + args.join(' ') + '\n');
        },
    }
};

const guacServer = new GuacamoleLite(websocketOptions, guacdOptions, clientOptions);
console.log("hello hello hello")
console.log('GuacamoleLite server running on port 3000');
