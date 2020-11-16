function wuzizengjia() {
    str =decodeURIComponent($("#wuzizengjia").serialize())
   $.ajaxSettings.async = false
    data =  getObj(str)

          $.post("zengjia.html",
          {

            "wuziming": data.wuziming,
            "wuzileixing": data.wuzileixing,
              "jinhuoshijian":data.jinhuoshijian,
              "shengyuliang":data.shengyuliang,
             "csrfmiddlewaretoken":$('[name="csrfmiddlewaretoken"]').val(),
          },
          function (data,status) {
              if (data["status"] ==1 || data['status'] == 0) {
                  alert(data["msg"])
                  $('#wuzizengjia')[0].reset()
              }
              else if (data["status"] == -1){
                  alert(data['msg'])
              }

              else  if(status != "success"){
                  alert("修改失败")
              }

      });
    $.ajaxSettings.async = true
    return false
}

$(document).ready(function(){
     $(".del").click(function () {
        the = $(this)
        wuziming = the.parents("tr").children("td").eq(0).text()
         wuzileixing = the.parents("tr").children("td").eq(1).text()
                   $.get("shanchu/",
          {

            "wuziming": wuziming,
            "wuzileixing": wuzileixing,
             "csrfmiddlewaretoken":$('[name="csrfmiddlewaretoken"]').val(),
          },
          function (data,status) {
              if (data["status"] ==1){
                  alert(data["msg"])
                  the.parents("tr").hide()
              }
              else {
                  alert("删除失败")
              }
        });
     })
    $(".chexiao").click(function() {
            row = $(this).parents("tr")
            $.get("chexiao/",
            {
                "lifashi_id":row.children("td").eq(0).text(),
            },
            function (data,status) {
                alert(data["msg"])
                if (data.status==1){
                    row.hide()
                }
            }
       )
    })

    $(".dizhi-fankui").click(function() {
            fankui = $(this).data("name")
            row = $(this).parents("tr")
            $.get("fankui/",
            {
                "lifashi_id":row.children("td").eq(0).text(),
                "fankui":fankui
            },
            function (data,status) {
                alert(data["msg"])
                if (data.status==1){
                    row.hide()
                }
            }
       )
    })

    $("body").on("click",".tupianshanchu", function() {
        the = $(this)
            file_name = the.prev("figure").find("img").attr("src").replace("/media/","")
            $.post(".",
            {
                "filename":file_name,
                "shanchu":'1',
                "csrfmiddlewaretoken":$('[name="csrfmiddlewaretoken"]').val(),
            },
            function (data,status) {
                if(data["status"] == "2"){
                    the.hide()
                    the.prev().remove()
                }
            }
       )
    })
    $("#search").click(function(){
        var txt=$("input[type=text]").val();
        col = $("select").val();
        $('tbody tr').hide()
        $('tbody tr ').each(function(){
                   $(this).children('td:eq('+col+'):contains("'+txt+'")').parent().show()
        })
    })
});


$('#anpai').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var lifashi_id = button.data('lifashi_id') // Extract info from data-* attributes
    $("#baocun").click(function () {
        str =decodeURIComponent($("#anpai_form").serialize())
    data =  getObj(str)
        $.post(".",
            {
                lifashi_id:lifashi_id,
                yonghu_id:data.yonghu_id,
                fuwu_id:data.fuwu_id,
                yuyueriqi:data.yuyueriqi,
                yuyueshijian:data.yuyueshijian,
                yuyuexiaohao:data.yuyuexiaohao,

                "csrfmiddlewaretoken":$('[name="csrfmiddlewaretoken"]').val(),
            },
            function (data,status) {
                alert(data["msg"])
                if (data.status==1){
                    $(":contains('取消')").click()
                    parent.location.reload()

                }
            }
       )
    })
    })

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
