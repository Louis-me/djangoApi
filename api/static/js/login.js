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

    $("#btn-confirm").click(function(){

        if ( !isJSON($("#params").val())) {
         alert("请填入正确入参的json")
            return
        }

        validate()
    })
     function validate() {
         $("#m-form").validate({　　
             onsubmit: true, // 是否在提交是验证
             onfocusout: false, // 是否在获取焦点时验证
             onkeyup: false, // 是否在敲击键盘时验证
             rules: {　　　　 //规则
                url: {required: true},
                params: {required: true},

             },
             messages: {
                 url: {required: "请输入url"},
                 params:{required: "请输入入参"},
             },
             submitHandler: function (form) { //通过之后回调
                 EditCase()
             },
             invalidHandler: function (form, validator) {
                 return false;
             }
         });
     }

     function EditCase() {
         $.ajax({　　
             url: 'login_edit',
             　　type: "post",
             　　dataType: "json",
             　　　data: {　　　　
                 "url": $("#url").val(),
                 "params": $("#params").val()
             },
             　　success: function (data) {　　
                   console.log(data)
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

