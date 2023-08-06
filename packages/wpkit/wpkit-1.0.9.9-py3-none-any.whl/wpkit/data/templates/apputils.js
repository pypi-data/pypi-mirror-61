apputiljs = function () {
    class Switch {
        constructor(turnOn, turnOff) {
            this.status = 'off';
            this.turnOn = (e) => {
                turnOn(e);
                this.status = 'on';
            };
            this.turnOff = (e) => {
                turnOff(e);
                this.status = 'off';
            };
        }

        reverse(e) {
            if (this.status === 'on') this.turnOff(e);
            else this.turnOn(e);
            return this;
        }

        bindKey(dic) {

            if (dic.on) {
                jwerty.key(dic.on, (e) => {
                    this.turnOn(e)
                });
            }
            if (dic.off) {
                jwerty.key(dic.off, (e) => {
                    this.turnOff(e)
                })
            }
            if (dic.reverse) {
                console.log("dic:", dic.reverse);
                jwerty.key(dic.reverse, (e) => {
                    console.log('reverse');
                    this.reverse(e)
                })
            }
            return this;
        }
    }

    var simpleMaximaze = function (el) {
        el.appendTo($("body"));
        $("body").height("100%");
        $("body").width("100%");
        el[0].style = el[0].style + `
            position:fixed;
            left:0;top:0;right:0;bottom:0;
            z-index:65535;
            padding:30px;
            box-sizing:bordered-box;
            overflow:auto;
        `;
        el.css("min_height", "100%");
        el.css("width", "100%");
        el.css('position', 'fixed')
    };
    Div = function () {
        return $('<div></div>')
    };
    Form = function () {
        return $('<form></form>')
    };
    var contentWindow = function (content) {
        var win = new winjs.RWindow();
        win.setContent(content);
        win.appendTo($('body'));
        win.hide();
        return win;
    };
    var T = wpjs.T;
    hook = {};
    if (typeof hidden_area === 'undefined') hidden_area = $('<div></div>').appendTo($('body')).hide();

    function createElement(tag) {
        var sinTags = [
            'img', 'hr', 'br'
        ];
        var douTags = [
            'div', 'ul', 'li', 'label'
        ];
        if (sinTags.indexOf(tag) > -1) {
            var el = $(`<${tag}></${tag}>`);
        } else {
            var el = $(`<${tag}>`);
        }
        return el.appendTo(hidden_area);
    }

    function hideElement(el) {
        el.hide();
        el.attr('visible', 'false');
    }

    function showElement(el) {
        el.show();
        el.attr('visible', 'true');
    }

    function inverseVisibility(el) {
        if (el.attr('visible') === 'false') {
            showElement(el)
        } else hideElement(el);
    }

    function stringPlaceHolder(length = 4, color = 'yellow') {
        var el = createElement('span').css({'background-color': color, "color": color}).html('吃'.repeat(length));
        return el;
    }

    class BookViewer {
        constructor(os,root) {
            this.os = os;
            this.root=root;
            this.win = contentWindow('').fitHeight().dockRight().width("80vw");
            this.sidebarWindow=contentWindow('').fitHeight().dockLeft().show().width('19vw').setBackgroundColor('#2C7EEA');
            // this.win.setBackgroundColor('#2C7EEA');
            this.render();
            this.info=this.os.tranverse_info(this.root);
            this.location='.';
            this.path='.';
            this.history=[this.path];
            var menu=createElement('div').width("100%").css({
                'background-color':'#1161EE',
                'color':'white'
            });
            this.win.flexRow(menu);
            var btn=createElement('button').css({
                'background-color':'inherit',
                'margin':'0',
                'color':'white'
            });
            btn.html('Back').click(()=>{this.backward()});
            `<div style="background-color: #1161EE;">`
            var pathBox=createElement('div').css({
                'background-color':'#1161EE',
                'color':'white',
                'min-width':'10em',
                'flex-flow':'row-reverse',
                'padding':'0px 5px',
                'font-weight':'bold'
            });
            menu.append(btn);
            menu.append(pathBox);
            this.pathBox=pathBox;
            this.win.addBar('menu',menu);
            this.win.contentBox.css({
                'padding-bottom':'3em'
            });
        }
        getInfo(path){
            // console.log("get info path:",path);
            path=this.os.standard_path(path);
            var names=path.split('/');
            var info=this.info;
            if(path.startsWith('/')||path.startsWith('.')){info=this.info;names.splice(0,1);}
            names.forEach((name)=>{if(!(name===''))info=info.children[name]});
            return info;
        }
        render(){
            var els=this.win.find('[book-link]');
            var el;
            for(let i=0;i<els.length;i++){
                el=$(els[i]);
                el.css('color','blue');
                el.click((e)=>{
                    e.preventDefault();
                    var el=$(e.target);
                    var path=el.attr('book-link');
                    // console.log("el:",el[0],"book-link:",path);
                    path=this.linkToPath(path);
                    // console.log("path:",path);
                    this.goTo(path);
                })
            }
            return this;
        }
        linkToPath(link){
            if(link.startsWith('/'))return link;
            return this.standard_path(this.location+'/'+link);
        }
        ospath(path){
            return this.root+'/'+path;
        }
        standard_path(path){
            return this.os.standard_path(path);
        }
        dirname(path){
            return this.os.dirname(path);
        }
        relpath(path){
            var path=this.os.relpath(this.root,path);
            if(path==='')path='/';
            return path;
        }
        viewPath(path,relpath){
            if(relpath)path=this.ospath(relpath);

            hook.location=this.location;
            var content;
            function  endsWith(str,list) {
                var res;
                list.forEach((ext)=>{
                    if(str.endsWith(ext))res=ext;
                });
                return res;
            }
            var extToLang={
              '.py':'python',
                '.js':'javascript'
            };
            if (path.endsWith('.page'))this.win.wrapHtml(this.os.getpage(path)).show();
            else if(path.endsWith('.md'))this.win.wrapMarkdown(this.os.read(path)).show();
            else if(path.endsWith('.html'))this.win.wrapHtml(this.os.read(path)).show();
            else if(path.endsWith('.jpg')|| path.endsWith('.png') || path.endsWith('.gif') ||path.endsWith('.jpeg')){content=createElement('img').attr('src',this.os.geturl(path));this.win.setContent(content).show();}
            else if(this.getInfo(relpath).type===T.DIR)this.win.wrapHtml(this.os.getpage(path)).show();
            else if(endsWith(path,['.py','.js','.c','.bat','.sh'])){
                let ext=endsWith(path,['.py','.js','.c','.bat','.sh']);
                this.win.wrapCode(this.os.read(path),extToLang[ext]).show();
            }
            else this.win.wrapText(this.os.read(path)).show();
            this.render();
        }
        view(){
            var sidebarContent=this.viewInfo(this.info);
            this.sidebarWindow.setContent(sidebarContent);
            this.refresh();
            return this;
        }
        relLocation(path){
            var info=this.getInfo(path);
            if(info.type===T.DIR)return path;
            else return this.dirname(path);
        }
        refresh(){
            this.path=this.history[this.history.length-1];
            this.location=this.relLocation(this.path);
            this.pathBox.html(this.path);
            this.viewPath('',this.path);return this;
        }
        backward(){
            if(this.history.length<=1)return this;
            var path=this.history.pop();
            this.refresh();return  this;
        }
        goTo(path){
            this.history.push(path);
            this.refresh();return this;
        }
        foreward(path){

        }
        viewInfo(item, depth = 0, root = null) {
            if(!root){
                root=this.root;
                var path=root;
            }else {
             var path = root + '/' + item.name;
            }
            var label = createElement(`div`);
            var nameTag = createElement('span').html(item.name);
            label.append(nameTag);
            label.prepend(stringPlaceHolder(depth * 3));
            var handle = createElement('span');
            nameTag.append(handle);
            nameTag.attr('path', path);
            `<div style="background-color: #2C7EEA">`;
            label.css({
                'color': 'white',
                'background-color': '#2C7EEA'
            });
            if (item.type === T.DIR) {
                nameTag.css({
                    'color': 'white',
                    'background-color': 'green'
                });
                handle.addClass('fa fa-folder-o');
                var el = createElement('div');
                el.append(label);
                var children_el = createElement('div');
                children_el.addClass('children');
                if (depth >= 1) hideElement(children_el);
                el.append(children_el);
                // console.log("item:", item);
                hook.item = item;
                if (Object.keys(item).indexOf('children') > -1) {
                    for(let name in item.children){
                        var child=item.children[name];
                        children_el.append(this.viewInfo(child, depth + 1,path));
                    }
                    // item.children.forEach((child) => {
                    //     children_el.append(this.viewInfo(child, depth + 1,path))
                    // });
                }
                nameTag.click(() => {
                    var ch = el.children('.children');
                    inverseVisibility(ch);
                });
                nameTag.click(() => {
                    console.log("path:",path);
                    // this.viewPath(path);
                    this.goTo(this.relpath(path));
                });
                return el;
            } else if (item.type === T.FILE) {
                nameTag.css({
                    'color': 'white',
                    'background-color': 'red'
                });
                nameTag.click(() => {
                    // this.viewPath(path)
                    this.goTo(this.relpath(path));
                });
                handle.addClass('fa fa-file-o');
                var el = createElement('div');
                el.append(label);
                return el;
            }


        }
    }

    function viewInfo(item, depth = 0, root = null) {
        var path = root + '/' + item.name;
        var label = createElement(`div`);
        var nameTag = createElement('span').html(item.name);
        label.append(nameTag);
        label.prepend(stringPlaceHolder(depth * 3));
        var handle = createElement('span');
        nameTag.append(handle);
        nameTag.attr('path', path);
        label.css({
            'color': 'white',
            'background-color': 'gray'
        });
        if (item.type === T.DIR) {
            nameTag.css({
                'color': 'white',
                'background-color': 'green'
            });
            handle.addClass('fa fa-folder-o');
            var el = createElement('div');
            el.append(label);
            var children_el = createElement('div');
            children_el.addClass('children');
            if (depth >= 1) hideElement(children_el);
            el.append(children_el);
            console.log("item:", item);
            hook.item = item;
            if (Object.keys(item).indexOf('children') > -1) {
                item.children.forEach((child) => {
                    children_el.append(viewInfo(child, depth + 1))
                });
            }
            nameTag.click(() => {
                var ch = el.children('.children');
                inverseVisibility(ch);
            });
            return el;
        } else if (item.type === T.FILE) {
            nameTag.css({
                'color': 'white',
                'background-color': 'red'
            });
            handle.addClass('fa fa-file-o');
            var el = createElement('div');
            el.append(label);
            return el
        }


    }

    return {
        contentWindow,
        simpleMaximaze,
        Switch,
        viewInfo,
        hideElement,
        showElement,
        inverseVisibility,
        BookViewer
    }
}();