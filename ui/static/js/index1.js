var id = 0
 $(function () {
    $("#nav-left ul li:eq(1) a").css("color", "red")
     $(".btn-del").click(function () {
         id = $(this).parents("tr").attr("id")
         $("#modal-del").modal("show")
     })
     $("#btn-modal-confirm").click(function () {
         $.ajax({　　
             url: 'report_del',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 "rid": id
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

     $(".btn-log").click(function(){
          $.ajax({　　
             url: 'download_log',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 "log": $(this).attr("log")
             },
             　　success: function (data) {
                 if (data["code"] == 0) {
                      window.location.href = data["path"]
                 }
             },
             error: function (e) {
                 alert("失败")
                 location.reload()
             }
         })
     })

      $(".btn-excel").click(function(){
          $.ajax({　　
             url: 'download_excel',
             　　type: "post",
             　　dataType: "json",
             　　data: {　　　　
                 "excel": $(this).attr("excel")
             },
             　　success: function (data) {
                 if (data["code"] == 0) {
                      window.location.href = data["path"]
                 }
             },
             error: function (e) {
                 alert("失败")
                 location.reload()
             }
         })
     })
 })

