if(typeof hidden_area==='undefined') {
                hidden_area = $('<div  class="hidden-area"></div>').hide();
                $('body').append(hidden_area);
            };
guijs=function () {
var {
        genUid, isdefined, makeDraggable, simpleMakeResizable
    } = wpjs;
    const parseCss=function(str){
      // str='';
      str=str.trim();
      if(str.endsWith(';'))str=str.slice(0,str.length-1);
      // console.log("str:",str);
      var dict={};
      var arr=str.split(';');
      arr.forEach((pair)=>{
          var [key,value]=pair.split(':');
          dict[key]=value;
      });
      return dict;
    };
    const createElement=function (tag) {
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
    };
    const wrapText=function(text){
      let el=createElement('textarea');
      el.attr('readonly','true');
      el.width('100%');
      el.height('100%');
      el.css('border','none');
      el.css('overflow-y','visible');
      el.val(text);
      return el
    };
    const wrapHtml=function(text){
      let el=createElement('div');
      el.html(text);
      return el;
    };
    const wrapMarkdown=function(text){
      let el=createElement('div').addClass('markown-box');
      el.html(marked(text));
      return el;
    };
    const flexRow=function (el) {
        return el.css(parseCss(`display:flex;flex-flow:row`));
    };
    const flexColumn=function (el) {
        return el.css(parseCss(`display:flex;flex-flow:column`));
    };
    class RWidget{
        constructor(el,className) {
            if($.isPlainObject(el)){
                el=el.el;
                className=el.className;
            }
            className=className||this.constructor.name||"RWidget";
            el=el || '<div></div>';
            this.id=className+genUid();
            this.el=$(el);
            this.el.addClass(className);
            hidden_area.append(this.el);
            this.el.attr('id',this.id);
            this.visible=true;
        }
        editable(){this.attr('contenteditable','true');return this;}
        white(){this.setBackgroundColor('white');return this;}
        orange(){this.setBackgroundColor('orange');return this;}
        green(){this.setBackgroundColor('green');return this;}
        red(){this.setBackgroundColor('red');return this;}
        blue(){this.setBackgroundColor('#2C7EEA');`<div style="background-color: #2C7EEA">`;return this;}
        yellow(){this.setBackgroundColor('yellow');return this;}
        dockLeft(){this.left(0);return this;}
        dockRight(){this.right(0);return this;}
        fixed(){this.fromCssString('position:fixed;');return this;}
        fitHeight(){this.fullViewHeight();this.top(0);return this;}
        fitWidth(){this.fullViewWidth();this.left(0);return this;}
        fitViewport(){this.fixed().left(0).top(0).fullViewWidth().fullViewHeight();return this;}
        fullViewHeight(){this.height('100vh');return this;}
        fullViewWidth(){this.width('100vw');return this;}
        fitParent(){this.fullWidth().fullHeight();return this;}
        fullHeight(){this.height('100%');return this;}
        fullWidth(){this.width('100%');return this;}
        flexRow(el){
            el=el||this.el;
            flexRow(el);
            return this;
        }
        flexColumm(el){
            el=el||this.el;
            flexColumn(el);
            return this;
        }
        wrapText(text){this.setContent(wrapText(text));return this;}
        wrapHtml(text){this.setContent(wrapHtml(text));return this;}
        wrapCode(text,type){
            var pre=createElement('pre');
            var code=createElement('code').addClass('language-'+type);
            pre.append(code);
            text=hljs.highlightAuto(text).value;
            code.html(text);
            // console.log("pre:",pre);
            this.setContent(pre);
            return this;
        }
        wrapMarkdown(text){this.setContent(wrapMarkdown(text));return this;}
        setContent(content){this.contentBox.html(content);return this;}
        disableDefualtCtrlAndThisKeydown(key){
            this.onCtrlAndThisKeydown(key,(e)=>{
                e.preventDefault();
            });return this;
        }
        disableDefaultKeydown(key){
            this.onThisKeydown(key,(e)=>{
                e.preventDefault();
            });return this;
        }
        disableDefaultEvent(eventName){
            this.on(eventName,(e)=>{
                e.preventDefault();
            });return this;
        }
        hover(callback){
            if(!callback){return this.el.hover();}
            this.el.hover(callback);return this;
        }
        click(callback){
            if(!callback){return this.el.click();}
            this.el.click(callback);return this;
        }
        on(types, selector, data, fn ){this.el.on(types, selector, data, fn );return this;}
        onKeydown(callback){this.el.onkeydown(fn);return this;}
        onEnterKeydown(callback){this.onThisKeydown(13,callback);return this;}
        onTabKeydown(callback){this.onThisKeydown(9,callback);return this;}
        onCtrlAndThisKeydown(key,callback){
            this.onCtrlKeydown((e)=>{
                if(e.keyCode===key){
                    if(callback)callback(e);
                }
            });return this;
        }
        onCtrlKeydown(callback){
            this.onKeydown((e)=>{
                if(e.ctrlKey){
                    if(callback)callback(e);
                }
            });return this;
        }
        onThisKeydown(key,callback){
            this.el.onkeydown((e)=>{
                if(e.keyCode===key){
                    if(callback)callback(e);
                }
            });return this;
        }
        simpleMakeResizable(){
            this.css({
                "resize":"both",
                "overflow":"auto"
            });return this;
        }
        isRWidget(el){return el instanceof RWidget;}
        setScrollbar(el){return this;}
        makeDraggable(handle){if(!handle)handle=this.handle;makeDraggable(this.el,handle);return this;}
        shadow(){this.el.css('box-shadow','0 9px 46px 8px rgba(0,0,0,.14), 0 11px 15px -7px rgba(0,0,0,.12), 0 24px 38px 3px rgba(0,0,0,.2)');return this;}
        setBackgroundImage(arg){return this.css("background-image",arg)}
        setBackgroundColor(arg){return this.css("background-color",arg)}
        setColor(arg){return this.css("color",arg)}
        setZIndex(arg){return this.css("z-index",arg);}
        getZIndex(){return this.css('z-index')}
        setPosition(top,left){this.top(top);this.left(left)}
        getPosition(){return [this.top(),this.left()]}
        right(arg){ if(typeof arg!='undefined'){var res=this.css("right",String(arg));return this;}else {var res=this.css("right");return res;}}
        bottom(arg){ if(typeof arg!='undefined'){var res=this.css("bottom",String(arg));return this;}else {var res=this.css("bottom");return res;}}
        left(arg){ if(typeof arg!='undefined'){var res=this.css("left",String(arg));return this;}else {var res=this.css("left");return res;}}
        top(arg){ if(typeof arg!='undefined'){var res=this.css("top",String(arg));return this;}else {var res=this.css("top");return res;}}
        setSize(w,h){this.width(w);this.height(h);}
        getSize(){return [this.width(),this.height()]}
        height(h){this.el.height(h);return this;}
        width(arg){this.el.width(arg);return this;}
        fromCssString(str){var dict=parseCss(str);this.el.css(dict);return this;}
        fromAttrString(str){var dict=parseCss(str);this.el.attr(dict);return this;}
        css(name,value){var res;if(value)res=this.el.css(name,value);else res=this.el.css(name);return value?this:res;};
        attr(name,value){var res;if(value)res=this.el.attr(name,value);else res=this.el.attr(name);return value?this:res;}
        prependTo(el){if(this.isRWidget(el)){el=el.el;}this.el.prependTo($(el));return this;}
        appendTo(el){if(this.isRWidget(el)){el=el.el;}this.el.appendTo($(el));return this;}
        appendToBody(){var body=$('body');this.appendTo(body);return this;}
        append(el){if(el instanceof RWidget)el=el.el;this.el.append($(el));return this;}
        html(el){if(el instanceof RWidget)el=el.el;var res=this.el.html(el);return el?this:res;}
        html(el){if(el instanceof RWidget)el=el.el;if(el){this.el.html(el);return this}else {return this.el.html();}}
        find(arg){return this.el.find(arg);}
        children(arg){return this.el.children(arg);}
        parent(arg){return this.el.parent(arg);}
        invertVisibility(){if(this.visible){this.hide();} else{this.show();}return this;}
        remove(){this.el.remove();return this;}
        hide(){this.visible=false;this.el.hide();return this;}
        show(){this.visible=true;this.el.show();return this;}
        reverseFlexDirection(){if(this.contentBox.css('flex-direction')==='column')this.contentBox.css('flex-direction','column-reverse'); else if(this.contentBox.css('flex-direction')==='column-reverse')this.contentBox.css('flex-direction','column');return this;}
    }
    class RButton extends RWidget{
        constructor(content,onclick) {
            super("<button></button>");
            if($.isPlainObject(content)){
                content=content.content;
                onclick=content.onclick;
            }
            if(content)this.el.html(content);
            if(onclick)this.click(onclick);
        }
    }
    class RListbox extends RWidget{
        constructor(...items) {
            super();
            this.width(200);
            this.css({
                "background-color":"blue",
                "color":"white",
                "font":"bold",
                "min-height":"200px"
            });

            var itemList=$("<div></div>");
            this.itemList=itemList;
            this.el.append(itemList);
            items.forEach((item)=>{this.addItem(item)});
        }
        addItem(el){
            this.itemList.append($(el));
            // console.log("new hihih")
        }
    }
    class RMenu extends RWidget{

    }
    class RDropdownMenu extends RMenu{}
    class RPopupMenu extends RMenu{
        constructor(title,...items) {
            super();
            // console.log('items:',items)
            this.listbox=new RListbox(items);
            var handle=new RButton(title,(e)=>{
                this.listbox.invertVisibility();
            });
            this.handle=handle;
            this.listbox.appendTo(this.el);
            this.handle.appendTo(this.el);
        }

    }
    class RInput extends RWidget{
        constructor(el) {
            super('<input>');
            if($.isPlainObject(el)){
                if(el.type)this.el.attr("type",el.type);
                if(el.value)this.el.attr("value",el.value);
            }
        }
        type(arg){
            if(arguments.length){
                this.attr("type",arg);
            }else {
                this.attr("type");
            }
        }
        files(){return this.el[0].files;}
        val(arg){if(typeof arg!='undefined'){this.el.val(arg);return this;}else{return this.el.val();}}


    }
    class RTextInput extends RInput{}
    class RFileInput extends RInput{}
    class RDialog extends RWidget{
        constructor() {
            super();
        }
    }
    class RMessagebox extends RDialog{}
    class RInputDialog extends RDialog{
        constructor() {
            super();
            var input=new RInput();
            input.appendTo(this.el);
            this.input=input;
        }
    }
    class RConfirmDialog extends RDialog{
        constructor(callback) {
            super();
            var nb=new RButton("YES");
            nb.click(()=>{this.remove()});
            var yb=new RButton("NO");
            yb.click(()=>{this.remove();if(callback)callback();});
            this.onEnterKeydown(()=>{yb.click()});
        }
    }
    class RTextarea extends RWidget{
        constructor() {
            super("<textarea></textarea>");
        }
        val(arg){if(typeof arg!='undefined'){this.el.val(arg);return this;}else{return this.el.val();}}
    }
    class RImagearea extends RWidget{
        constructor() {
            super("<img>");
        }
    }
    class RWindow extends RWidget{
        constructor() {
            super();
            `<div style="box-shadow: ">`
            this.setSize(500,400);
            this.el[0].style+=`;position:fixed;display:flex;flex-flow:column`;
            this.shadow();
            this.handle=createElement('div').addClass('rwindow-handle').appendTo(this.el);
            this.handle[0].style+=';display:flex;min-height:20px;width:100%;background-color:orange;';
            // this.makeDraggable(this.handle);
            // this.simpleMakeResizable();
            this.contentBox=createElement('div').addClass('rwindow-contentbox').appendTo(this.el);
            this.contentBox[0].style+=`;display:flex;flex:1 0 auto;max-height:100vh;flex-flow:column;overflow:auto`;
            this.el.css('overflow','hidden');
            this.setScrollbar();
            this.bars={};
        }
        addBar(name,el){
            this.bars[name]=el;
            this.handle.after(el);
            return this;
        }
    }

    class RDiv extends RWidget{
        constructor() {
            super(createElement('div'));
        }
    }
    class RSimpleMenuBar extends RDiv{
        constructor() {
            super();
            this.flexRow();
        }
        addButtonMap(map){for(var key in map){this.addButton(key,map[key]);} return this;}
        addButton(text,onclick){new RButton(text,onclick).appendTo(this);return this;}
    }
    class RContentWidget extends RDiv{
        constructor() {
            super();
            this.contentBox=new RDiv().appendTo(this);
            this.menuBox=new RSimpleMenuBar().prependTo(this);
        }
        addMenu(){
            this.menuBox=new RSimpleMenuBar().prependTo(this);return this;
        }
    }
    class RLinkInput extends RDiv{
        constructor() {
            super();
        }
    }
    class RFileInputArea extends RContentWidget{
        constructor() {
            super();
            this.file_input=new RInput({'type':'file'}).appendTo(this.contentBox);
            this.submit_btn=new RButton('submit');
            this.menuBox.append(this.submit_btn);
        }
        success(func){this.submit_btn.click(()=>{
            var files=this.file_input.files();if(func)func(files);
        });return this;
        }
    }
    class RPowerInput extends RContentWidget{
        constructor() {
            super();
            this.shadow();
            this.contentBox.fullWidth().orange().fromCssString('height:10em');
            this.text_input=new RTextarea().fitParent().appendTo(this.contentBox).hide();
            this.html_input=new RDiv().editable().white().appendTo(this.contentBox).fitParent().hide();
            this.file_input=new RFileInputArea().shadow().appendTo(this.contentBox).hide();
            this.link_input=new RLinkInput().fitParent().appendTo(this.contentBox).hide();
            this.text_input.show();
            this.menuBox.addButtonMap({
                'plain-text': (e)=> {this.text_input.show();},
                'html':(e)=>{this.hideAll();this.html_input.show()},
                'file':(e)=>{this.hideAll();this.file_input.show()},
                'link':(e)=>{this.hideAll();this.link_input.show()}
            })
        }
        val(){
            if(this.text_input.visible){return this.text_input.val()}
            else if(this.html_input.visible){return  this.html_input.html()}
            else if(this.file_input.visible){return this.file_input.val()}
            else if(this.link_input.visible){return this.link_input.val()}
        }
        hideAll(){
            this.text_input.hide();
            this.html_input.hide();
            this.file_input.hide();
            this.link_input.hide();
            return this;
        }
    }
    class RColumnList extends RDiv{
        constructor() {
            super();
            this.flexColumm();
            this.contentBox=new RDiv();
            this.contentBox.flexColumm().appendTo(this);
        }
        reverse(){this.reverseFlexDirection();return this;}
        addLinkItem(text,href){var el=createElement('a').attr('href',href).html(text);this.addItem(el);return this;}
        addItem(content){
            var el=new RDiv();
            el.html(content);
            el.fromCssString('min-height:2em;padding:5px;');
            el.fullWidth();
            this.contentBox.append(el);
            return this;
        }
    }
    class RBoardApp extends RColumnList{
        constructor() {
            super();
            this.os=panjs.getDefaultOS();
            this.db=panjs.getDefaultDB();
            this.dbKey=wpjs.getRelativeUrl()+this.constructor.name;
            this.power_inut=new RPowerInput().prependTo(this);
            this.power_inut.menuBox.blue();
            this.power_inut.file_input.success((files)=>{
                this.os.uploadfiles(files,'./data/upload',()=>{
                    var fn='./data/upload/'+files[0].name;
                    var url=this.os.geturl(fn);
                    // console.log("url:",url);
                    this.addLinkItem(files[0].name,url);
                    this.save();
                })
            });
            this.load();
        }
        setData(data){
            this.db.set(this.dbKey,data);
        }
        getData(){
            // this.setData({'content':''});
            var data=this.db.get(this.dbKey);
            console.log("getData:",data)
            if(!data){data={};data.content='';this.setData(data)};
            return data;
        }
        load(){
            var data=this.getData();
            console.log("data:",data);
            this.contentBox.html(data.content);
        }
        save(){
            var data=this.getData();
            data.content=this.contentBox.html();
            console.log("set data:",data);
            this.setData(data);
            console.log("data_get:",this.getData());
        }
    }
    return{
        RWidget,RButton,RInput,RTextInput,RFileInput,
        RDialog,RMessagebox,RInputDialog,RListbox, RMenu,
        RDropdownMenu,RImagearea,RTextarea,RWindow,RPopupMenu,
        RDiv,RColumnList,RLinkInput,RSimpleMenuBar,RContentWidget,
        RPowerInput,RBoardApp,
        createElement,
    }
}();
