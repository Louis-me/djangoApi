var edit = 0 // 0 表示为新建，1表示为编辑
var id = 0 // 关联的模块id
$(function(){
    $("#nav-left ul li:eq(5) a").css("color", "red")
    $("#btn-task-new-module").click(function(){
        $("#modal-task-module").modal("show")
        edit = 0
    })
    $(".btn-edit").click(function(){
        $("#modal-task-module").modal("show")
        edit = 1
        id = $(this).parents("tr").attr("id")
        $("#sel-module").val($(this).parents("tr").attr("mid"))
    })

    validate()
     $(".btn-del").click(function () {
         id = $(this).parents("tr").attr("id")
         $("#modal-del").modal("show")
     })

     $("#btn-modal-confirm").click(function () {
        $.rpc.req("../../task_module_del","post",{"tmid": id},function(resp){
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

    function NewTaskModule() {
        var data = {　　　　
                 "name": $("#sel-module").find("option:selected").text(),
                 "mid": $("#sel-module").val(),
                 "tid": $("#tid").val()
                 }
         $.rpc.req("../../task_module_new","post",data,function(resp){
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
    function EditTaskModule() {
         var data = {　　　　
                  "name": $("#sel-module").find("option:selected").text(),
                 "tmid": id,
                  "mid": $("#sel-module").val()
                 }
         $.rpc.req("../../task_module_edit","post",data,function(resp){
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

   function validate() {
        $("#m-form").validate({　　
            onsubmit: true, // 是否在提交是验证
            onfocusout: false, // 是否在获取焦点时验证
            onkeyup: false, // 是否在敲击键盘时验证
            rules: {　　　　 //规则
                name: {required: true},
             },
            messages: {
                 name: {required: "请输入任务名"},
            },
            submitHandler: function (form) { //通过之后回调
                 if (edit == 0) {
                     NewTaskModule()
                 } else {
                     EditTaskModule()
                 }
             },
             invalidHandler: function (form, validator) {
                 return false;
             }
        });
   }
})