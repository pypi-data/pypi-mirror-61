edjs = function () {
    var {QWindow, QMenubar} = winjs;
    var {genUid, isdefined, disableTab,indentWhenTab} = wpjs;
    var {registerOpener, QDesktopApplication, QEvent} = sysjs;
    if (panjs) var {Pan} = panjs;

    // var store=store;
    class Editor extends QDesktopApplication {
        constructor(el, content, pan, location, filename) {
            super();
            this.className = 'Editor';
            if ((el != null) && ($.isPlainObject(el))) {
                this.el = el.el;
                this.init_content = el.content;
                this.pan = el.pan;
                this.location = el.location;
                this.filename = el.filename;
            } else {
                this.el = el;
                this.init_content = content;
                this.pan = pan;
                this.location = location;
                this.filename = filename;
            }
            this.window.setTitle('Editor');
            this.init();
            this.addEventListeners();
            this.onStart.push(() => {
                this.doOnStart();
            })
        }

        doOnStart() {
            try {
                this.restoreData();
            } catch (e) {
                console.log(e);
            }
            disableTab(this.window.el());
            indentWhenTab(this.window.find("textarea"))
        }

        restoreData() {
            var res = store.get(this.className);
            if (res) {
                var {url, location, filename} = res.pan;
                var pan = new Pan(url);
                this.openFile(pan, location, filename);
            }
        }

        saveData() {
            if (this.pan) {
                var res = store.get(this.className) || {pan: {}};
                res.pan.url = this.pan.url;
                res.pan.location = this.location;
                res.pan.filename = this.filename;
                return store.set(this.className, res);
            }
        }

        addEventListeners() {
            this.window.listenCtrlKeydown(83, (e) => {
                this.saveFile((res) => {
                    if (res) this.window.clearDialog();
                });
            })
        }

        initStyles() {
            var el = this.window.find('#' + this.uid);
            el.css({
                "height": "100%",
                "display": "flex",
                "flex-flow": "column",
            });
            el.find(".taskbar").css({
                "flex": "0 0"
            });
            el.find(".body").css({
                "flex": "1 0 auto",
                "display": "flex",
                "flex-flow": "column"
            })

        }

        init() {
            this.menubar = new QMenubar({});
            if (isdefined(this.menubar)) {
                var self = this;
                this.menubar.addItem('save', () => {
                    self.saveFile();
                })
            }
            this.init_content = this.init_content || 'Write some thing here...';
            this.window.setContent(this.html());
            this.content_box = this.window.find('.edit-area');
            this.initStyles();
        }

        update() {
            this.window.setContent(this.html());
        }

        info(msg) {
            this.window.info(msg);
        }

        setFilename(filename) {
            this.filename = filename;
            this.window.find(".info-filename").html(filename);
        }

        getFilename() {
            return this.filename || '';
        }

        saveFile(callback) {
            var self = this;
            console.log({
                location: self.location,
                filename: self.filename,
                content: self.getContent()
            });
            var res = self.pan.saveFile(self.location, self.filename, self.getContent());
            if (res) self.info("Succeeded to save file!");
            if (typeof callback === 'function') callback(res);
            this.saveData();
        }

        openFile(pan, location, filename) {
            console.log('open', filename);
            console.log("pan:", pan);
            this.pan = pan;
            this.location = location;
            this.setFilename(filename);
            // this.filename = filename;
            var content = pan.getFile(location, filename);
            this.add_content(content);
            this.saveData();
        }

        add_content(cont) {
            return this.content_box.html(cont);
        }

        getContent() {
            var content = this.content_box.val();
            return content;
        }

        html() {
            return `<div id="${this.uid}">
<div class="qeditor-head" style="display: flex;flex-flow: row;padding: 5px;">
${this.menubar.toString()}
<div class="qeditor-infobar" style="display: flex;flex:1 0 auto;flex-flow: row-reverse">
<span class="info-filename">${this.getFilename()}</span>
</div>
</div>
                
        <div class="body" style="display: flex;flex-flow: column;background-color: dimgray">
        <textarea class="edit-area" style="flex:1 0 auto;width: 100%;overflow: auto">
        ${this.init_content}
</textarea>
        </div>
                </div>`
        }
    }

    if (typeof sysjs != "undefined") {
        registerOpener('.txt', Editor);
        registerOpener('.py', Editor);
        registerOpener('.md', Editor);
        registerOpener('.bat', Editor);
        registerOpener('.sh', Editor);
        registerOpener('.gitignore', Editor);
        registerOpener('.log', Editor);
        registerOpener('.dic', Editor);
        registerOpener('.json', Editor);
    }
    return {
        Editor: Editor
    }
}();