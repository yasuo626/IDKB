function api_request(formData, apiUrl, callback) {

    var xhr = new XMLHttpRequest();
    xhr.open('POST', apiUrl, true);
    xhr.onload = function() {
        if (xhr.status === 200) {
            var jsonResponse = JSON.parse(xhr.responseText);
            callback(jsonResponse)
            // 在这里处理解析后的 JSON 数据
            console.log(jsonResponse);
        } else {
            // 请求失败
            alert('Request failed with status:', xhr.status);
            console.error('Request failed with status:', xhr.status);
        }
    };
    xhr.send(formData);
}

var idkb_api_url=document.getElementById('api_url').innerText
var local_url='https://idkb.aidroid.top'
var home_url=local_url+'/idkb/'

// 示例数据和 API 地址
var api_user_login = local_url+'/wmc/apiuser';
var api_user_logout = local_url+'/wmc/apiuser';
var api_user_logoff = local_url+'/wmc/apiuser';
var api_user_register = local_url+'/wmc/apiuser';
var api_user = local_url+'/wmc/apiuser';

var api_krdroid_file_upload = idkb_api_url+'/file_upload';
var api_krdroid_file_delete = idkb_api_url+'/file_delete';
var api_krdroid_kb_create = idkb_api_url+'/kb_create';
var api_krdroid_kb_delete = idkb_api_url+'/kb_delete';
var api_krdroid_kb_add_files = idkb_api_url+'/kb_add_files';
var api_krdroid_kb_get_files = idkb_api_url+'/kb_get_files';
var api_krdroid_kb_drop_files = idkb_api_url+'/kb_drop_files';
var api_krdroid_chat= idkb_api_url+'/chat';

var api_krdroid_file_get = idkb_api_url+'/file_get';
var api_krdroid_file_get_detail = idkb_api_url+'/file_get_detail';
var api_krdroid_kb_get = idkb_api_url+'/kb_get';
var api_krdroid_kb_get_detail = idkb_api_url+'/kb_get_detail';
var api_krdroid_kb_get_valid_files = idkb_api_url+'/kb_get_valid_files';




var absolute_container=document.getElementById('absolute_container')



var current_kb_name=''; //point to current select_kb

function response_logout(responseData) {
    // document.location.reload();
    window.location.href = home_url;
}
function logout(){
    var formdata = new FormData();
    formdata.append('method','logout');
    api_request(formdata,api_user,response_logout);
}
function show_etc_menu(){
    menu=document.getElementById('etc_menu');

    if(menu.style.display=='block'){
        menu.style.display='none';
        absolute_container.style.display='none';
    }else{
       menu.style.display='block';
        absolute_container.style.display='block';
    }

}


