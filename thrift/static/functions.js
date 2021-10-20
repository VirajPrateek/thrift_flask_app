$(document).ready(function() {

	var windowLoc = $(location).attr('pathname'); //jquery format to get window.location.pathname
	switch(windowLoc){
	    case "/":
   			welcomeMessage();
   			break;
  		case "/features/expenditure":
    		addingExpenditure();
    		break;
  		case "/features/view":
    		viewForm();
   		 	break;
	}

$(function(){
    var dtToday = new Date();

    var month = dtToday.getMonth() + 1;
    var day = dtToday.getDate();
    var year = dtToday.getFullYear();
    if(month < 10)
        month = '0' + month.toString();
    if(day < 10)
        day = '0' + day.toString();

    var maxDate = year + '-' + month + '-' + day;
    $('#txtDate').attr('max', maxDate);
    $('#txtDate').val(maxDate);
});

});

function openNav() {
  document.getElementById("mySidepanel").style.width = "250px";
  $('.home-page').hide();
}

function closeNav() {
  document.getElementById("mySidepanel").style.width = "0";
  $('.home-page').show();
}

function welcomeMessage(){
	$('.home-page').append("<span>Welcome!</span>"+
		"<p>Go to side-bar for adding data</p>"+
		"<p>Drop-down on top to view data </p>")
}


function addingExpenditure(){

	var max_fields      = 10; //maximum input boxes allowed
	var wrapper   		= $(".input_fields_wrap"); //Fields wrapper
	var add_button      = $(".add_field_button"); //Add button ID

	var x = 0; //initlal text box count
	$(add_button).click(function(e){ //on add input button click
		e.preventDefault();
		if(x < max_fields){ //max input box allowed
			x++; //text box increment
			$(wrapper).append('<div class="anItem" style="background-color:lightyellow; margin:13px;">'+
				'<input type="text" class="iName" name="iName" placeholder="Item Name"/>'+
				'<input type="number" class="iAmount" name="iAmount" placeholder="Item Amount" required/><br/>'
				+'<button class="remove_field">Remove</button></div>'); //add input box
		}

	$(".iAmount").on("change keyup paste", function(){
		makeExpenditureDataReady();
		});

	});


	$(wrapper).on("click",".remove_field", function(e){ //user click on remove text
		e.preventDefault();
		var amountToRemove = parseInt($(this).parent('div').children('.iAmount').val());
		var itemToRemove = $(this).parent('div').children('.iName').val()
		alert("Removing item: "+itemToRemove+"("+ amountToRemove+")");

		var from = $('#totalAmount').val();
		var updatedAmount = from -  amountToRemove;
		$('#totalAmount').val(updatedAmount);
		$('#totalAmountDisplay').val(updatedAmount);
		$(this).parent('div').remove(); x--;
		makeExpenditureDataReady();
	})

}

function makeExpenditureDataReady(){
		var totalItems = $('.iAmount').length;
		var allAmounts = [];
		var allItems = []; //never required..
		var totalAmount 	= 0; //Initial amount is zero
		var itemList ="";

		 for (var i = 0; i < totalItems; i++) {//push all values to different arrays
		 	var amountToPush = $('.iAmount').eq(i).val();
		 	var itemToPush = $('.iName').eq(i).val()
		 	allAmounts.push(amountToPush);//amount
		 	allItems.push(itemToPush);//item's name - not required I guess now.
		 	itemList = itemList + itemToPush+'('+amountToPush+'),';
		 }

		 for (var i = 0; i < allAmounts.length; i++) {//sum amount array values
 		   totalAmount += allAmounts[i] << 0;
		}
		$('#totalAmount').val(totalAmount);
		$('#totalAmountDisplay').val(totalAmount);
		$('#itemList').val(itemList);

}

function viewForm(){

}