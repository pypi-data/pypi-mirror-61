imviewjs=function () {
    var {QWindow, QMenubar} = winjs;
    var {genUid, isdefined} = wpjs;
    var {registerOpener, QDesktopApplication, QEvent} = sysjs;
    class ImageViewer extends QDesktopApplication{
        constructor(pan) {
            super();
            this.window.setTitle("ImageViewer");
            this.pan=pan;
        }
        init(){

        }
        show(){
            this.window.show();
        }
        hide(){
            this.window.hide();
        }
        openFile(arg1,location,filename){
            if($.isPlainObject(arg1)){
                this.pan=arg1.pan;
                this.location=arg1.location;
                this.filename=arg1.filename;
            }else {
                this.pan=arg1;
                this.location=location;
                this.filename=filename;
            }
            var url=this.pan.getUrl(this.location,this.filename);
            var content=`<img src="${url}" style="width:100%;height: 100%;">`;
            this.window.setContent(content);
            this.show();
        }
    }
    registerOpener('.jpg',ImageViewer);
    registerOpener('.png',ImageViewer);
    registerOpener('.gif',ImageViewer);
    return{
        ImageViewer:ImageViewer
    }
}();