function kb_detail_close(){
    document.getElementById('kb_detail').style.display='none';
    absolute_container.style.display='none';

}
function response_kb_get_detail(responsedata){
    if(responsedata.state=='0'){
        absolute_container.style.display='block';
        document.getElementById('kb_detail_name').innerText=responsedata.detail['name']
        document.getElementById('kb_detail_api').innerText=responsedata.detail['api']
        document.getElementById('kb_detail_llm').innerText=responsedata.detail['llm']
        document.getElementById('kb_detail_embedding_model').innerText=responsedata.detail['embedding_model']
        document.getElementById('kb_detail_reference').innerText=responsedata.detail['reference']
        document.getElementById('kb_detail_create_time').innerText=responsedata.detail['create_time']
        document.getElementById('kb_detail_update_time').innerText=responsedata.detail['update_time']
        document.getElementById('kb_detail').style.display='block';
    }else{
        alert(responsedata.error_info)
    }
}
function kb_add_li(name,api,llm,embedding_model){
    var kb_list=document.getElementById("kb_list");
    var kb_li=document.createElement("li");
    kb_li.setAttribute('class','kb_list_li');
    kb_li.setAttribute('id',name);

    var kb_li_name=document.createElement("span");
    var kb_li_api=document.createElement("span");
    var kb_li_llm=document.createElement("span");
    var kb_li_embedding_model=document.createElement("span");
    kb_li_name.innerText=name;
    kb_li_api.innerText=api;
    kb_li_llm.innerText=llm;
    kb_li_embedding_model.innerText=embedding_model;
    kb_li.appendChild(kb_li_name)
    kb_li.appendChild(kb_li_api)
    kb_li.appendChild(kb_li_llm)
    kb_li.appendChild(kb_li_embedding_model)

    kb_list.appendChild(kb_li);

    kb_li.addEventListener("click", function(event) {
        var kbname=event.currentTarget.id;
        current_kb_name=kbname;
        var username=document.getElementById('get_username').innerText;
        var formdata = new FormData();
        formdata.append('kbname',kbname);
        formdata.append('username',username);
        api_request(formdata,api_krdroid_kb_get_detail,response_kb_get_detail);
    });
}
function response_kb_get(responsedata){
    if(responsedata.state=='0'){
        for (kb of responsedata.kb_list) {
            kb_add_li(kb['name'],kb['api'],kb['llm'],kb['embedding_model']);
        }
    }else{
        alert(responsedata.error_info)
    }
}
function kb_get(){
    var username=document.getElementById('get_username').innerText;
    var formdata = new FormData();
    formdata.append('username',username);
    api_request(formdata,api_krdroid_kb_get,response_kb_get);
}
kb_get()

function clear_list(list){
    while (list.firstChild) {
      list.removeChild(list.firstChild);
    }
}

function response_kb_create_submit(responsedata){
    document.getElementById('create_loader').style.display='none';
    document.getElementById('create_response_msg').style.display='inline-block';
    if(responsedata.state=='0'){
        var allStatesAreZero=true;
        for (let i = 0; i < responsedata.length; i++) {
          if (responsedata[i].state !== '0') {
            allStatesAreZero = false;
            break;
          }
        }
        if(allStatesAreZero){
            document.getElementById('create_response_msg').innerText="create success";
             setTimeout(() => {
                document.getElementById('kb_create_form').style.display='none';
                absolute_container.style.display='none';
                location.reload();
            }, 1000);
        }else{
            error_info=""
            responsedata.forEach(item => {
                error_info+=`${item.name}:${item.error_info}; `
            });
            document.getElementById('create_response_msg').innerText=error_info;
        }
    }else{
        document.getElementById('create_response_msg').innerText=`${responsedata.error_info}`;
        document.getElementById('create_loader').style.display = 'none';
    }
}
function kb_create_form_close(){
    document.getElementById('kb_create_form').style.display='none';
    absolute_container.style.display='none';
}
function kb_create_submit(){
    var username=document.getElementById('get_username').innerText;
    var kbname=document.getElementById('kb_create_form_kbname').value;
    if(kbname.indexOf('.') != -1){
        alert('kbname only allow alphabet,number,_');
        return ;
    }
    if(kbname==''){
        alert("kbname not empty");
        return ;
    }

    var api=document.getElementById('api_select').value;
    var llm=document.getElementById('llm_select').value;
    var embedding_model=document.getElementById('embedding_model_select').value;
    var formdata = new FormData();
    formdata.append('username', username);
    formdata.append('kbname', kbname);
    formdata.append('api', api);
    formdata.append('llm', llm);
    formdata.append('embedding_model', embedding_model);
    console.log(formdata)
    api_request(formdata,api_krdroid_kb_create,response_kb_create_submit);
    document.getElementById('create_loader').style.display='inline-block';
}
function kb_create(){
    absolute_container.style.display='block';
    document.getElementById('kb_create_form').style.display='block';
}


