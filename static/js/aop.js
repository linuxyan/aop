$(document).ready(function(){

 //$("#send").click(function(){
//	$.post("svnadd/",
//	{ 
//	  email:$('#inputEmail').val(),
//	  passwd:$('#inputPassword').val()
//	},
//	function(result){
//	  alert(result);
//	  });
// });  
 
 //$("a[name='Edit']").click(function(){
 //  var $v =$("a[name='Edit']").attr('id');
//	alert($v);
 //});
 
  $("a[name='addservergroup']").click(function(){	
   var $group_id =$(this).attr('id');
   var $host_id = $(this).attr('value');
   $.post("/addtogroup/",
   { 
     grouptype:"servergroup",
     host_id:$host_id,
     group_id:$group_id
   },
   function(result){
    $('#addgroupstatus').text(result);
    $(".alert").alert();
    $('#myModal').modal({
    backdrop:true,
    keyboard:true,
    show:true});
  });});	
 
 
   $("a[name='addscriptgroup']").click(function(){	
   var $group_id =$(this).attr('id');
   var $script_id = $(this).attr('value');
   $.post("/addtogroup/",
   { 
     grouptype:"scriptgroup",
     script_id:$script_id,
     group_id:$group_id
   },
   function(result){
    $('#addgroupstatus').text(result);
    $('#myModal').modal({
    backdrop:true,
    keyboard:true,
    show:true});
  });});

   $("a[name='hostgroup_del_host']").click(function(){	
   var $host_id =$(this).attr('id');
   var $group_id = $(this).attr('value');
   $.post("/hostgroup_del_host/",
   { 
    host_id:$host_id,
     group_id:$group_id
   },
   function(result){
   //$("#group_host_table").load(location.href+"#group_host_table>*");
     location.reload();
    });
   });
   
   $("a[name='scriptgroup_del_script']").click(function(){	
   var $script_id =$(this).attr('id');
   var $group_id = $(this).attr('value');
   $.post("/scriptgroup_del_script/",
   { 
    script_id:$script_id,
     group_id:$group_id
   },
   function(result){
   //$("#group_host_table").load(location.href+"#group_host_table>*");
     location.reload();
    });
   });   
   
   $("a[name='runtask']").click(function(){	
   var $task_id =$(this).attr('id');
   $.post("/task_run/",
   { 
      task_id:$task_id
   },
   function(result){
     alert(result);
     location.reload();
    });
   }); 
   
   
   
   
}); 