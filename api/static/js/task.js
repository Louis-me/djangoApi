var edit = 0 // 0 表示为新建，1表示为编辑
var id = 0 // 任务id
$(function(){

    $("#nav-left ul li:eq(4) a").css("color", "red")

    $("#btn-task-new").click(function(){
        $("#modal-task").modal("show")
        edit = 0
    })
    $(".btn-edit").click(function(){
        $("#modal-task").modal("show")
        edit = 1
        id = $(this).parents("tr").attr("id")
         name = $(this).parents("td").prev().text()
        $("#name").val(name)
    })
     $(".btn-del").click(function () {
         id = $(this).parents("tr").attr("id")
         $("#modal-del").modal("show")
     })

     $("#btn-modal-confirm").click(function () {
        $.rpc.req("task_del","post",{"id": id},function(resp){
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
    validate()


    $(".btn-run").click(function(){
        $("#modal-operate").modal("show")
         $.rpc.req("task_run","post",{"tid": $(this).parents("tr").attr("id")},function(resp){
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

    function NewTask() {
        $.rpc.req("task_new","post",{"name":$("#name").val()},function(resp){
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
    function EditTask() {
        var data = {"name": $("#name").val(), "id": id}
        $.rpc.req("task_edit","post",data,function(resp){
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
                selectpicker: {required: true}
             },
            messages: {
                 name: {required: "请输入任务名"},
                 selectpicker: {required: "请选择模块"},
            },
            submitHandler: function (form) { //通过之后回调
                 if (edit == 0) {
                     NewTask()
                 } else {
                     EditTask()
                 }
             },
             invalidHandler: function (form, validator) {
                 return false;
             }
        });
   }

})