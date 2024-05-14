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










function file_detail_close(){
    document.getElementById('file_detail').style.display='none';
    absolute_container.style.display='none';

}
function response_file_get_detail(responsedata){
    if(responsedata.state=='0'){
        absolute_container.style.display='block';
        document.getElementById('file_detail_name').innerText=responsedata.detail['name']
        document.getElementById('file_detail_type').innerText=responsedata.detail['type']
        document.getElementById('file_detail_size').innerText=responsedata.detail['size']
        document.getElementById('file_detail_api').innerText=responsedata.detail['api']
        document.getElementById('file_detail_embedding_model').innerText=responsedata.detail['embedding_model']
        document.getElementById('file_detail_embeddings_size').innerText=responsedata.detail['embeddings_size']
        document.getElementById('file_detail_count').innerText=responsedata.detail['count']
        document.getElementById('file_detail_create_time').innerText=responsedata.detail['create_time']
        document.getElementById('file_detail_update_time').innerText=responsedata.detail['update_time']
        document.getElementById('file_detail').style.display='block';
    }else{
        alert(responsedata.error_info)
    }
}
function file_add_li(name,type,size,api,embedding_model,create_time){
    var file_list=document.getElementById("file_list");
    var file_li=document.createElement("li");
    file_li.setAttribute('class','file_list_li');
    file_li.setAttribute('id',name);

    var file_li_name=document.createElement("span");
    var file_li_type=document.createElement("span");
    var file_li_size=document.createElement("span");
    var file_li_api=document.createElement("span");
    var file_li_embedding_model=document.createElement("span");
    var file_li_create_time=document.createElement("span");
    file_li_name.innerText=name;
    file_li_type.innerText=type;
    file_li_size.innerText=size;
    file_li_api.innerText=api;
    file_li_embedding_model.innerText=embedding_model;
    file_li_create_time.innerText=create_time;
    file_li.appendChild(file_li_name)
    file_li.appendChild(file_li_type)
    file_li.appendChild(file_li_size)
    file_li.appendChild(file_li_api)
    file_li.appendChild(file_li_embedding_model)
    file_li.appendChild(file_li_create_time)

    file_list.appendChild(file_li);

    file_li.addEventListener("click", function(event) {
        var filename=event.currentTarget.id
        var username=document.getElementById('get_username').innerText
        var formdata = new FormData();
        formdata.append('filename',filename);
        formdata.append('username',username);
        api_request(formdata,api_krdroid_file_get_detail,response_file_get_detail);
        console.log(formdata);
    });
}
function response_file_get(responsedata){
    if(responsedata.state=='0'){
        for (file of responsedata.files) {
            file_add_li(file['name'],file['type'],file['size'],file['api'],file['embedding_model'],file['create_time'])
        }
    }else{
        alert(responsedata.error_info)
    }
}
function file_get(){
    var username=document.getElementById('get_username').innerText;
    var formdata = new FormData();
    formdata.append('username',username);
    api_request(formdata,api_krdroid_file_get,response_file_get);
}
file_get()

function openFileUploader() {
    document.getElementById('add_file_upload').click();
}
function displaySelectedFiles() {
    const fileList = document.getElementById('add_file_upload').files;
    const listContainer = document.getElementById('add_file_list');
    listContainer.innerHTML = ''; // 清空列表

    var num=fileList.length;
    if(num>3){
        num=3;
    }
    for (let i = 0; i < num; i++) {
        const listItem = document.createElement('li');
        listItem.textContent = fileList[i].name;
        listContainer.appendChild(listItem);
    }
    const listItem = document.createElement('li');
    listItem.textContent = `total ${fileList.length} files`;
    listContainer.appendChild(listItem);
}


