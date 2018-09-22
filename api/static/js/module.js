 var id = 0
var edit = 0 //0 表示为新建，1表示为编辑

 $(function () {
        validate(edit)
     $(".btn-edit").click(function () {
         edit = 1
         name = $(this).parents("td").prev().text()
         id = $(this).parents("tr").attr("id")
         $("#name").val(name)
         validate(edit)
     });
     $(".btn-del").click(function () {
         id = $(this).parents("tr").attr("id")
         $("#modal-del").modal("show")
     })
     $("#btn-run").click(function(){
        $("#modal-operate").modal("show")
         $.ajax({　　
             url: 'run',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 "mid": $(this).parents("tr").attr("id")
             },
             　　success: function (data) {
                    if (data["code"] == 0) {
                        alert(data["msg"])
                         location.reload()
                    } else {
                        alert(data["msg"])
                    }
             },
             error: function (e) {
                 alert("失败")
//                 location.reload()
             }
         })
     })
     $("#btn-modal-confirm").click(function () {
         $.ajax({　　
             url: 'module_del',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 "mid": id
             },
             　　success: function (data) {　　　　
//                alert(data["msg"])
                 location.reload()
             },
             error: function (e) {
                 alert("失败")
//                 location.reload()
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
         $.ajax({　　
             url: 'module_new',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 "name": $("#name").val(),
             },
             　　success: function (data) {　　　　 //要执行的代码
                    if (data["code"] == 0) {
                         alert("新建成功")
                         location.reload()
                    } else {
                      alert("新建失败"+ data["msg"])
                    }
             },
             error: function (e) {
                 alert("失败")
                 location.reload()
             }
         })
     }

     function EditModule() {
         $.ajax({　　
             url: 'module_edit',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 name: $("#name").val(),
                 id: id
             },
             　　success: function (data) {　　　　 //要执行的代码
                 location.reload()
             },
             error: function (e) {
                 alert("失败")
                 location.reload()
             }
         })
     }
 })