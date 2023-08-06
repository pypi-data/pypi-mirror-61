panjs = function () {
    var postJson = wpjs.postJson;
    var uploadFile = wpjs.uploadFile;

    class RemoteDB {
        constructor(url) {
            this.url = url;
            this.cmd_url = url + '/cmd';
        }

        execute(cmd,callback) {
            console.log(cmd);
            var res = postJson(this.cmd_url, cmd).responseJSON;
            console.log(res);
            if (res.success){
                if(callback){callback(res)};
                return res.data;
            }
            else {
                console.log("Cmd Error!", res);
                if(callback){callback(res)};
                return res.data;
            }
        }

        set(key, value) {
            var cmd = {cmd: {op: "set", params: {key: key, value: value}}};
            return this.execute(cmd);
        }
        add(key, value) {
            var cmd = {cmd: {op: "add", params: {key: key, value: value}}};
            return this.execute(cmd);
        }

        get(key) {
            var cmd = {cmd: {op: "get", params: {key: key}}};
            return this.execute(cmd);
        }

        delete(key) {
            var cmd = {cmd: {op: "delete", params: {key: key}}};
            return this.execute(cmd);
        }

        recover(ket, step) {
            var cmd = {cmd: {op: "recover", params: {key: key, step: step}}};
            return this.execute(cmd);
        }
    }

    class RemoteFS {
        constructor(url) {
            this.url = url;
            this.cmd_url = this.url + '/cmd';
            this.upload_url = this.url + '/upload';
        }

        execute(cmd,callback) {
            // console.log(cmd);
            var res = postJson(this.cmd_url, cmd).responseJSON;
            // console.log(res);
            if (res.success){
                if(callback){callback(res)};
                return res.data;
            }
            else {
                console.log("Cmd Error!", res);
                if(callback){callback(res)};
                return res.data;
            }
        }
        getUrl(location,name){
            var cmd = {cmd: {op: "getUrl", params: {location: location, name: name}}};
            return this.execute(cmd);
        }
        getDir(location, dirname) {
            var cmd = {cmd: {op: "getDir", params: {location: location, dirname: dirname}}};
            return this.execute(cmd);
        }

        getFile(location, filename) {
            var cmd = {cmd: {op: "getFile", params: {location: location, filename: filename}}};
            return this.execute(cmd);
        }

        newDir(location, dirname) {
            var cmd = {cmd: {op: "newDir", params: {location: location, dirname: dirname}}};
            return this.execute(cmd);
        }

        newFile(location, filename) {
            var cmd = {cmd: {op: "newFile", params: {location: location, filename: filename}}};
            return this.execute(cmd);
        }

        saveFile(location, filename, content) {
            var cmd = {cmd: {op: "saveFile", params: {location: location, filename: filename, content: content}}};
            return this.execute(cmd);
        }

        deleteFile(location, name) {
            var cmd = {cmd: {op: "delete", params: {location: location, name: name}}};
            return this.execute(cmd);
        }

        deleteDir(location, name) {
            var cmd = {cmd: {op: "delete", params: {location: location, name: name}}};
            return this.execute(cmd);
        }

        uploadFile(location, filename, file, callback) {
            var info = {
                info: {
                    location: location,
                    filename: filename,
                    file: file
                }
            };
            uploadFile(this.upload_url, file, info, (res) => {
                console.log(res);
                if(typeof callback!="undefined")callback(res);
                if (res.success) return res.data;
                else {
                    console.log("Error!", res);
                    return res.data;
                }
            });

        }
    }

    class Pan extends RemoteFS {
        constructor(url) {
            super(url);
        }

        pull(callback) {
            var cmd = {cmd: {op: "pull", params: {}}};
            return this.execute(cmd,callback);
        }

        push(callback) {
            var cmd = {cmd: {op: "push", params: {}}};
            return this.execute(cmd,callback);
        }
    }
    class OS {
        constructor(url) {
            this.url = url;
            if(url==='/')url='';
            this.cmd_url = url + '/cmd';
            this.upload_url = url + '/upload';
        }

        execute(cmd,callback) {
            // console.log(cmd);
            cmd={'cmd':cmd};
            var res = postJson(this.cmd_url, cmd).responseJSON;
            // console.log(res);
            if (res.success){
                if(callback){callback(res)}
                return res.data;
            }
            else {
                console.log("Cmd Error!", res);
                if(callback){callback(res)}
                return res.data;
            }
        }

        getfile(path,callback){
            var cmd={op:'getfile',params:[path]};
            var res=postJson(this.cmd_url,cmd);
            return res
        }
        dirname(path,callback){
            var cmd={op:'dirname',params:[path]};
            return this.execute(cmd,callback);
        }
        basename(path,callback){
            var cmd={op:'basename',params:[path]};
            return this.execute(cmd,callback);
        }
        standard_path(path,callback){
            var cmd={op:'_standard_path',params:[path]};
            return this.execute(cmd,callback);
        }
        relpath(root,path,callback){
            var cmd={op:'_relpath',params:[root,path]};
            return this.execute(cmd,callback);
        }
        getpage(path,callback){
            var cmd={op:'getpage',params:[path]};
            return this.execute(cmd,callback);
        }
        geturl(path,callback){
            var cmd={op:'geturl',params:[path]};
            return this.execute(cmd,callback);
        }
        glob(path,callback){
            var cmd={op:'glob',params:[path]};
            return this.execute(cmd,callback);
        }
        info(path,callback){
            var cmd={op:'info',params:[path]};
            return this.execute(cmd,callback);
        }
        tranverse_info(path,depth=-1,callback){
            var cmd={op:'tranverse_info',params:[path,depth]};
            return this.execute(cmd,callback);
        }
        read(path,callback){
            var cmd={op:'read',params:[path]};
            return this.execute(cmd,callback);
        }
        write(path,s,callback){
            var cmd={op:'write',params:[path,s]};
            return this.execute(cmd,callback);
        }
        newfile(path,callback){
            var cmd={op:'newfile',params:[path]};
            return this.execute(cmd,callback);
        }
        writefile(path,s,callback){
            var cmd={op:'writefile',params:[path,s]};
            return this.execute(cmd,callback);
        }
        exists(path,callback){
            var cmd={op:'exists',params:[path]};
            return this.execute(cmd,callback);
        }
        isdir(path,callback){
            var cmd={op:'isdir',params:[path]};
            return this.execute(cmd,callback);
        }
        isfile(path,callback){
            var cmd={op:'exists',params:[path]};
            return this.execute(cmd,callback);
        }
        islink(path,callback){
            var cmd={op:'exists',params:[path]};
            return this.execute(cmd,callback);
        }
        ismount(path,callback){
            var cmd={op:'exists',params:[path]};
            return this.execute(cmd,callback);
        }
        listdir(path,callback){
            var cmd={op:'listdir',params:[path]};
            return this.execute(cmd,callback);
        }
        remove(path,callback){
            var cmd={op:'remove',params:[path]};
            return this.execute(cmd,callback);
        }
        rmtree(path,callback){
            var cmd={op:'rmtree',params:[path]};
            return this.execute(cmd,callback);
        }
        mkdir(path,callback){
            var cmd={op:'mkdir',params:[path]};
            return this.execute(cmd,callback);
        }
        makedirs(path,callback){
            var cmd={op:'makedirs',params:[path]};
            return this.execute(cmd,callback);
        }
        copy(src,dst,callback){
            var cmd={op:'copy',params:[src,dst]};
            return this.execute(cmd,callback);
        }
        copydir(src,dst,callback){
            var cmd={op:'copydir',params:[src,dst]};
            return this.execute(cmd,callback);
        }
        rename(src,dst,callback){
            var cmd={op:'rename',params:[src,dst]};
            return this.execute(cmd,callback);
        }
        move(src,dst,callback){
            var cmd={op:'move',params:[src,dst]};
            return this.execute(cmd,callback);
        }
        uploadfiles(files, dst, callback) {
            var formdata=new FormData();
            for(var i=0;i<files.length;i++){
                var file=files[i];
                formdata.append(file.name,file);
            }
            formdata.append("dst",dst);
            var xhr=new XMLHttpRequest();
            xhr.open('POST',this.upload_url,true);
            xhr.send(formdata);
            xhr.addEventListener('loadend',(e)=>{
                if(xhr.status===200){
                    var res=JSON.parse(xhr.responseText);
                    if(callback)callback(res);
                }
            });
        }
    }

    var getDefaultDB=function () {
        return new RemoteDB('/db');
    };
    var getDefaultFS=function () {
        return new RemoteFS('/fs');
    };
    var getDefaultOS=function () {
      return new OS('/os')
    };
    return {
        getDefaultOS,
        getDefaultFS,
        getDefaultDB,
        OS,
        RemoteDB: RemoteDB,
        RemoteFS: RemoteFS,
        Pan: Pan
    }
}();