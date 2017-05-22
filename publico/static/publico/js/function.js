jQuery(document).ready(function()
{
	jQuery(".cont_menu ul li:first").attr("style","background:none !important;");
	cbpBGSlideshow.init();
	jQuery(".cont_breadCrumbs ul li:first").attr("style","background:none !important;");

	alto_restante = jQuery(document).height()- 106;
	jQuery(".listsubmenu").height(alto_restante);

	/*jQuery(".anadir_texto a").bind("click",function(e)
	{
		e.preventDefault();
		idProducto = jQuery(this).attr("name");
		jQuery.ajax({
			type:"POST",
			url: site.baseUrl+"/wp-insert-product.php",
			data:{insert:"true",idProducto:idProducto},
			success:function(data)
			{
				/* alert(data); 
			}
		});
	});*/

	//jQuery(".close_reg").bind("click",function(e)
	//{
	//	e.preventDefault();
	//	id_producto = jQuery(this).attr("name");

	//	jQuery.ajax(
	//	{
	//		type:"POST",
	//		url: site.baseUrl+"/wp-delete-producto.php",
	//		data:{insert:"true",id_producto:id_producto},
	//		success:function(data)
	//		{
	//			location.reload();
	//		}
	//	});
	//});
});