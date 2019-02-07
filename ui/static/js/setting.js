 $(function () {
      $("#nav-left ul li:eq(2) a").css("color", "red")
       validate()
     function validate() {
         $("#m-form").validate({　　
             onsubmit: true,
             onfocusout: false,
             onkeyup: false,
             rules: {　　　　 //规则
                login_url: {required: true},
                home_url: {required: true},
             },
             messages: {
                 login_url: {required: "请输入登录url"},
                 home_url:{required: "请输入主页url"},
             },
             submitHandler: function (form) { //通过之后回调
                 EditCase()
             },
             invalidHandler: function (form, validator) {
                 return false;
             }
         });
     }
     function EditCase() {
        data = {"home_url": $("#home_url").val(), "login_url":  $("#login_url").val()}
        $.rpc.req("setting_edit","post",data,function(resp){
            if (resp && resp["code"] == 0) {
                    alert("成功")
                     location.reload()
               } else {
                     if (resp && resp["code"] ) {
                         alert(resp.msg)
                     } else {
                        alert("请求失败")
                     }
                     location.reload()
               }
            })
        }
   })



