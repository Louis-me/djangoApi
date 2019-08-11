 var id = 0
var edit = 0 //0 表示为新建，1表示为编辑

 $(function () {
     $("#nav-left ul li:eq(6) a").css("color", "red")
      validate()
     $(".btn-edit").click(function () {
         edit = 1
         name = $(this).parents("td").prev().text()
         id = $(this).parents("tr").attr("id")
         $("#name").val($.trim(name))
     });
     $("#btn-new").click(function() {
        edit = 0
     });

     $(".btn-del").click(function () {
         id = $(this).parents("tr").attr("id")
         $("#modal-del").modal("show")
     })

     $("#btn-modal-confirm").click(function () {
        $.rpc.req("../../case_del","post",{"cid": id},function(resp){
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
                     required: "请输入用例名"　　　　
                 },
             },
             submitHandler: function (form) { //通过之后回调
                 if (edit == 0) {
                     NewCase()
                 } else {
                     EditCase()
                 }
             },
             invalidHandler: function (form, validator) {
                 return false;
             }
         });
     }

     function NewCase() {
           $.rpc.req("../../case_new","post",{"name": $("#name").val(), "mid": $("#mid").val()},function(resp){
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

     function EditCase() {
          $.rpc.req("../../case_edit","post",{"name": $("#name").val(), "cid": id},function(resp){
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