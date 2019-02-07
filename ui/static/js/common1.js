 ;(function ($) {
    $.rpc = {};
    $.rpc.req = function (url, type, data, cb) {
        $.ajax({
            url: url ,
            type:type,
            dataType:"json",
//            timeout:500,
            error:function (xhr) {
                if ($.isFunction(cb)) {
                    cb(null);
                }
            },
            data:data,
            success:function (data) {
                if ($.isFunction(cb)) {
                    cb(data);
                }
            }
        });

    };
})(jQuery);



