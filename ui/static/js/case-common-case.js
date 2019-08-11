var edit = 0 // 0 表示为新建，1表示为编辑
var id = 0 // 是ccc_id
$(function(){

    $("#nav-left ul li:eq(6) a").css("color", "red")

    $("#btn-new").click(function(){
        edit = 0
    })
    $(".btn-edit").click(function(){
        edit = 1
        id = $(this).parents("tr").attr("id")
        var sort = $.trim($(this).parents("td").prevAll(":eq(0)").text())
        $("#sort").val(sort)
        $("#sel-common-case").val($(this).parents("tr").attr("id"))
    })

    validate()
     $(".btn-del").click(function () {
         id = $(this).parents("tr").attr("id")
         $("#modal-del").modal("show")
     })

     $("#btn-modal-confirm").click(function () {
            $.rpc.req("../../../case_common_case_del","post",{"ccc_id": id},function(resp){
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

    function NewCaseCommonCase() {
        var data =  {　　　　
                 "name": $("#sel-common-case").find("option:selected").text(),
                 "cc_id": $("#sel-common-case").val(),
                 "cid": $("#cid").val(),
                 "ccc_id": id,
                 "sort": $.trim($("#sort").val())
                 }
        $.rpc.req("../../../case_common_case_new","post",data,function(resp){
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
    function EditCaseCommonCase() {
          var data =  {　　　　
             "name": $("#sel-common-case").find("option:selected").text(),
             "cc_id": $("#sel-common-case").val(),
             "ccc_id": id,
             "sort": $.trim($("#sort").val())
             }
        $.rpc.req("../../../case_common_case_edit","post",data,function(resp){
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
               sort: {digits: true, required: true}
             },
            messages: {
                 sort: {required: "排序必须为整数"},
            },
            submitHandler: function (form) { //通过之后回调
                 if (edit == 0) {
                     NewCaseCommonCase()
                 } else {
                     EditCaseCommonCase()
                 }
             },
             invalidHandler: function (form, validator) {
                 return false;
             }
        });
   }
})