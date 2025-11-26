<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Tombesson.com - Gallerie Jean Moulin</title>
<script type="text/javascript" src="js/jquery.js"></script>
<script type="text/javascript" src="js/interface.js"></script>

<!--[if lt IE 7]>
 <style type="text/css">
 div, img { behavior: url(iepngfix.htc) }
 </style>
<![endif]-->

<link href="style.css" rel="stylesheet" type="text/css" />
<style type="text/css">
<!--
a:link {
	color: #666666;
}
a:visited {
	color: #666666;
}
a:hover {
	color: #FFFFFF;
}
a:active {
	color: #666666;
}
-->
</style></head>
<body>
<div class="dock" id="dock">
  <div class="dock-container">
  
  
  <?php
   $regexp = "[0-9a-zA-Z]";
   
   $dir = $_GET['dir'];
   if(eregi($regexp, $dir)) {
   //$dir = 'gallery';
	
   // open specified directory
   $dirHandle = opendir($dir);
   $count = -1;
   $returnstr = "";
   while ($file = readdir($dirHandle)) {
      // if not a subdirectory and if filename contains the string '.jpg' 
      if(!is_dir($file) && strpos($file, '.jpg')>0) {
         // update count and string of files to be returned
         $count++;
         //$returnstr .= '&f'.$count.'='.$file;
		 $returnstr = $file;
		 echo '<a class="dock-item" href="#"><img src="'.$dir.'/'.$returnstr.'"/></a>'; 
      }
   } 
   //$returnstr .= '&';
   
   closedir($dirHandle);
   }
?>
  
</div>
</div>
<script type="text/javascript">
	
	$(document).ready(
		function()
		{
			$('#dock').Fisheye(
				{
					maxWidth: 300,
					items: 'a',
					itemsText: 'span',
					container: '.dock-container',
					itemWidth: 200,
					
					proximity: 200,
					halign : 'center'
				}
			)
		}
	);

</script>
<br />
<br />
<br />

<a href="index.html">Return to main page.
</a>
</body>
</html>