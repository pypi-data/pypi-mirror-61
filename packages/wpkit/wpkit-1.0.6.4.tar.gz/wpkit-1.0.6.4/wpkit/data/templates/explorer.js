explorerjs = function () {
    var QWindow = winjs.QWindow;
    var {Pan} = panjs;
    // var pan = new panjs.Pan("http://127.0.0.1:8002/fs");
    var Editor = edjs.Editor;
    var T = wpjs.T;
    var genUid = wpjs.genUid;
    var {
        openFile,
        QEvent,
        QApplication,
        QDesktopApplication
    } = sysjs;

    class Explorer extends QDesktopApplication {
        constructor() {
            super("Explorer");
            this.className = "Explorer";
            this.window.setTitle("Explorer");
            this.onDisplay.push(() => {
                this.init();
            });
        }

        init() {
            this.window.setContent(this.source().template);
            this.viewbox = $('#' + this.uid);
            this.vm = this.init_vm({win: this.window});
        }

        openPan(pan) {
            if (!this.vm) {
                this.init_vm({pan: pan});
            }
        }

        init_vm(obj) {
            var {win, pan, location, root_path, loc_history} = obj;
            var vm = new Vue({
                el: `#${this.uid}`,
                delimiters: ['<%', '%>'],
                data: {
                    className: 'Explorerer',
                    pan: pan,
                    items: [],
                    location: location || "./",
                    root_path: root_path || "./",
                    loc_history: loc_history || ['./'],
                    window: win,
                    cache: {
                        timeOut: null
                    }
                },
                created: function () {
                    // console.log("created...");
                    this.window.setSize(550,400);
                    if (!this.pan && !this.restoreData()) {
                        var loc=window.location.href;
                        loc=loc.slice(0,-1);
                        this.input({msg:`Input A url that I can host,default:${loc}`, callback:(url) => {
                            if (!url || url === '') {
                                url = loc;
                            }
                            var pan = new Pan(url);
                            console.log("new pan:", pan)
                            this.openPath(pan);
                        }, defaultValue:loc,placeHolder: this.defaultValue});
                    }
                },
                methods: {
                    openPath(pan, location, root_path, loc_history) {
                        this.pan = pan;
                        this.location = location || './';
                        this.root_path = root_path || './';
                        this.items = this.pan.getDir(this.root_path, this.location);
                        this.loc_history = loc_history || ['./'];
                        this.saveData();
                        this.refresh();
                    },
                    clearData(){
                        var res = store.get(document.location + "." + this.className);
                        // console.log(res)
                        if(res){
                            store.remove(document.location + "." + this.className);
                            var res = store.get(document.location + "." + this.className);
                            console.log("after clear:",res);
                            this.refresh();
                        }
                    },
                    restoreData() {
                        var res = store.get(document.location + "." + this.className);
                        if (res) {
                            var {url, location, root_path, loc_history} = res.pan;
                            var pan = new Pan(url);
                            try {
                                this.openPath(pan, location, root_path, loc_history);
                                return true;
                            } catch (e) {
                                console.log(e);
                                return null;
                            }
                        }
                    },
                    saveData() {
                        if (this.pan) {
                            var res = store.get(document.location + "." + this.className) || {pan: {}};
                            res.pan.url = this.pan.url;
                            res.pan.location = this.location;
                            res.pan.root_path = this.root_path;
                            res.pan.loc_history = this.loc_history;
                            return store.set(document.location + "." + this.className, res);
                        }
                    },
                    log: function (text) {
                        text = text || 'expolorer info....';
                        console.log(text);
                    },
                    dialog: function (e) {
                        console.log('window:', this.window);
                        // this.window.dialog();
                        this.window.input((text) => {
                            console.log('get text:', text);
                        });
                        console.log('dialog sent...');
                    },
                    input: function (msg, callback, hint = '',defaultValue='') {
                        if ($.isPlainObject(msg)) {
                            var {msg, callback, hint, defaultValue} = msg;
                        }
                        this.window.inputText({msg, callback:(text) => {
                            callback(text);
                        }, placeHolder:hint,defaultValue});
                    },
                    confirm: function (msg, callback) {
                        this.window.confirm(msg, callback);
                    },
                    info: function (msg, callback) {
                        this.window.info(msg, callback);
                    },
                    warn: function (msg, callback) {
                        this.window.warn(msg, callback);
                    },
                    forward: function (name) {
                        this.loc_history.push(this.location + '/' + name);
                        this.refresh();
                    },
                    backward: function () {
                        if (this.loc_history.length <= 1) {
                            return false;
                        }
                        this.loc_history.pop();
                        this.refresh();
                    },
                    goTo: function (path) {
                        this.loc_history.push(path);
                        this.refresh();
                    },
                    goHome: function () {
                        this.goTo(this.loc_history[0]);
                    },
                    refresh: function () {
                        var loc = this.loc_history.slice(-1)[0];
                        this.items = this.pan.getDir(this.root_path, loc);
                        this.location = loc;
                        // this.saveData();
                    },
                    tryNewFile: function (e) {
                        var self = this;
                        // console.log("new file");
                        this.input('What is the file name?', function (fn) {
                            self.pan.newFile(self.location, fn);
                            self.refresh();
                        })
                    },
                    tryNewDir: function (e) {
                        var self = this;
                        this.input('What is the directory name?', function (dn) {
                            self.pan.newDir(self.location, dn);
                            self.refresh();
                        })
                    },
                    trySaveFile: function (location, filename, content) {
                        var res = this.pan.saveFile(location, filename, content);
                        if (!res) {
                            this.warn("Cannot save file! An error occured!")
                        } else {
                            this.info("Succeeded!")
                        }

                    },
                    tryDeleteFile: function (name) {
                        var self = this;
                        this.confirm(`Are You sure to delete the file ${name}?`, function () {
                            self.pan.deleteFile(self.location, name);
                            self.refresh();
                        })
                    },
                    tryDeleteDir: function (name) {
                        var self = this;
                        this.confirm('Are You sure to delete the directory?', function () {
                            self.pan.deleteDir(self.location, name);
                            self.refresh();
                        })
                    },
                    tryDelete: function (e) {
                        var selected = this.selected();
                        console.log(e, selected);
                        selected.map((v, i) => {
                            var item = $(v);
                            var type = item.attr("itemtype");
                            var name = item.attr("itemname");
                            if (type === T.DIR) this.tryDeleteDir(name);
                            else if (type === T.FILE) this.tryDeleteFile(name);
                        })
                    },
                    tryUpload: function (e) {
                        var self = this;
                        this.window.inputFile("Choose file to upload", (name, files) => {
                            var file = files[0];
                            console.log("file to upload:", name, file);
                            self.pan.uploadFile(self.location, file.name, file, (res) => {
                                if (res.success) {
                                    self.info(res.msg);
                                } else {
                                    self.warn(res.msg);
                                }
                                self.refresh();
                            });
                        });
                    },
                    tryDownload:function(e){
                        var self=this;
                        var items=this.selected();
                        if(items.length>0){
                            var item=$(items[0]);
                            var name=item.attr("itemname");
                            var url=this.pan.getUrl(this.location,name);
                            // console.log(window)
                            window.open(url);
                        }
                    },
                    tryPull:function(e){
                        this.pan.pull((res)=>{
                            this.refresh();
                            this.info(res.msg);
                        });
                    },
                    tryPush:function(e){
                        this.pan.push((res)=>{
                            this.refresh();
                            this.info(res.msg);
                        });
                    },
                    unselectAllItems: function () {
                        var el = $(this.$el);
                        var items = el.find(".flist-item");
                        items.map((v, i) => {
                            var item = $(i);
                            // item.attr("item-selected","false");
                            item.removeClass("fitem-selected");
                        });
                    },
                    selectItem: function (e) {
                        // e.preventDefault();
                        clearTimeout(this.cache.timeOut);
                        var self = this;
                        this.cache.timeOut = setTimeout(function () {
                            console.log('单击');
                            // 单击事件的代码执行区域
                            // ...
                            e.preventDefault();
                            e.stopPropagation();
                            //console.log(e)
                            var obj = $(e.target).parent();
                            self.unselectAllItems();
                            // obj.attr("item-selected","true");
                            obj.addClass("fitem-selected");

                        }, 200);
                    },
                    selected: function () {
                        var el = $(this.$el);
                        var items = el.find(".flist-item");
                        var selected = [];
                        items.map((i, v) => {
                            var item = $(v);
                            // if(item.attr("item-selected")=="true"){selected.push(v)}
                            if (item.hasClass("fitem-selected")) {
                                selected.push(v)
                            }
                        });
                        return selected;
                    },
                    updateView: function (e) {
                        // console.log(e.target);
                        e.preventDefault();
                        clearTimeout(this.cache.timeOut);
                        var obj = $(e.target).parent('.flist-item');
                        var name = obj.attr('itemname');
                        var type = obj.attr('itemtype');
                        switch (type) {
                            case T.DIR:
                                this.forward(name);
                                break;
                            case T.FILE:
                                // console.log(" give pan:",this.pan)
                                openFile(this.pan, this.location, name);
                                break;
                            default:
                                null;
                                break;
                        }

                    }
                }
            });
            vm.$data.window = this.window;
            console.log('window init:', vm.$window);
            return vm;
        }

        source() {
            return {
                template: `<div class="w-100 h-100 explorer" id="${this.uid}" @click="unselectAllItems">
        <div class="text-info head">
            <span class="label-primary menu-item" @click="goHome">Home</span>
            <span @click="backward" class="label-public menu-item">Back</span>
            <span class="label-primary menu-item" @click="tryNewFile">New File</span>
            <span class="label-public menu-item" @click="tryNewDir">New Dir</span>
            <span @click="tryDelete" class="label-primary menu-item">Delete</span>
            <span @click="refresh" class="label-primary menu-item">Refresh</span>
            <span @click="tryUpload" class="label-primary menu-item">Upload</span>
            <span @click="tryDownload" class="label-primary menu-item">Download</span>
            <span @click="clearData" class="label-primary menu-item">ClearData</span>
            <span @click="tryPull" class="label-primary menu-item">Pull</span>
            <span @click="tryPush" class="label-primary menu-item">Push</span>
        </div>
        <div class="body" >
            <div class="flist-item" v-bind:itemname="fileitem.name" v-bind:itemtype="fileitem.type" 
                 v-for="fileitem in items">
                <label @dblclick="updateView" @click="selectItem" ><%fileitem.name%></label>
                <label><%fileitem.type%></label>
            </div>
        </div>
    </div>
    <style>
        #${this.uid} {
            display: flex;
            flex-flow: column;
        }
        #${this.uid} .head {
            flex: 0 1 40px;
            width: 100%;
            background-color: white;color: orange;
            border-bottom: black dotted 2px;
        }
        #${this.uid} .head .menu-item{
            margin:auto -3px auto -3px;
            padding:0 3px;
            border: dotted black 2px;
        }
        #${this.uid} .flist-item{
            border-bottom: dotted 2px black;
        }
        #${this.uid} .body {
            flex: 1 0 auto;
            max-height: calc(90% - 40px);
            /*height: 300px;*/
            width: 100%;
            background-color: white;
            color: orange;
            overflow: auto;
        }
        #${this.uid} .fitem-selected{
            background-color: dodgerblue;color:white;
        }
    </style>`,
                style: ``
            }
        }

    }

    return {
        Explorer: Explorer
    }
}();
