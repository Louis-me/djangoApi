var edit = 0 // 0 表示为新建，1表示为编辑
var id = 0

 $(function () {
    $("#nav-left ul li:eq(3) a").css("color", "red")
     validate()
      $(".btn-del").click(function () {
         id = $(this).parents("tr").attr("id")
         $("#modal-del").modal("show")
     })
     $("#btn-modal-confirm").click(function () {
        $.rpc.req("../../../check_del","post",{"chid": id},function(resp){
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

     $(".btn-edit").click(function () {
         edit = 1
         id = $(this).parents("tr").attr("id")
        var name = $.trim($(this).parents("td").prevAll(":eq(4)").text())
        var find_type = $.trim($(this).parents("td").prevAll(":eq(2)").text())
        var element_info = $.trim($(this).parents("td").prevAll(":eq(3)").text())
        var operate_type = $.trim($(this).parents("td").prevAll(":eq(1)").text())
        var extend = $.trim($(this).parents("td").prevAll(":eq(0)").text())
        $("#name").val(name)
        $("#find_type").val(find_type)
        $("#element_info").val(element_info)
        $("#operate_type").val(operate_type)
        $("#extend").val(extend)
     });
     $("#btn-new").click(function() {
        edit = 0
     });
     function validate() {
         $("#m-form").validate({　　
             onsubmit: true,
             onfocusout: false,
             onkeyup: false,
             rules: {　　　　 //规则
                element_info: {required: true},
                name: {required: true},
                sort: {digits: true, required: true}
             },
             messages: {
                 element_info: {required: "请输入元素"},
                 name:{required: "请输入名称"},
                 sort: "必须输入整数",
             },
             submitHandler: function (form) { //通过之后回调
                if (edit==1) {
                    EditCheck()
                } else {
                    NewCheck()
                }

             },
             invalidHandler: function (form, validator) {
                 return false;
             }
         });
     }
    function NewCheck() {
        var name = $.trim($("#name").val())
        var find_type = $.trim($("#find_type").val())
        var element_info = $.trim($("#element_info").val())
        var operate_type = $.trim($("#operate_type").val())
        var extend = $.trim($("#extend").val())
        var sort =  $.trim($("#sort").val())

        var data = {"name": name, "find_type":  find_type, "element_info": element_info,"operate_type":operate_type,
         "extend": extend, "cid": $("#cid").val()}
        $.rpc.req("../../../check_new", "post", data, function(resp){
            if (resp && resp["code"] == 0) {
                    alert("成功")
                     location.reload()
            }
            else {
                    if (resp && resp["code"] ) {
                         alert(resp.msg)
                    } else {
                        alert("请求失败")
                     }
                    location.reload()
            }
        })
    }
     function EditCheck() {
        var name = $.trim($("#name").val())
        var find_type = $.trim($("#find_type").val())
        var element_info = $.trim($("#element_info").val())
        var operate_type = $.trim($("#operate_type").val())
        var extend = $.trim($("#extend").val())
        var sort =  $.trim($("#sort").val())
        var data = {"name": name, "find_type":  find_type, "element_info": element_info,"operate_type":operate_type,
         "extend": extend, "sort":sort, "chid": id}
        $.rpc.req("../../../check_edit","post",data,function(resp){
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