function response_file_upload(responsedata){
    document.getElementById('upload_loader').style.display='none';
    document.getElementById('upload_response_msg').style.display='inline-block';
    if(responsedata.state=='0'){
        var allStatesAreZero=true;
        for (let i = 0; i < responsedata.file_states.length; i++) {
          if (responsedata.file_states[i]['state'] !== 0) {
            allStatesAreZero = false;
            break;
          }
        }
        if(allStatesAreZero){
            document.getElementById('upload_response_msg').innerText="upload success";
             setTimeout(() => {
                document.getElementById('file_upload_form').style.display='none';
                absolute_container.style.display='none';
                location.reload();
            }, 1000);
        }else{
            error_info=""
            responsedata.file_states.forEach(item => {
                error_info+=`${item.name}:${item.error_info}; `
            });
            document.getElementById('upload_response_msg').innerText=error_info;

            document.getElementById('file_upload_submit_but').disable=false;
            document.getElementById('file_upload_submit_but').style.opacity="1.0";
        }
    }else{
        document.getElementById('upload_response_msg').innerText=`${responsedata.error_info}`;
        document.getElementById('upload_loader').style.display = 'none';
    }
}
function file_upload_form_close(){
    document.getElementById('file_upload_form').style.display='none';
    absolute_container.style.display='none';
}
function file_upload(){
    if(document.getElementById('file_upload_submit_but').disable){
        return ;
    }

    document.getElementById('file_upload_submit_but').disable=true;
    document.getElementById('file_upload_submit_but').style.opacity="0.3";

    var username=document.getElementById('get_username').innerText;
    var api=document.getElementById('api_select').value;
    var embedding_model=document.getElementById('embedding_model_select').value;
    var files=document.getElementById('add_file_upload').files;
    var formdata = new FormData();
    for (var i = 0; i < files.length; i++) {
        formdata.append('files', files[i]);
    }
    formdata.append('username', username);
    formdata.append('api', api);
    formdata.append('embedding_model', embedding_model);

    api_request(formdata,api_krdroid_file_upload,response_file_upload);
    document.getElementById('upload_loader').style.display='inline-block';
}
function file_add(){
    absolute_container.style.display='block';
    document.getElementById('file_upload_form').style.display='block';
}


function file_delete_form_close(){
    document.getElementById('file_delete_form').style.display='none';
    absolute_container.style.display='none';
}
function file_delete() {

    absolute_container.style.display='block';
    document.getElementById('file_delete_form').style.display='block';
    var file_delete_list = document.getElementById('file_delete_list');
    while (file_delete_list.firstChild) {
      file_delete_list.removeChild(file_delete_list.firstChild);
    }

    var file_list = document.getElementById('file_list');
    var file_list_items = file_list.querySelectorAll('li');
    file_list_items.forEach(function(item) {
        const fileName = item.querySelector('span').innerText;
        const li = document.createElement('li');
        li.innerText = fileName;
        file_delete_list.appendChild(li);
    });

    const fileListItems = file_delete_list.getElementsByTagName('li');
    for (let i = 0; i < fileListItems.length; i++) {
        fileListItems[i].addEventListener('click', function() {
      // 切换选中样式
      this.classList.toggle('selected');
    });
    }
}
function response_file_delete_submit(responsedata){
    if(responsedata.state=='0'){
        var allStatesAreZero=true;
        for (let i = 0; i < responsedata.file_states.length; i++) {
          if (responsedata.file_states[i]['state'] !== 0) {
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
            responsedata.file_states.forEach(item => {
                error_info+=`${item.name}:${item.error_info}; \n`
            });
            alert(error_info);
        }
    }else{
        alert(responsedata.error_info);
    }
}
function file_delete_submit() {
    const selectedItems = document.querySelectorAll('.file_delete_list li.selected');
    var formdata = new FormData();
    var files=[];
    for (let i = 0; i < selectedItems.length; i++) {
        files.push(selectedItems[i].innerText);
    }
    if(files.length<1){
        alert('not file selected ');
        return ;
    }
    for(file of files){
         formdata.append('files',file);
    }
    formdata.append('username',document.getElementById('get_username').innerText);
    api_request(formdata,api_krdroid_file_delete,response_file_delete_submit);
}
function file_delete_select_all() {
  but=document.getElementById('file_delete_select_all');
  const fileDeleteList = document.getElementById('file_delete_list');
    const fileListItems = fileDeleteList.getElementsByTagName('li');
  if(but.innerText=="select all"){
        but.innerText="cancle";
        for (let i = 0; i < fileListItems.length; i++) {
        fileListItems[i].classList.add('selected');
      }
  }else{
        but.innerText="select all";
      for (let i = 0; i < fileListItems.length; i++) {
        fileListItems[i].classList.remove('selected');
      }
  }
}











