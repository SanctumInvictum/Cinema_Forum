

function set_display_menu(style, text) {
    let menu = document.getElementById('loggedMenu');
    document.getElementById('navbarDropdown').innerText = text;
    if (style.length === 0 ) {
        menu.removeAttribute("style");
    }  else{
         menu.style.display = style;
    }

}

// console.log(document.getElementById('signUpMenu').style.display = "none");

// показать юзернейм
function display_logger_user(username) {
        let signUpMenu = document.getElementById('signUpMenu').style.display = "none";
        set_display_menu("", username);
        console.log("ПОКАЗАТЬ МЕНЮ");
}

// убрать юзернейм
function undisplay_logger_user() {
        let signUpMenu = document.getElementById('signUpMenu').style.display = "";
        set_display_menu("none", "");
        console.log("СКРЫТЬ МЕНЮ");
}


function get_auth_token() {
    let url = '/auth/jwt/login';
    let username = modalEmailInput.value;
    let password = modalPasswordInput.value;

    return $.ajax({
        url: url,
        type: 'post',
        // headers: {"Content-Type": "application/x-www-form-urlencoded"},
        data: {'username': username, 'password': password },
        // data: {'username': 'chugun@gmail.com', 'password': '123456789'},
        beforeSend : function(xhr) {

        },
        success: function(xhr){
            console.log(xhr);
            console.log(document.cookie = `Authorization: Bearer ${xhr.access_token}`);
            console.log("token set");
            display_logger_user(username);
            set_userlog(1, username);

            console.log("Успешная авторизация");
        },
        error: function(error){
            console.log(`error: ${error}`);
        }
    });
}

function register_user(password) {
    let url = '/auth/register';
    let email = emailInput.value;
    let username = usernameInput.value;

    return $.ajax({
        url: url,
        type: 'post',
        dataType:"json",
        // headers: {"Content-Type": "application/json"},
        contentType: "application/json",
        data: JSON.stringify({ 'email': email, 'username': username, 'password': password}),
        success: function(result){
            console.log(result);
            console.log("Успешная регистрация");

        },
        error: function(error){
            console.log(`error: ${JSON.stringify(error)}`);
        }
    });
}

function logout() {
    set_userlog(0, "");
    undisplay_logger_user();
}

// установка доп инфы для отслеживания логирования пользователя
function set_userlog(status, username) {
    localStorage.setItem("loggin", status);
    localStorage.setItem("username", username);
}

//  авторизация по кнопке
document.getElementById('modalSignInBtn').onclick = function() {
    let result = get_auth_token();
    // console.log("Редирект");
    // window.location.href = "/home";
};

//  регистрация по кнопке
// document.getElementById('signUpBtn').onclick = function() {
//     let pass1 = password1Input.value;
//     let pass2 = password2Input.value;
//     console.log("sdfsd", pass1 === pass2);
//     if (pass1 === pass2) {
//         let password = pass1;
//
//         console.log(emailInput.value);
//         console.log(pass1);
//         let result = register_user(password);
//         console.log(result);
        // console.log("Редирект");
        // window.location.href = "/home";
    // }

// };


//  выход из учетки по кнопке
document.getElementById('logoutBtn').onclick = function() {
    let result = logout();
};


// при загрузке страницы определяет логгированную панель меню
window.onload = function (e) {
    console.log("cookie right now: ", document.cookie);
    console.log("localstorage now: ", localStorage);

    console.log(localStorage.getItem("loggin") === "0");
    console.log(localStorage);
    if (localStorage.getItem("loggin") === "0") {
        // set_display_menu("none", "");
        undisplay_logger_user();
    } else{
        // set_display_menu("", localStorage.getItem("username"));
        display_logger_user(localStorage.getItem("username"));
    }
}