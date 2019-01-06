var edit = 0 // 0 表示为新建，1表示为编辑
var id = 0

 $(function () {
     function isJSON(str) {
        if (typeof str == 'string') {
            try {
                var obj=JSON.parse(str);
                if(typeof obj == 'object' && obj ){
                    return true;
                }else{
                    return false;
                }
            } catch(e) {
                console.log('error：'+str+'!!!'+e);
                return false;
            }
        }
    }
    $("#btn-module-new").click(function(){
        $("#modal-case").modal("show")
        $("#url").val($("#curl").val())
        $("#name").val($("#cname").val())
         $("#sel-pro").val($("#cpro").val())
         $("#sel-method").val($("#cmethod").val())
         $("#params").val($("#cparams").val())
         $("#hope").val($("#chope").val())
    })
    // 模糊生成用例
    $("#btn-fuzz-batch").click(function(){
        if ($(".table-striped>tbody>tr:eq(0)").attr("id")) {
            alert("请先删除模块用例")
            return
        }
        $("#modal-operate").modal("show")

            $.ajax({　　
             url: '../../../batch_fuzz',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 "cid": $("#cid").val()
             },
             　　success: function (data) {
                 if (data["code"] == 0) {
                     location.reload()
                 }
             },
             error: function (e) {
                 alert("暂时只支持{}开头的json")
                 location.reload()
             }
         })

    })
     $(".btn-edit").click(function () {
         edit = 1
          id = $(this).parents("tr").attr("id")
         name = $(this).parents("td").prevAll(":eq(5)").text()
         id = $(this).parents("tr").attr("id")
         pro = $(this).parents("td").prevAll(":eq(4)").text()
         url = $(this).parents("td").prevAll(":eq(3)").text()
         method = $(this).parents("td").prevAll(":eq(2)").text()
         param = $(this).parents("td").prevAll(":eq(1)").text()
         hope = $(this).parents("td").prevAll(":eq(0)").text()
         $("#name").val(name)
         $("#sel-pro").val(pro)
         $("#url").val($.trim(url))
         $("#sel-method").val(method)
         $("#params").val($.trim(param))
         $("#hope").val($.trim(hope))
         validate(edit)
     });
     $(".btn-del").click(function () {
         id = $(this).parents("tr").attr("id")
         $("#modal-del").modal("show")
     })
     $("#btn-modal-confirm").click(function () {
         $.ajax({　　
             url: '../../../fuzz_del',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 "fid": id
             },
             　　success: function (data) {
                 if (data["code"] == 0) {
                     location.reload()
                 }
             },
             error: function (e) {
                 alert("失败")
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
                name: {required: true},
                url: {required: true},
                params: {required: true},

             },
             messages: {
                 name: {required: "请输入用例名"},
                 ur: {required: "请输入url"},
                 params:{required: "请输入入参"},
             },
             submitHandler: function (form) { //通过之后回调
                 //进行ajax传值
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
     validate(edit)

     function NewCase() {
        if (!isJSON($("#params").val())) {
        alert("请填入正确入参的json")
        return
        }
        if ($("#hope").val()!="" && !(isJSON($("#hope").val()))) {
        alert("请填入期望值json")
        return
        }

         $.ajax({　　
             url: '../../../fuzz_new',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 "name": $("#name").val(),
                 "url":  $.trim($("#url").val()),
                 "method": $("#sel-method").val(),
                 "protocol":$("#sel-pro").val(),
                 "params":  $.trim($("#params").val()),
                 "hope":  $.trim($("#hope").val()),
                 "cid": $("#cid").val()
             },
             　　success: function (data) {
                   alert("新建用例成功")
                 location.reload()
             },
             error: function (e) {
                 alert("失败")
                 location.reload()
             }
         })
     }

     function EditCase() {
         $.ajax({　　
             url: '../../../fuzz_edit',
             　　type: "post",
             　　dataType: "json",
             　　　data: {　　　　
                 "name": $("#name").val(),
                 "url":  $.trim($("#url").val()),
                 "method": $("#sel-method").val(),
                 "protocol":$("#sel-pro").val(),
                 "params":  $.trim($("#params").val()),
                 "hope":  $.trim($("#hope").val()),
                 "fid": id
             },
             　　success: function (data) {　　　　 //要执行的代码
                  if (data["code"] == 0) {
                       location.reload()
                  }
             },
             error: function (e) {
                 alert("失败")
                 location.reload()
             }
         })
     }
 })

