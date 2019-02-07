 var id = 0
var edit = 0 //0 表示为新建，1表示为编辑

 $(function () {
     $("#nav-left ul li:eq(3) a").css("color", "red")

        validate(edit)
     $(".btn-edit").click(function () {
         edit = 1
         name = $(this).parents("td").prev().text()
         id = $(this).parents("tr").attr("id")
         $("#name").val(name)
         validate(edit)
     });
    $("#btn-new").click(function(){
        edit = 0
    })
     $(".btn-del").click(function () {
         id = $(this).parents("tr").attr("id")
         $("#modal-del").modal("show")
     })

     $("#btn-modal-confirm").click(function () {
        $.rpc.req("module_del","post",{"mid": id},function(resp){
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
     })

     function validate() {
         $("#m-form").validate({　　
             onsubmit: true, // 是否在提交是验证
             onfocusout: false, // 是否在获取焦点时验证
             onkeyup: false, // 是否在敲击键盘时验证
             rules: {　　　　 //规则
                 user: {　　 //要对应相对应的input中的name属性
                     required: true　　
                 },
             },
             messages: {　　　　 //验证错误信息
                 name: {　　　　
                     required: "请输入用户名"　　　　
                 },
             },
             submitHandler: function (form) { //通过之后回调
                 //进行ajax传值
                 if (edit == 0) {
                     NewModule()
                 } else {
                     EditModule()
                 }
             },
             invalidHandler: function (form, validator) {
                 return false;
             }
         });
     }

     function NewModule() {
        $.rpc.req("module_new","post",{"name": $("#name").val()},function(resp){
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
     function EditModule() {
        $.rpc.req("module_edit","post",{"name": $("#name").val(), "id": id},function(resp){
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