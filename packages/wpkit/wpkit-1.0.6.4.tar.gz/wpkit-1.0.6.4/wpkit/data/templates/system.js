sysjsData = {};
sysjs = function () {
    var QWindow = winjs.QWindow;
    var QMenubar = winjs.QMenubar;
    var QDialog = winjs.QDialog;
    var QWedget = winjs.QWedget;
    var genUid = wpjs.genUid;
    var {fullScreen} = swjs;
    var {RWidget,RListbox,RButton,RPopupMenu,RDropdownMenu}=winjs;
    var Application = class {
        constructor() {
            this.window = new QWindow();

        }
    };

    var openerMap = {};
    sysjsData.openerMap = openerMap;
    var registerOpener = function (ext, opener) {
        if(!openerMap[ext]){openerMap[ext]=[]}
        openerMap[ext].push(opener);
    };

    class QEvent extends CustomEvent {
        constructor(eventName, detail) {
            super(eventName, {detail: detail});
        }
    }

    var requestLighten = function (app) {
        dispatchEvent(new QEvent("lightenApp", {app: app}));
    };
    var openApp=function (App) {
        var app=new App();
        app.start();
        app.display();
        return app;
    };
    var openFile = function (pan, location, filename) {
        console.log('opening file...', filename);
        console.log("pan:",pan);
        console.log(openerMap);
        var parts = filename.split('.');
        if (parts.length > 1) {
            var ext = '.' + parts.slice(-1)[0];
            if (Object.keys(openerMap).indexOf(ext) > -1) {
                var Opener= openerMap[ext].slice(-1)[0];
                var opener = new Opener;
                opener.start();
                console.log("before poen:",pan);
                opener.openFile(pan, location, filename);
                opener.display();
            }
        }
    };

    class QApplication {
        constructor(className) {
            className = className || 'QApplication';
            this.uid = className + genUid();
            this.onStart = [];
            this.onPrepare = [];
        }

        start() {
            for (var i in this.onStart) {
                if (typeof this.onStart[i] === 'function') {
                    this.onStart[i]();
                }
            }
        }
        display(){

        }
        prepare() {
            for (var i in this.prepare) {
                if (typeof this.prepare[i] === 'function') {
                    this.prepare[i]();
                }
            }
        }
    }

    class QDesktopApplication extends QApplication {
        constructor(className) {
            className = className || "QDesktopApplication";
            super(className);
            this.window = new QWindow();
            this.window.appendTo($($("body")[0]));
            this.window.hide();
            var self = this;
            this.window.listenClick((e) => {
                e.stopPropagation();
                self.lighten();
            });
            this.window.doClose = function () {
                dispatchEvent(new QEvent("destroyApp", {app: self}));
            };
            this.onDisplay = [];
        }

        start() {
            super.start();
            this.window.hide();
        }

        lighten() {
            dispatchEvent(new QEvent("lightenApp", {app: this}));
        }

        display(callback) {
            dispatchEvent(new QEvent("displayApp", {
                    app: this,
                    callback: () => {
                        this.initDisplay();
                        if (typeof callback === 'function') callback();
                    }
                })
            );
        }

        initDisplay() {
            for (var i in this.onDisplay) {
                if (typeof this.onDisplay[i] === 'function') {
                    this.onDisplay[i]();
                }
            }
        }
    }

    class QTaskbarItem extends QWedget {
        constructor(arg1) {
            super();
            if ($.isPlainObject(arg1)) {
                this.app = arg1.app;
            } else {
                this.app = arg1;
            }
            this.setData();
        }

        setData() {
            var app = this.app;
            this.title = app.title || app.window.getTitle();
            // console.log(this.title)
            this.callbackName = 'callback_' + genUid();
            window[this.callbackName] = function (e) {
                if (app.window.visible) {
                    requestLighten(app);
                } else {
                    app.window.show();
                    requestLighten(app);
                }
            }
        }

        source() {
            return {
                template:
                    `
                <span class="qtaskbar-item" style="height: 100%;background-color:goldenrod;min-width: 50px;" onclick="${this.callbackName}()">${this.title}</span>
                `
            }
        }
    }

    class QTaskbar extends QWedget {
        constructor() {
            super();
            this.items = [];
            this.onCreate.push(()=>{
                // console.log("new taskbar");
                // hh.j();
                // var startmenu=new RStartMenu();
                // this.el().find('.qtaskbar-body').prepend(startmenu.el);
                // console.log("new hihih")
                // startmenu.prependTo(this.find("qtaskbar-body"))
            })
        }

        itemsToString() {
            var s = '';
            this.items.map((v, i) => {
                s += v.toString();
                var src = v.source();
            });
            return s;
        }

        activate() {
            super.activate();
            this.addEventListeners();
        }

        addEventListeners() {
            var self = this;
            this.find(".qtaskbar-handle-fullscreen").click(() => {
                dispatchEvent(new QEvent("fullscreenQDE"));
            })
        }

        addItem(app) {
            var item = new QTaskbarItem({app: app});
            this.items.push(item);
            this.update();
            // console.log("add item", item)
        }

        removeItem(app) {
            // console.log("taskbar.items:",this.items);
            for (var i in this.items) {
                if (this.items[i].app === app) {
                    this.items.splice(i, 1);
                    this.update();
                    return;
                }
            }
        }

        source() {
            return {
                template:
                    `
                <div class="qtaskbar" id="${this.uid}">
                <div class="qtaskbar-head"></div>
                <div class="qtaskbar-body">
                
                ${this.itemsToString()}
                <div class="qtaskbar-addon ">
                <span class="qtaskbar-addon-item qtaskbar-handle-fullscreen">FullScreen</span>
                <input class="qtaskbar-addon-cmd" type="text"
                 style="background: white;margin:2px;height:26px;padding: 2px;flex:1 0 auto;color:black;"
                  placeholder="Input something...">
</div>
</div>
</div>
                `,
                style:
                    `\
                <style>
                 #${this.uid} {
            /*flex-flow: row;*/
            /*flex: 0 0 40px;*/
            /*display: flex;*/
            /*flex-flow: row;*/
            min-height: 30px;
            padding: 3px;
            margin: 0;
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: black;color: white;
            /*border-bottom: black dotted 2px;*/
            box-sizing: border-box;
            z-index: 65535;
        }
        #${this.uid} .qtaskbar-body{
            display: flex;
            flex-flow:row;
        }
        #${this.uid} .qtaskbar-item{
            margin:auto 3px auto 3px;
            /*padding: ;*/
            border-top: dotted black 2px;
            border-left: dotted black 2px;
            border-right: dotted black 2px;
            border-bottom: dotted black 2px;
        }
        #${this.uid} .qtaskbar-addon{
            background-color: #00a8c6;
            flex:1 0 auto;
            display: flex;
            flex-flow: row-reverse;
        }
        #${this.uid} .qtaskbar-addon-item{
            background-color:wheat;
            padding: 0px 5px;
        }
            </style>\
                `
            }
        }
    }
    // nnn=0
    class RStartMenu extends RPopupMenu{
        constructor() {
            var button=new RButton("Test");
            super("Start",button.el[0]);
            this.setZIndex(1024);
        }
    }
    class QDisplayEnvironment extends QApplication {
        constructor() {
            super();
            this.base = $('body');
            `<div style="display: flex;flex-flow: row-reverse"></div>`
            this.base.css({
                display: 'flex',
                "flex-flow": "column-reverse",
                height: "100vh",
                width: "100%",
                overflow: "hidden"
            });
            this.run();
            // console.log("create new qde...");
        }

        run() {
            this.startmenu=new RStartMenu();
            this.startmenu.appendTo(this.base);
            // console.log(this.startmenu.handle)
            this.startmenu.handle.click();
            this.taskbar = new QTaskbar();
            this.taskbar.appendTo(this.base);
            // this.taskbar.el().find('.qtaskbar-body').append(this.startmenu.handle);
            // console.log("new taskbar done...");
            this.tasks = [];
            this.addEventListeners();
        }

        setBackground(url) {
            var content = `<img src="${url}" style="position:fixed;width:100%;height: 100%;">`
            this.base.append($(content));
        }

        fullScreen() {
            var self = this;
            $(document).ready(() => {
                fullScreen(self.base);
            })
        }

        addEventListeners() {
            var self = this;
            $(window).on("displayApp", (e) => {
                self.displayApp(e.detail.app, e.detail.callback);
            }).on("destroyApp", (e) => {
                self.destroyApp(e.detail.app);
            }).on('lightenApp', (e) => {
                self.lightenApp(e.detail.app);
            }).on("fullscreenQDE", (e) => {
                self.fullScreen();
            });
        }

        lightenApp(app) {
            if (!this.tasks.length) return;
            var tapp = this.getTopApp();
            var max = tapp.window.getZIndex();
            app.window.setZIndex(max + 1);
        }

        displayApp(app, callback) {
            // return(callback())
            var [x, y] = this.getAvailablePosition(app);
            app.window.setPosition(x, y);
            app.window.appendTo(this.base);
            app.window.show();
            this.tasks.push(app);
            this.taskbar.addItem(app);
            this.lightenApp(app);
            // console.log("add tasks:",this.tasks);
            callback();
        }

        destroyApp(app) {
            this.taskbar.removeItem(app);
            var index = this.tasks.indexOf(app);
            this.tasks.splice(index, 1);
            app.window.remove();
        }

        getTopApp() {
            if (!this.tasks.length) return;
            var max = this.tasks[0].window.getZIndex();
            var index = 0;
            for (var i = 1; i < this.tasks.length; i++) {
                var tmp = this.tasks[i].window.getZIndex();
                if (tmp > max) {
                    max = tmp;
                    index = i
                }
            }
            return this.tasks[index];
        }

        getAvailablePosition(app1) {
            // console.log("app1:",app1)
            function random_between(a,b) {
                return Number.parseInt(Math.random()*(b-a)+a);
            }

            if(app1){
                    var [w,h]=app1.window.getSize();
                    var x=(window.innerWidth-w)/2+random_between(-50,50);
                    var y=(window.innerHeight-h)/2+random_between(-50,50);
                    x=x>0?x:0;
                    y=y>0?y:0;
                    return [x,y];
                }
            var app = this.getTopApp();
            var [tx, ty] = app.window.getPosition();
            tx += 20;
            ty -= 10;
            return [tx ,ty];
        }
    }

    return {
        openFile: openFile,
        registerOpener: registerOpener,
        QEvent: QEvent,
        QApplication: QApplication,
        QDesktopApplication: QDesktopApplication,
        QDisplayEnvironment: QDisplayEnvironment,
        openApp
    }
}();