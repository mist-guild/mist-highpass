const { app, BrowserWindow, Menu, globalShortcut } = require('electron');
const { PythonShell } = require('python-shell');

PythonShell.run(__dirname + '/Application/app.py', null, function (err, results) {
    if (err) throw err;
    console.log('results: %j', results);
});

function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 1600,
        height: 1000,
        icon: __dirname + '/src/static/myIcon.ico',
    });
    mainWindow.loadURL('http://127.0.0.1:5000');
    mainWindow.removeMenu();
    mainWindow.setResizable(false);
    //mainWindow.webContents.openDevTools();

    globalShortcut.register('f5', function () {
        console.log('Refreshing Electron page...');
        mainWindow.reload();
    })
}

app.whenReady().then(() => {
    createWindow();
});

app.on('window-all-closed', () => {
    app.quit();
    console.log("App closed.");
});