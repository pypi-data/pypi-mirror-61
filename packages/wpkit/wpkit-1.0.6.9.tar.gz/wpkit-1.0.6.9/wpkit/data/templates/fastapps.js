fastappjs = function () {
    var {
        getDefaultDB,
    } = panjs;
    var {
        getRelativeUrl, getDefaultUserName
    } = wpjs;
    var{
        Switch
    }=apputiljs;
    class BaseFastApp {
        constructor() {
            this.db = getDefaultDB();
            this.dbKey = getDefaultUserName() + getRelativeUrl();
            this.showSwitch=new Switch(()=>{this.show()},()=>{this.hide()});
        }
        bindShowSwitch(key){
            this.showSwitch.bindKey({
                reverse:key
            });
            return this;
        }
        getEl(){
            return this.el;
        }
        appendTo(el) {
            $(document).ready(() => {
                el = el || $('body');
                el.append(this.el);
            })

        }
        show(){
            this.getEl().show();
        }
        hide(){
            this.getEl().hide();
        }

        find(sel) {
            return this.el.find(sel);
        }

        setData(obj) {
            this.db.set(this.dbKey, obj);
        }

        getData() {
            return this.db.get(this.dbKey);
        }
    }
    class JSCLI extends BaseFastApp{
        constructor(props) {
            super(props);
            var source=`
            <div style="position: fixed;top:0;">
            <button class="run-btn" style="float:left;">RUN</button>
            <textarea class="code-area" style="width:100vw;min-width:200px;min-height: 200px;resize: both"></textarea>
</div>
            `;
            this.el=$(source).addClass('js-cli');
            this.run_btn=this.find('.run-btn');
            this.code_area=this.find('.code-area');
            this.run_btn.click((e)=>{
                var code=this.code_area.val();
                console.log(eval(code))
            });
            this.appendTo();
            this.showSwitch.bindKey({
                reverse:'ctrl+alt+r'
            }).turnOff();
            jwerty.key('ctrl+shift+enter',(e)=>{
                this.run_btn.click();
            });
            wpjs.indentWhenTab(this.code_area);
            jwerty.key('ctrl+s',(e)=>{
                this.setData({code:this.code_area.val()});
                console.log("saved.");
            });
            this.code_area.val(this.getData().code);


        }

    }
    class WhiteBoard extends BaseFastApp {
        constructor() {
            super();
            var source = `<div style="position: fixed;left:0;top:0;right:0;bottom:0;height: 100%;width: 100%;z-index: 1025;background-color: white;border: gainsboro solid 1px">
        <div class="view-area" contenteditable="true" style="overflow:auto;height: 100%;width: 100%;border:2px solid #00c6ff"></div>

    <textarea class="code-area" contenteditable="true"
              style="height: 100%;width: 100%;border:2px solid #00c6ff ;display: none"></textarea>
        </div>`;
            this.el = $(source).addClass('whiteboard');

            var view_area = this.find('.view-area');
            var code_area = this.find('.code-area');
            this.view_area = view_area;
            this.code_area = code_area;
            this.bindShowSwitch('ctrl+b');
            this.showSwitch.turnOff();
            this.editSwicth = new Switch((e) => {
                if(e)e.preventDefault();
                view_area.attr('contenteditable', 'true');
                view_area.focus();
            }, (e) => {
                if(e)e.preventDefault();
                view_area.attr('contenteditable', 'false');
            }).bindKey({
                reverse: 'ctrl+e'
            }).turnOff();
            this.codeSwitch = new Switch(() => {
                var content = view_area.html();
                code_area.val(content);
                view_area.hide();
                code_area.show();
                code_area.focus();
            }, () => {
                var content = code_area.val();
                view_area.html(content);
                code_area.hide();
                view_area.show();
            }).bindKey({
                reverse: 'ctrl+m'
            });

            jwerty.key('ctrl+s', (e) => {
                e.preventDefault();
                var data = this.getData();
                data.content = this.view_area.html();
                this.setData(data);
            });
            wpjs.indentWhenTab(this.el);
            this.init();
        }

        appendTo(el) {
            $(document).ready(() => {
                el = el || $('body');
                el.append(this.el);
            })

        }

        init() {
            var data = this.getData();
            if (!data) {
                this.setData({content: ''});
            } else {
                this.view_area.html(data.content);
            }
            this.appendTo();
        }
    }


    return {
        JSCLI,
        BaseFastApp,
        WhiteBoard
    }
}();
var {
    BaseFastApp,
    WhiteBoard,
    JSCLI,
} = fastappjs;
whiteboard = new WhiteBoard();
jscli=new JSCLI();