function kb_delete_form_close(){
    document.getElementById('kb_delete_form').style.display='none';
    absolute_container.style.display='none';
}
function kb_delete() {

    absolute_container.style.display='block';
    document.getElementById('kb_delete_form').style.display='block';
    var kb_delete_list = document.getElementById('kb_delete_list');
    clear_list(kb_delete_list);

    var kb_list = document.getElementById('kb_list');
    var kb_list_items = kb_list.querySelectorAll('li');
    kb_list_items.forEach(function(item) {
        const kbName = item.querySelector('span').innerText;
        const li = document.createElement('li');
        li.innerText = kbName;
        kb_delete_list.appendChild(li);
    });

    const kbListItems = kb_delete_list.getElementsByTagName('li');
    for (let i = 0; i < kbListItems.length; i++) {
        kbListItems[i].addEventListener('click', function() {
      // 切换选中样式
      this.classList.toggle('selected');
    });
    }
}
function response_kb_delete_submit(responsedata){
    if(responsedata.state=='0'){
        var allStatesAreZero=true;
        for (let i = 0; i < responsedata.length; i++) {
          if (responsedata[i].state !== '0') {
            allStatesAreZero = false;
            break;
          }
        }
        if(allStatesAreZero){
            setTimeout(() => {
                location.reload();
            }, 1000);
        }else{
            error_info=""
            responsedata.forEach(item => {
                error_info+=`${item.name}:${item.error_info}; \n`
            });
            alert(error_info);
        }
    }else{
        alert(responsedata.error_info);
    }
}
function kb_delete_submit() {
    const selectedItems = document.querySelectorAll('.kb_delete_list li.selected');
    var formdata = new FormData();
    var kbs=[]
    for (let i = 0; i < selectedItems.length; i++) {
        kbs.push(selectedItems[i].innerText);
    }
    if(kbs.length!=1){
        alert('only allow 1 kb selected ');
        return ;
    }
    formdata.append('kbname',kbs[0]);
    formdata.append('username',document.getElementById('get_username').innerText);
    api_request(formdata,api_krdroid_kb_delete,response_kb_delete_submit);
}


function kb_files_operate_close(){
    document.getElementById('kb_files_operate_form').style.display='none';
    absolute_container.style.display='none';
}
function response_kb_files_operate(responsedata){
    if(responsedata.state=='0'){
        var kb_files_list=document.getElementById("kb_files_list");
        clear_list(kb_files_list);
        responsedata.files.forEach(function(file) {
            const li = document.createElement('li');
            li.innerText =file;
            kb_files_list.appendChild(li);
        });

        const kbListItems = kb_files_list.getElementsByTagName('li');
        for (let i = 0; i < kbListItems.length; i++) {
            kbListItems[i].addEventListener('click', function() {
          // 切换选中样式
          this.classList.toggle('selected');
        });
        }
    }else{
        alert(responsedata.error_info);
    }
}
function kb_files_operate(){
    kb_detail_close();
    absolute_container.style.display='block';
    document.getElementById('kb_files_operate_form').style.display='block';

    var formdata = new FormData();
    formdata.append('username',document.getElementById('get_username').innerText);
    formdata.append('kbname',current_kb_name);

    api_request(formdata,api_krdroid_kb_get_files,response_kb_files_operate);
}


function kb_files_add_close(){
    document.getElementById('kb_files_add_form').style.display='none';
    absolute_container.style.display='none';
}
function response_kb_files_add(responsedata){
    if(responsedata.state=='0'){
        var kb_files_list=document.getElementById("kb_files_add_list");
        clear_list(kb_files_list);

        responsedata.files.forEach(function(file) {
            const li = document.createElement('li');
            li.innerText =file;
            kb_files_list.appendChild(li);
        });

        const kbListItems = kb_files_list.getElementsByTagName('li');
        for (let i = 0; i < kbListItems.length; i++) {
            kbListItems[i].addEventListener('click', function() {
          // 切换选中样式
          this.classList.toggle('selected');
        });
        }
    }else{
        alert(responsedata.error_info);
    }
}
function kb_files_add(){
    kb_files_operate_close();
    absolute_container.style.display='block';
    document.getElementById('kb_files_add_form').style.display='block';

    var formdata = new FormData();
    formdata.append('username',document.getElementById('get_username').innerText);
    formdata.append('kbname',current_kb_name);

    api_request(formdata,api_krdroid_kb_get_valid_files,response_kb_files_add);
}

