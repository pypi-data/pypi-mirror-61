wpjs = function () {

    console.log('my.js loaded.');
    var debug = true;
    var tlog = function (text) {
        if (debug) {
            console.log(message = "tlog message:");
            console.log(text);
        }
    };
    var isdefined = function (obj) {
        return typeof obj != "undefined";
    };
    var postJson = function (url, data) {
        return $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: url,
            data: JSON.stringify(data),
            async: false,
            dataType: "json"
        });
    };
    var uploadFile = function (url, file, JSONdata, callback) {
        var data = new FormData();
        data.append('file', file);
        // data.append()
        if (typeof data != "undefined") {
            var keys = Object.keys(JSONdata);
            for (var i in keys) {
                var k = keys[i];
                // console.log(k,JSONdata[k]);
                data.append(k, JSON.stringify(JSONdata[k]));
                // data.append(k,JSONdata[k]);
            }
        }

        // data.append('data',data);
        // data.append('location','./');
        // data.append()
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        //xhr.setRequestHeader("Content-Type", "multipart\/form-data;"); //千万不能要这一句，否则后台request.files读不到file
        xhr.send(data);

        xhr.addEventListener('loadend', function () {
            console.log("xhr.status:", xhr.status)
            if (xhr.status === 200) {
                var res_json = JSON.parse(xhr.responseText);
                console.log(res_json);
                if (typeof callback != "undefined") callback(res_json);
            }
        }, false);
    };
    // document.querySelector('input').addEventListener('keydown', function (e) {
    // if (e.key === 9) {
    //     e.preventDefault();
    // }
    // });
    const disableKeydown = function (el, keyCode) {
        $(el).keydown((e) => {
            // console.log("keydown:",e);
            if (e.keyCode === keyCode) {
                e.preventDefault();
                // console.log("preventDefault")
            }
        });
    };
    const disableTab = function (el) {
        disableKeydown(el, 9);
    };
    const indentWhenTab = function (el) {
        $(el).on("keydown", (e) => {
            if (e.keyCode === 9) {
                e.preventDefault();
                var target = e.target;
                // console.log("target:", target);
                var start = target.selectionStart;
                var end = target.selectionEnd;
                // set textarea value to: text before caret + tab + text after caret
                $(target).val($(target).val().substring(0, start)
                    + "\t"
                    + $(target).val().substring(end));

                // put caret at right position again
                target.selectionStart =
                    target.selectionEnd = start + 1;
            }
        })
    };
    var disable_ctrl_s = function () {
        document.onkeydown = function (e) {
            e = e || window.event;//Get event

            if (!e.ctrlKey) return;

            var code = e.which || e.keyCode;//Get key code

            switch (code) {
                case 83://Block Ctrl+S
                case 87://Block Ctrl+W -- Not work in Chrome and new Firefox
                    e.preventDefault();
                    e.stopPropagation();
                    break;
            }
        };
    };

    var T = {
        NOT_FOUND: "NOT_FOUND",
        NOT_EXISTS: "NOT_EXISTS",
        NO_VALUE: "NO_VALUE",
        NOT_IMPLEMENTED: "NOT_IMPLEMENTED",
        NOT_ALLOWED: "NOT_ALLOWED",
        EMPTY: "EMPTY",
        NO_SUCH_VALUE: "NO_SUCH_VALUE",
        NO_SUCH_ATTR: "NO_SUCH_ATTR",
        NOT_GIVEN: "NOT_GIVEN",
        FILE: "FILE",
        DIR: "DIR",
        LINK: "LINK",
        MOUNT: "MOUNT"
    };
    var genUid = function () {
        return Math.random().toString().slice(2, -1);
    };

    var simpleMakeResizable = function (el) {
        el.style.resize = 'both';
        el.style.overflow = 'auto';
    };
    var makeDraggable = function (el, head) {
        // Make the DIV element draggable:
        head = head || el;
        el = $(el)[0];
        head = $(head)[0];
        // console.log("head:",head);
        dragElement(el);

        function dragElement(elmnt) {
            elmnt.style.position = 'absolute';
            var ofx = 0, ofy = 0;
            var ox1, ox2, oy1, oy2 = 0;
            if (head) {
                // if present, the header is where you move the DIV from:
                head.onmousedown = dragMouseDown;
            } else {
                // otherwise, move the DIV from anywhere inside the DIV:
                elmnt.onmousedown = dragMouseDown;
            }

            function dragMouseDown(e) {
                e = e || window.event;
                e.preventDefault();
                ox1 = elmnt.offsetLeft;
                oy1 = elmnt.offsetTop;
                ox2 = e.clientX;
                oy2 = e.clientY;
                document.onmouseup = closeDragElement;
                document.onmousemove = elementDrag;
            }

            function elementDrag(e) {
                e = e || window.event;
                e.preventDefault();
                // console.log(e)
                // console.log("e.x,y:",e.clientX,e.clientY)
                // console.log(window.innerWidth,window.innerHeight)
                if (e.clientX <= 0 || e.clientY <= 0 || e.clientX >= window.innerWidth || e.clientY >= window.innerHeight) {
                    return null
                }
                ofx = e.clientX - ox2;
                ofy = e.clientY - oy2;
                elmnt.style.top = (oy1 + ofy) + "px";
                elmnt.style.left = (ox1 + ofx) + "px";
                res = {
                    ox1: ox1, oy1: oy1, ox2: ox2, oy2: oy2, x: e.clientX, y: e.clientY, ofx: ofx, ofy: ofy,
                    offsetTop: elmnt.offsetTop, offsetLeft: elmnt.offsetLeft
                }
                // console.log(res)
            }

            function closeDragElement() {
                // stop moving when mouse button is released:
                document.onmouseup = null;
                document.onmousemove = null;
            }
        }
    };
    var getDefaultUserName = function () {
        return 'admin';
    };

    var getRelativeUrl=function (path) {
        var url = document.location.toString();
        url=path||url;
        var arrUrl = url.split("//");

        var start = arrUrl[1].indexOf("/");
        var relUrl = arrUrl[1].substring(start);//stop省略，截取从start开始到结尾的所有字符
        if (relUrl.indexOf("?") != -1) {
            relUrl = relUrl.split("?")[0];
        }
        return relUrl;
    };
    return {
        getRelativeUrl,
        getDefaultUserName,
        genUid: genUid,
        disableKeydown,
        disableTab,
        indentWhenTab,
        disable_ctrl_s: disable_ctrl_s,
        T: T,
        simpleMakeResizable: simpleMakeResizable,
        makeDraggable: makeDraggable,

        isdefined: isdefined,
        postJson: postJson,
        uploadFile: uploadFile
    }
}();