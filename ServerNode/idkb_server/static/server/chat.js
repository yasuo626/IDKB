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









var main_block=document.getElementById("main_block");
var switch_kb_enable=document.getElementById("switch_kb_enable");


function empty_messages(){
    while (main_block.firstChild) {
      main_block.removeChild(main_block.firstChild);
    }
}
function gobottom(element){
    element.scrollTop = element.scrollHeight;
}
function create_msg(role,msg,parent){
    var m=document.createElement("div");
    var ico=document.createElement("div");
    var content=document.createElement('div');

    if (role=='user'){
        m.setAttribute('class','chat_client_msg');
        ico.setAttribute('class',"chat_client_ico");
        content.setAttribute('class',"chat_client_content");
        content.innerText=msg;
    }
    else if (role=='assistant'){
        m.setAttribute('class','chat_agent_msg');
        ico.setAttribute('class',"chat_agent_ico");
        content.setAttribute('class',"chat_agent_content");
        continuesdisplayText(msg,content);
    }
    else if (role=='info'){
        m.setAttribute('class','chat_info_msg');
        ico.setAttribute('class',"chat_info_ico");
        content.setAttribute('class',"chat_info_content");
        content.innerText=msg;
    }
    else{
        console.log("error role");
        return ;
    }
    m.appendChild(ico);
    m.appendChild(content);
    parent.appendChild(m);
    gobottom(main_block);
}
function continuesdisplayText(msg, elem) {
  let index = 0;

  // 使用setInterval每隔一定时间执行一次回调函数
  const intervalId = setInterval(() => {
    // 每次回调函数执行时，将元素的 innerText 设置为 msg 的前 index 个字符
    elem.innerText = msg.substring(0, index);

    // 增加 index 的值
    index++;

    // 如果 index 大于等于 msg 的长度，则已经显示完所有字符，清除定时器
    if (index > msg.length) {
      clearInterval(intervalId);
    }
  }, 5); // 每次回调函数执行的时间间隔，单位为毫秒
}


function chat_detail(){
}
function response_chat_delete(responsedata){
    if(responsedata.state=='0'){
        location.reload();
    }else{
        alert(responsedata.error_info)
    }

}
function chat_delete(){
    var chatname=document.getElementById("current_chatname").innerText;
    var formdata = new FormData();
    formdata.append('chatname',chatname);
    formdata.append('username',document.getElementById('get_username').innerText);
    formdata.append('method','delete');
    api_request(formdata,api_krdroid_chat,response_chat_delete);

}
function response_chat_load(responsedata){
    empty_messages()
    if(responsedata.state=='0'){
        for (msg of responsedata.history) {
            create_msg(msg['role'],msg['content'],main_block);
        }
    }else{
        alert(responsedata.error_info)
    }
}
function chat_load(chatname){
    document.getElementById("current_chatname").innerText=chatname;
    var formdata = new FormData();
    formdata.append('chatname',chatname);
    formdata.append('username',document.getElementById('get_username').innerText);
    formdata.append('method','load');
    api_request(formdata,api_krdroid_chat,response_chat_load);
}
function response_chat_get(responsedata){
    var chat_list_ul=document.getElementById("chat_list_ul");
    while (chat_list_ul.firstChild) {
      chat_list_ul.removeChild(chat_list_ul.firstChild);
    }
    if(responsedata.state=='0'){

        for (chat of responsedata.chat_list) {
            var chat_li=document.createElement("li");
            chat_li.setAttribute('id',chat);
            chat_li.innerText=chat;
            chat_list_ul.append(chat_li);
            chat_li.addEventListener("click", function(event) {
                chat_load(event.target.id);
            });
        }
        var chat_li=document.createElement("div");
        chat_li.setAttribute('class','chat_list_add');
        chat_li.addEventListener("click",chat_new );
        chat_li.innerText='+';
        chat_list_ul.append(chat_li);
        for (chat of responsedata.chat_list) {
            chat_load(chat);
            return ;
        }
    }else{
        alert(responsedata.error_info)
    }
}
function chat_get(){
    var formdata = new FormData();
    formdata.append('username',document.getElementById('get_username').innerText);
    formdata.append('method','get');
    api_request(formdata,api_krdroid_chat,response_chat_get);
}
chat_get()

