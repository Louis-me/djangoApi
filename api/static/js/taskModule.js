var edit = 0 // 0 表示为新建，1表示为编辑
var id = 0 // 关联的模块id
$(function(){


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
         $.ajax({　　
             url: '../../task_del',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 "tmid": id
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

    function NewTaskModule() {
       $.ajax({　　
                url: '../../task_module_new',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 "name": $("#sel-module").find("option:selected").text(),
                 "mid": $("#sel-module").val(),
                 "tid": $("#tid").val()
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
    function EditTaskModule() {
       $.ajax({　　
             url: '../../task_module_edit',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 "name": $("#sel-module").find("option:selected").text(),
                 "tmid": id,
                  "mid": $("#sel-module").val(),
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