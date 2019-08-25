var id = 0
 $(function () {
    $("#nav-left ul li:eq(1) a").css("color", "red")

     $(".btn-del").click(function () {
         id = $(this).parents("tr").attr("id")
         $("#modal-del").modal("show")
     })
     $("#btn-modal-confirm").click(function () {
        $.rpc.req("report_del","post",{"rid": id},function(resp){
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

     $(".btn-log").click(function(){
        $.rpc.req("download_log","post",{ "log": $(this).attr("log")},function(resp){
            if (resp && resp["code"] == 0) {
                       window.location.href = resp["path"]
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

      $(".btn-excel").click(function(){
           $.rpc.req("download_excel","post",{ "excel": $(this).attr("excel")},function(resp){
            if (resp && resp["code"] == 0) {
                window.location.href = resp["path"]

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
 })

