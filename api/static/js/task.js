var edit = 0 // 0 表示为新建，1表示为编辑
var id = 0 // 任务id
$(function(){


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
         $.ajax({　　
             url: 'task_del',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 "id": id
             },
             　　success: function (data) {　　　　
                alert(data["msg"])
                 location.reload()
             },
             error: function (e) {
                 alert("失败")
                 location.reload()
             }
         })
     })
    validate()


    $(".btn-run").click(function(){
        $("#modal-operate").modal("show")
         $.ajax({　　
             url: 'task_run',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 "tid": $(this).parents("tr").attr("id")
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
                     location.reload()
                 }
            })
    })

    function NewTask() {
       $.ajax({　　
                url: 'task_new',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 "name": $("#name").val(),
                 },
             　　success: function (data) {
                   alert("新建成功")
                 location.reload()
                 },
                 error: function (e) {
                     alert("失败")
                     location.reload()
                 }
             })
    }
    function EditTask() {
       $.ajax({　　
             url: 'task_edit',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 "name": $("#name").val(),
                 "id": id
             },
             　　success: function (data) {
                   alert("编辑成功")
                    location.reload()
             },
             error: function (e) {
                 alert("失败")
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