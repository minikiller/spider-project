$(function(){
	//内页左侧折叠
	$(".list-d").click(function(){
		if($(this).hasClass("this-close")){
			$(this).removeClass("this-close");
			$(this).parents("li").siblings().children("dl").children("dt").addClass("this-close");
			$(this).siblings("dd").animate({opacity:1},300).css("height","auto");
			$(this).parents("li").siblings().children("dl").children("dd").animate({height:0,opacity:0},300);
		}else{
			$(this).addClass("this-close");
			$(this).siblings("dd").animate({height:0,opacity:0},300);
		}
	});
	$(".title").click(function(){
		if($(this).hasClass("this-close")){
			$(this).siblings("dl").removeAttr("style");
			$(this).removeClass("this-close");
			$(this).siblings("dl").animate({height:"auto",opacity:1},300);
		}else{
			$(this).addClass("this-close");
			$(this).siblings("dl").animate({height:0,opacity:0},300);
		}
	});
	
	$(".left-menu dd a").click(function(){
		$(this).addClass("hover");
		$(this).parents(".left-menu").find(".hover").not($(this)).removeClass("hover");
	});
	
	$(".sty_table tbody tr").hover(function(){
		$(this).css("background","#f1f5f9");
	},function(){
		$(".sty_table tbody tr:even").css("background","#fff");
		$(".sty_table tbody tr:odd").css("background","#f4f4f4");
	});

	

	$(".sty_table").each(function(index, element) {    
		$(this).children("tbody").children("tr:even").css("background","#fff");
		$(this).children("tbody").children("tr:odd").css("background","#f4f4f4");
    });
	
	$(".sty_table tbody tr").each(function(index, element) {
        $(this).click(function(){       	
			$(this).find(".sp_radio").addClass("checked");
			$(this).siblings().find(".sp_radio").removeClass("checked");
		});
    });
	
	
	$(".sty_table_v2 tbody tr").hover(function(){
		$(this).css("background","#f1f5f9");
	},function(){
		$(".sty_table_v2 tbody tr:even").css("background","#fff");
		$(".sty_table_v2 tbody tr:odd").css("background","#f4f4f4");
	});

	

	$(".sty_table_v2").each(function(index, element) {    
		$(this).children("tbody").children("tr:even").css("background","#fff");
		$(this).children("tbody").children("tr:odd").css("background","#f4f4f4");
    });
	
	$(".sty_table_v2 tbody tr").each(function(index, element) {
        $(this).click(function(){
    		var i = $(this).find(".sp_radio");
        	if(i.hasClass("checked")){
        		i.removeClass("checked");
        	}else{
        		i.addClass("checked");
        	}
        	
        	
	//		$(this).find(".sp_radio").addClass("checked");
	//		$(this).siblings().find(".sp_radio").removeClass("checked");
		});
    });
	
	$("input,textarea").focus(function(){
		$(this).css("color","#333");
	});
})