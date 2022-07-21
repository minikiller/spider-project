    $(function () {
            var i = 0;
            var sm = setInterval(donghua, 5000);

            $(".it-banner ul li").hover(function () {
                $(this).addClass("hover").siblings().removeClass("hover");

                clearInterval(sm);

                var img1 = "#img" + $(this).index();
                $(img1).fadeIn(500).siblings("a").fadeOut(500);

            }, function () {
                sm = setInterval(donghua, 3000);
            });

            function donghua() {
            	var count = $("#pictureNewsCount").val();
                if (i > count-1) { i = 0; }
                var img1 = "#img" + i;
                $(img1).fadeIn(500).siblings("a").fadeOut(500);
                $(".lit_bn ul li").eq(i).addClass("hover").siblings().removeClass("hover");                $(".ban-sp span").eq(i).addClass("setOn").siblings().removeClass("setOn");
                i++;
            }
            donghua();
            $('.ban-sp span').click(function(){
				i=$(this).index();
			})
        });
/*tab切换*/
function setTab(tabNav){
	$(tabNav).children("span").click(function(){
		$(this).addClass("hover").siblings().removeClass("hover");
		var uList=$(".ul_"+$(this).attr("data-rel"));
		uList.addClass("setOn").siblings().removeClass("setOn");
	});
}

    Date.prototype.Format = function(fmt) {
        var o = {
            "M+" : this.getMonth() + 1,
            "d+" : this.getDate(),
            "h+" : this.getHours(),
            "m+" : this.getMinutes(),
            "s+" : this.getSeconds(),
            "q+" : Math.floor((this.getMonth() + 3) / 3),
            "S" : this.getMilliseconds()
        };
        if (/(y+)/.test(fmt))
            fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
        for (var k in o)
            if (new RegExp("(" + k + ")").test(fmt))
                fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
        return fmt;
    }
