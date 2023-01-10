const electron = require('electron')
// Module to control application life.
const app = electron.app
// Module to create native browser window.
const BrowserWindow = electron.BrowserWindow

const path = require('path')
const url = require('url')

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow

function createWindow () {
  // Create the browser window.
  mainWindow = new BrowserWindow({width: 800, height: 600})

  // and load the index.html of the app.
  mainWindow.loadURL(url.format({
    pathname: path.join(__dirname, '/gui/gui.html'),
    protocol: 'file:',
    slashes: true
  }))

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()

  // Emitted when the window is closed.
  mainWindow.on('closed', function () {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null
  })
}

var createWindow2 = function(){ //delete this
//   TODO: spwan a child python process to run the flask server
   //call python?
  // var subpy = require('child_process').spawn('python', ['./engine/flask_1.py']);

  // var rq = require('request-promise');
  //spawning child processes to initialize flask from electron | Other way is to run a bash script
  // var python = require('child_process').spawn('python', ['./engine/flask_1.py']);
  // python.stdout.on('data', function (data) {
  //   console.log("data: ", data.toString('utf8'));
  // });
  // python.stderr.on('data', (data) => {
  //   console.log(`stderr: ${data}`); // when error
  // });

  // let script = path.join(__dirname, 'pycalc', 'api.py')
  // pyProc = require('child_process').spawn('python', [script, port])


  var mainAddr = 'http://127.0.0.1:5000'; //This can be done to directly build everything in flask
  // Create the browser window.
  mainWindow = new BrowserWindow({width: 800, height: 600});
  // and load the index.html of the app.
  // mainWindow.loadURL('file://' + __dirname + '/index.html');
  mainWindow.loadURL(mainAddr);
  // Open the devtools.
  // mainWindow.webContents.openDevTools();
  // Emitted when the window is closed.
  mainWindow.on('closed', function() {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null;
    // kill python
    // subpy.kill('SIGINT');
    // setTimeout(() => { //kill after a delay
    //     subprocess.kill('SIGINT');
    //   }, 1000);
  });
};
// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
// app.on('ready', createWindow)

app.on('ready', createWindow2); //delete this

// Quit when all windows are closed.
app.on('window-all-closed', function () {
  // On OS X it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q

    app.quit()
})

app.on('activate', function () {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) {
    createWindow2()
  }
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
