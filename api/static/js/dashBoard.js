
$(function(){
     $("#nav-left ul li:eq(2) a").css("color", "red")

    dashBoard_module_case()
    dashBoard_top10_task()
    dashBoard_top100_case_time()



    function dashBoard_module_case() {
        $.rpc.req("dashBoard_module_case","get",{},function(resp){
            if (resp && resp["code"] == 0) {
//                    alert("成功")
//                     location.reload()
//                    id, title, yAxis_title,data
                    highColumn("module-case","模块下的用例", "模块下的用例",resp.data)
             } else {
                     if (resp && resp["code"] ) {
                         alert(resp.msg)
                     } else {
                        alert("请求失败")
                     }
//                     location.reload()
               }
        })
    }

    function dashBoard_top10_task() {
            $.rpc.req("dashBoard_top10_task","get",{},function(resp){
            if (resp && resp["code"] == 0) {
                var id = "#top10-task"
                var h_title = "前十个任务用例执行统计"
                var h_yaxis_title = "前十个任务用例执行统计"
                var h_tooltip = ""
                var h_series = resp.data
                    highLine(id,h_title,h_yaxis_title,h_tooltip,h_series)
             } else {
                     if (resp && resp["code"] ) {
                         alert(resp.msg)
                     } else {
                        alert("请求失败")
                     }
//                     location.reload()
               }
        })
    }
    // 前100个用例的耗时情况
    function dashBoard_top100_case_time() {
            $.rpc.req("dashBoard_top100_case_time","get",{},function(resp){
            if (resp && resp["code"] == 0) {
                var id = "#top100-case"
                var h_title = "前100个用例的耗时情况"
                var h_yaxis_title = "前100个用例的耗时情况"
                var h_tooltip = ""
                var h_series = resp.data
                    highLine(id,h_title,h_yaxis_title,h_tooltip,h_series)
             } else {
                     if (resp && resp["code"] ) {
                         alert(resp.msg)
                     } else {
                        alert("请求失败")
                     }
//                     location.reload()
               }
        })
    }

})