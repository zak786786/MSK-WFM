const path = require('path');
const {app, BrowserWindow, Menu}  = require('electron');
const isMac = process.platform === 'darwin';
const isDev = process.env.NODE_ENV !== 'production';

let mainWindow;
function createmainWindow() {
    const mainWindow = new BrowserWindow({
        title: 'MSK app',
        width: isDev ? 1750: 1000,
        height: 720,
        webPreferences :{
          contextIsolation: true,
          nodIntergration: true,
          //preload: path.join(__dirname, 'preload.js')
        },
    });
if (isDev){
  mainWindow.webContents.openDevTools();
}

mainWindow.loadFile(path.join(__dirname,'index.html'));
// launches index.html - uses stylecss index- launches dashboard.js
}

app.whenReady().then(() =>{
    createmainWindow();
    const mainMenu = Menu.buildFromTemplate(menu);
    Menu.setApplicationMenu(mainMenu);


    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
          createMainWindow()
        }
      })
})
//dev tools



// menu template
const menu = [
  {
    label: 'File',
    submenu: [
      {
        label : 'Quit',
        click: () => app.quit(),
        accelerator: 'CmdOrCtrl+W'
      },
    ],
  },
];


// for mac users:
app.on('window-all-closed', () => {
  if (!isMac) {
    app.quit()
  }
})
//meta tag stopping online importing. - http-equiv
// run- npx electronmon .  -for visual changes after save 
// run- npm start  -for app start