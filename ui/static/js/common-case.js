 var id = 0
var edit = 0 //0 表示为新建，1表示为编辑

 $(function () {
     $("#nav-left ul li:eq(5) a").css("color", "red")
      validate()

    $("#btn-new").click(function() {
        edit = 0
     })

     $(".btn-edit").click(function () {
         edit = 1
         name = $.trim($(this).parents("td").prev().text())
         id = $(this).parents("tr").attr("id")
         $("#name").val(name)
     });

     $(".btn-del").click(function () {
         id = $(this).parents("tr").attr("id")
         $("#modal-del").modal("show")
     })

     $("#btn-modal-confirm").click(function () {
        $.rpc.req("common_case_del","post",{"id": id},function(resp){
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
                 name: {　　 //要对应相对应的input中的name属性
                     required: true　　
                 },
             },
             messages: {　　　　 //验证错误信息
                 name: {　　　　
                     required: "请输入用例名"　　　　
                 },
             },
             submitHandler: function (form) { //通过之后回调
                 //进行ajax传值
                 if (edit == 0) {
                     CommonCaseNew()
                 } else {
                     CommonCaseEdit()
                 }
             },
             invalidHandler: function (form, validator) {
                 return false;
             }
         });
     }

     function CommonCaseNew() {
           $.rpc.req("common_case_new","post",{"name": $("#name").val()},function(resp){
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

     function CommonCaseEdit() {
          $.rpc.req("common_case_edit","post",{"name": $("#name").val(), "id": id},function(resp){
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