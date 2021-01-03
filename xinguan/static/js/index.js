
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

function denglucheck(event) {
    $.ajaxSettings.async = false;
    is_right = false
    str =decodeURIComponent($("#denglu").serialize())
    data = getObj(str)
    mima = data.mima
    data_res = {}
        dianzhulianxi= data.dianzhulianxi

      $.post("/jianyue/lifadian/denglu/",
          {
            "dianzhulianxi": dianzhulianxi,
            "mima": mima,
              "csrfmiddlewaretoken":$('[name="csrfmiddlewaretoken"]').val()
          },
          function (data) {
          data_res = data
      });

    if (data_res.status == 0 || data_res.status == 1){
                alert(data_res['msg']);
            }
            else {
                is_right = true
            }
        $.ajaxSettings.async = true;
                return  is_right
  }
function zhucecheck() {
    $.ajaxSettings.async = false;
    str =decodeURIComponent($("#zhuce").serialize())
    data = getObj(str)
    mima = data.mima
    is_right= false
      dianzhuming= data.dianzhuming
          shenfenzheng= data.shenfenzheng
            dianzhulianxi= data.dianzhulianxi
            dianming= data.dianming
            dizhi= data.dizhi
    mima2 = data.mima2
    if (mima !== mima2) {
      alert("对不起，您2次输入的密码不一致");
    }

    else if(!isChinaName(dianzhuming) || !isCardNo(shenfenzheng)||!isPhoneNo(dianzhulianxi) || !isMima(mima) ){
        return true
    }
    else {
      $.post("/jianyue/lifadian/zhuce/",
          {
            "dianzhuming": dianzhuming,
            "shenfenzheng": shenfenzheng,
            "dianzhulianxi": dianzhulianxi,
            "dianming": dianming,
            "dizhi": dizhi,
            "mima": mima,
             "csrfmiddlewaretoken":$('[name="csrfmiddlewaretoken"]').val(),
          },
          function (data) {
            data_res = data
      });
      if (data_res.status == 0||  data_res.status == -1 || data_res.status == 2){
          alert(data_res['msg']);
            }
            else {
                is_right = true
            }
    }
    $.ajaxSettings.async = true;
    return is_right

}
function xiugai() {
    $.ajaxSettings.async = false;
    var ziduan = window.ziduan
    var neirong = $("#xiugaineirong").val()

    if (ziduan == "shenfenzheng"){
        if (!isCardNo(neirong)){
            alert("格式错误")
            return false
        }
    }
    else if (ziduan == "dianzhuming"){
        if(!isChinaName(neirong)){
            alert("格式错误，请输入中文姓名")
            return false
        }
    }
    else if (ziduan=="dianzhulianxi"){
        if(!isPhoneNo(neirong)){
            alert("格式错误，请输入正确的电话号码")
            return false
        }
    }
    else if (ziduan=="mima"){
        if (!isMima(neirong)){
            alert("格式错误,请输入20位的字母或数字")
            return false
        }
    }

          $.post("/jianyue/lifadian/xiugai/",
          {

            "ziduan": ziduan,
            "neirong": neirong,
             "csrfmiddlewaretoken":$('[name="csrfmiddlewaretoken"]').val(),
          },
          function (data,status) {
                  alert(data['msg'])
              if (data["status"] ==1) {
                  $("#"+ziduan).parent().prev().text(neirong)
                  $(":contains('取消')").click()
              }
              else  if(status != "success"){
                  alert("修改失败")
              }
      });
    $.ajaxSettings.async = true
    return false
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

/*姓名身份证，手机号提交*/
function isChinaName(name) {
    var pattern = /^[\u4e00-\u9fa5]{2,}$/;
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

$(function(){
    $(".xiugai").click(function (e) {
        var id = $(this).attr("id")
        window.ziduan = id
        return true
    })
});