function chat_clear(){
    empty_messages();
}


function chat_new_form_close(){
    document.getElementById('chat_new_form').style.display='none';
    absolute_container.style.display='none';
}
function response_kb_get(responsedata){
    if(responsedata.state=='0'){
        var kb_select=document.getElementById("kb_select");
        for (kb of responsedata.kb_list) {
            var kb_option=document.createElement("option");
            kb_option.setAttribute('id',kb['name']);
            kb_option.value=kb['name'];
            kb_option.innerText=kb['name'];
            kb_select.append(kb_option);
        }
    }else{
        alert(responsedata.error_info)
    }
}
function chat_new() {
    absolute_container.style.display='block';
    document.getElementById('chat_new_form').style.display='block';
    var formdata = new FormData();
    formdata.append('username',document.getElementById('get_username').innerText);
    api_request(formdata,api_krdroid_kb_get,response_kb_get);
}
function response_chat_new_submit(responsedata){
    if(responsedata.state=='0'){
        document.getElementById('chat_new_loader').style.display = 'none';
        document.getElementById('chat_new_response_msg').style.display='inline-block';
        document.getElementById('chat_new_response_msg').innerText="create success";
        setTimeout(() => {
            location.reload();
        }, 1000);
    }else{
        document.getElementById('chat_new_loader').style.display = 'none';
        document.getElementById('chat_new_response_msg').style.display='inline-block';
        document.getElementById('chat_new_response_msg').innerText=`${responsedata.error_info}`;
    }
}
function chat_new_submit() {

    var max_context=parseInt(document.getElementById('chat_new_form_max_context').value);
    var chatname=document.getElementById('chat_new_form_name').value;
    if(isNaN(max_context) ){
        alert('max context must be a number');
        return;
    }
    if(max_context<1||max_context>5){
        alert('max context must be in [1,5]');
        return;
    }
    if(chatname.indexOf('.') != -1){
        alert('chatname only allow alphabet,number,_');
        return ;
    }

    document.getElementById('chat_new_loader').style.display = 'inline-block';
    var formdata = new FormData();
    formdata.append('username',document.getElementById('get_username').innerText);
    formdata.append('method','create');
    formdata.append('kbname',document.getElementById('kb_select').value);
    formdata.append('chatname',chatname);
    formdata.append('max_context',max_context);
    formdata.append('system_template',document.getElementById('chat_new_form_system_template').value);
    formdata.append('question_template',document.getElementById('chat_new_form_question_template').value);

    api_request(formdata,api_krdroid_chat,response_chat_new_submit);
}



function response_chat_chat(responsedata){
    var refs="\n\nreferences:\n";
    console.log(responsedata);
    for(ref of responsedata.refs){
        refs+=ref+";\n";
    }

    if(responsedata.state=='0'){
        create_msg('assistant',responsedata.reply+refs,main_block);
    }else{
        create_msg('info',responsedata.error_info,main_block);
    }
    document.getElementById('chat_chat').disabled=false;
    document.getElementById('chat_chat').style.opacity='1.0';

}
function chat_chat(){
    var message=document.getElementById('chat_input').value;
    if(message==''){
        alert('input can not be empty');
        return ;
    }
    create_msg('user',message,main_block);
    document.getElementById('chat_chat').disabled=true;
    document.getElementById('chat_chat').style.opacity='0.5';
    var formdata = new FormData();
    formdata.append('username',document.getElementById('get_username').innerText);
    formdata.append('chatname',document.getElementById('current_chatname').innerText);
    formdata.append('message',message);
    formdata.append('method','chat');
    formdata.append('msgtype','text');
    console.log(switch_kb_enable.checked? 1:0)
    formdata.append('kb_enable',switch_kb_enable.checked? 1:0);
    api_request(formdata,api_krdroid_chat,response_chat_chat);
    document.getElementById('chat_input').value='';

}


