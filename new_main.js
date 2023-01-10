const electron = require('electron')
// Module to control application life.
const app = electron.app
// Module to create native browser window.
const BrowserWindow = electron.BrowserWindow

// electron.crashReporter.start();

const path = require('path')
const url = require('url')

var mainWindow = null;
var subpy = null;

app.on('ready', function () {
  // call python?
  subpy = require('child_process').spawn('python', ['./pose_backend.py']);
  //var subpy = require('child_process').spawn('./dist/hello.exe');
  var rq = require('request-promise');
  var mainAddr = 'http://127.0.0.1:5000';

  var openWindow = function () {
    mainWindow = new BrowserWindow({ width: 800, height: 600 });
    // mainWindow.loadURL('file://' + __dirname + '/index.html');
    mainWindow.loadURL('http://127.0.0.1:5000');
    mainWindow.webContents.openDevTools();
    mainWindow.on('closed', function () {
      mainWindow = null;
      subpy.kill('SIGINT');
    });
  };

  // var startUp = function(){
  // rq(mainAddr)
  //     .then(function(htmlString){
  //         console.log('server started!');
  //         openWindow();
  //     })
  //     .catch(function(err){
  //         console.log('waiting for the server start...');
  //         //TODO: add certain time out to prevent infinite loop
  //         startUp();
  //     });
  // };

  var startUp = function (attempts) {
    // default value for attempts if not provided
    attempts = attempts || 0;

    // maximum number of attempts
    var maxAttempts = 10;

    rq(mainAddr)
      .then(function (htmlString) {
        console.log('server started!');
        openWindow();
      })
      .catch(function (err) {
        console.log('waiting for the server start..., attempt ' + attempts + ' of ' + maxAttempts);
        if (attempts < maxAttempts) {
          // try again after 1 second
          setTimeout(function () {
            startUp(attempts + 1);
          }, 1000);
        } else {
          console.error('Error: server could not be started');
          // handle error, e.g. display message to user
        }
      });
  };

  //fire!
  startUp();
});


app.on('window-all-closed', function () {
  //if (process.platform != 'darwin') {
  // app.quit();
  //}
  try {
    console.log('closing server')
    subpy.stdin.write('\x03')
  } catch (err) {
    console.log(err);
    console.log('subpy not started');
    console.log('Cannot close server');
  }
  app.quit();
});