function response_kb_add_submit(responsedata){
    if(responsedata.state=='0'){
        document.location.reload();
    }else{
        alert(responsedata.error_info);
        document.getElementById('kb_files_add_submit_but').disable=false;
        document.getElementById('kb_files_add_submit_but').style.opacity="1.0";
}
}
function kb_files_add_submit(){

    if(document.getElementById('kb_files_add_submit_but').disable){
        return ;
    }

    const selectedItems = document.getElementById('kb_files_add_list').querySelectorAll('.kb_files_list li.selected');
    var formdata = new FormData();
    var files=[]
    for (let i = 0; i < selectedItems.length; i++) {
        files.push(selectedItems[i].innerText);
    }
    if(files.length<1){
        alert('at least 1 file selected ');
        return ;
    }

    document.getElementById('kb_files_add_submit_but').disable=true;
    document.getElementById('kb_files_add_submit_but').style.opacity="0.3";
    for(file of files){
         formdata.append('files',file);
    }
    formdata.append('kbname',current_kb_name);
    formdata.append('username',document.getElementById('get_username').innerText);
    api_request(formdata,api_krdroid_kb_add_files,response_kb_add_submit);

}



function kb_files_drop_close(){
    document.getElementById('kb_files_drop_form').style.display='none';
    absolute_container.style.display='none';
}
function response_kb_files_drop(responsedata){
    if(responsedata.state=='0'){
        var kb_files_list=document.getElementById("kb_files_drop_list");
        clear_list(kb_files_list);
        responsedata.files.forEach(function(file) {
            const li = document.createElement('li');
            li.innerText =file;
            kb_files_list.appendChild(li);
        });

        const kbListItems = kb_files_list.getElementsByTagName('li');
        for (let i = 0; i < kbListItems.length; i++) {
            kbListItems[i].addEventListener('click', function() {
          // 切换选中样式
          this.classList.toggle('selected');
        });
        }
    }else{
        alert(responsedata.error_info);
    }
}
function kb_files_drop(){
    kb_files_operate_close();
    absolute_container.style.display='block';
    document.getElementById('kb_files_drop_form').style.display='block';

    var formdata = new FormData();
    formdata.append('username',document.getElementById('get_username').innerText);
    formdata.append('kbname',current_kb_name);

    api_request(formdata,api_krdroid_kb_get_files,response_kb_files_drop);
}
function response_kb_drop_submit(responsedata){
    if(responsedata.state=='0'){
        document.location.reload();
        }else{
            alert(responsedata.error_info);
            document.getElementById('kb_files_drop_submit_but').disable=false;
            document.getElementById('kb_files_drop_submit_but').style.opacity="1.0";
    }
}
function kb_files_drop_submit(){

    if(document.getElementById('kb_files_drop_submit_but').disable){
        return ;
    }
    const selectedItems = document.getElementById('kb_files_drop_list').querySelectorAll('.kb_files_list li.selected');
    var formdata = new FormData();
    var files=[]
    for (let i = 0; i < selectedItems.length; i++) {
        files.push(selectedItems[i].innerText);
    }
    if(files.length<1){
        alert('at least 1 file selected ');
        return ;
    }

    document.getElementById('kb_files_drop_submit_but').disable=true;
    document.getElementById('kb_files_drop_submit_but').style.opacity="0.3";

    for(file of files){
         formdata.append('files',file);
    }
    formdata.append('kbname',current_kb_name);
    formdata.append('username',document.getElementById('get_username').innerText);
    api_request(formdata,api_krdroid_kb_drop_files,response_kb_drop_submit);


}









