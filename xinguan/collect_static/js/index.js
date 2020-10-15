
function cambiar_login() {
  document.querySelector('.cont_forms').className = "cont_forms cont_forms_active_login";  
document.querySelector('.cont_form_login').style.display = "block";
document.querySelector('.cont_form_sign_up').style.opacity = "0";               

setTimeout(function(){  document.querySelector('.cont_form_login').style.opacity = "1"; },400);  
  
setTimeout(function(){    
document.querySelector('.cont_form_sign_up').style.display = "none";
},200);  
  }

function cambiar_sign_up(at) {
  document.querySelector('.cont_forms').className = "cont_forms cont_forms_active_sign_up";
  document.querySelector('.cont_form_sign_up').style.display = "block";
document.querySelector('.cont_form_login').style.opacity = "0";
  
setTimeout(function(){  document.querySelector('.cont_form_sign_up').style.opacity = "1";
},100);  

setTimeout(function(){   document.querySelector('.cont_form_login').style.display = "none";
},400);  


}    

function ocultar_login_sign_up() {

document.querySelector('.cont_forms').className = "cont_forms";  
document.querySelector('.cont_form_sign_up').style.opacity = "0";               
document.querySelector('.cont_form_login').style.opacity = "0"; 

setTimeout(function(){
document.querySelector('.cont_form_sign_up').style.display = "none";
document.querySelector('.cont_form_login').style.display = "none";
},500);  
}


//注册反馈
function getObj(str) {
			let arr = str.split('&');
			let obj = {};
			arr.map(function(item) {
				let tempArr = item.split('=');
				obj[tempArr[0]] = tempArr[1];
			});
			console.log(obj); // {name: "freely", age: "20", city: "beijing", job: "fe"}
		return obj
}
$(document).ready(function() {
  $("#zhucesub").click(function () {
    str =$("#zhuce").serialize()
    data = getObj(str)
    mima = data.mima
      dianzhuming= data.dianzhuming
          shenfenzheng= data.shenfenzheng
            dianzhulianxi= data.dianzhulianxi
            dianming= data.dianming
            dizhi= data.dizhi
    mima2 = data.mima2
      alert(isChinaName(decodeURIComponent(dianzhuming)))
    if (mima !== mima2) {
      alert("对不起，您2次输入的密码不一致");
    }

    else if(!isChinaName(decodeURIComponent(dianzhuming)) || !isCardNo(shenfenzheng)||!isPhoneNo(dianzhulianxi) || !isMima(mima) ){
        return true
    }
    else {
      $.post("/jianyue/lifadian/zhuce/",
          {
            "dianzhuming": dianming,
            "shenfenzheng": shenfenzheng,
            "dianzhulianxi": dianzhulianxi,
            "dianming": dianming,
            "dizhi": dizhi,
            "mima": mima,
             "csrfmiddlewaretoken":$('[name="csrfmiddlewaretoken"]').val()
          },
          function (data,status) {
            alert("数据: \n" + data['msg'] + "\n状态: " + status);
            // $(location).attr('href', 'www.baidu.com');重定向操作
      });
    }
  });
});

/*姓名身份证，手机号提交*/
function isChinaName(name) {
    var pattern = /^[\u4e00-\u9fa5]{2,4}$/;
    return pattern.test(name);
}


// 验证身份证
function isCardNo(card) {
    var pattern = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;
    return pattern.test(card);
}

// 验证手机号
function isPhoneNo(phone) {
    var pattern = /^1[34578]\d{9}$/;
    return pattern.test(phone);
}
function isMima(mima) {
    var pattern = /^[\d\w_]{6,20}$/;
    return pattern.test(mima);
}
