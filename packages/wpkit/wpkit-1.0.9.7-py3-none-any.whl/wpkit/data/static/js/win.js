class QWindow {
        constructor(el) {
            this.el=el;
            //resizable
            el.resizable({
                addClass:false
            });
            //draggable
            el.draggable().click(function () {
                $(this).draggable({disabled: false});
            }).dblclick(function () {
                $(this).draggable({disabled: true});
            });
            // console.log($('#editor-style'))
            this.init();
        }
        init(){
            var style= this.style();
            var content=this.el.html();
            this.el.html('');
            console.log('html',this.el.html())
            this.el.append($(style));
            this.el.addClass('window');
            this.el.append($(this.html()));
            this.el.find('.window-inner').html(content);
        }

        html(){
           return `
        <div class="window-header"></div>
        <div class="window-body">
            <div  class="window-inner">
                this is window inner.
            </div>
        </div>
            `

        }
        style(){
            var style={
                window:``
            }
            var style=`
            <style id="editor-style">
    .window {
        background-color: #ff4a37;
        width: 400px;
        height: 400px;
        /*max-width: 400px;*/
        /*max-height: 400px;*/
        display: flex;
        flex-flow: column;
    }
    .window-header {
        flex: 0 0 30px;
        background-color: deepskyblue;
        width: 100%;
    }

    .window-body {
        flex: auto;
        overflow: auto;
        padding: 5px;
        width: 100%;
        background-color: #f1f1f1;

    }

    .window-inner {
        box-sizing: border-box;
        overflow: auto;
        flex: 1 0 auto;
        height: 100%;
        width: 100%;
        background-color: white;
        padding: 5px;
    }
</style>
            `
            return style;
        }
    }