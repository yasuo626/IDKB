
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





function show_etc_menu(){
    menu=document.getElementById('etc_menu');
    if(menu.style.display=='block'){
        menu.style.display='none';
    }else{
       menu.style.display='block';
    }

}
function showRegisterForm() {
    document.getElementById('login_form').style.display = 'none';
    document.getElementById('register_form').style.display = 'block';
}
function response_logout(responseData) {
    document.location.reload();
}
function logout(){
    var formdata = new FormData();
    formdata.append('method','logout');
    api_request(formdata,api_user,response_logout);
}

function response_login(responseData) {
    if(responseData.state=='0'){
        document.getElementById('login_response_msg').style.display='inline-block';
        document.getElementById('login_response_msg').innerText="login success";
        document.getElementById('login_loader').style.display = 'none';
        setTimeout(() => {
            document.getElementById('fullscreen_shadow').style.display='none';
            document.getElementById('login_container').style.display='none';
        }, 500);
    }else{
        document.getElementById('login_response_msg').style.display='inline-block';
        document.getElementById('login_response_msg').innerText=`${responseData.error_info}`;
        document.getElementById('login_loader').style.display = 'none';
    }
}
function login() {
    document.getElementById('login_loader').style.display = 'inline-block';
    document.getElementById('login_response_msg').style.display = 'none';

    username=document.getElementById('login_username').value;
    password=document.getElementById('login_password').value;

    var formdata = new FormData();
    formdata.append('method','login');
    formdata.append('username',username);
    formdata.append('password',password);
    api_request(formdata,api_user,response_login);
}
function response_register(responseData) {
    // 在这里对响应数据进行处理
    if(responseData.state=='0'){
        document.getElementById('register_response_msg').style.display='inline-block';
        document.getElementById('register_response_msg').innerText="register success";
        document.getElementById('register_loader').style.display = 'none';
        setTimeout(() => {
            document.getElementById('register_form').style.display = 'none';
            document.getElementById('login_form').style.display = 'block';
        }, 500);
    }else{
        document.getElementById('register_response_msg').style.display='inline-block';
        document.getElementById('register_response_msg').innerText=`${responseData.error_info}`;
        document.getElementById('register_loader').style.display = 'none';
    }
}
function register() {

    document.getElementById('register_loader').style.display = 'inline-block';
    document.getElementById('register_response_msg').style.display = 'none';

    username=document.getElementById('register_username').value;
    email=document.getElementById('register_email').value;
    password=document.getElementById('register_password').value;

    var formdata = new FormData();
    formdata.append('method','register');
    formdata.append('username',username);
    formdata.append('email',email);
    formdata.append('password',password);

    api_request(formdata,api_user,response_register);
}

function login_required(){
        require_login=document.getElementById('require_login').innerText
        is_login=document.getElementById('is_login').innerText
        username=document.getElementById('get_username').innerText

        if(require_login==1){
            if(is_login==1){
                document.getElementById('main_container').innerText+=`${username}`;
            }else{
                document.getElementById('fullscreen_shadow').style.display='block';
                document.getElementById('login_container').style.display='block';
            }
        }
}
login_required()