function trim(str) {
  return str.replace(/^\s+|\s+$/g, '');
}

function checkNumber(number)
{

  var pattern=/^([0-9])+/;

    if(pattern.test(number)) {
	return true;
  } else {
	return false;
  }

}

function toggleFormVisibility()
{
  var change_properties_element = document.getElementById('change_properties');

  var nosub_link_element = document.getElementById('nosub');

  var vis = change_properties_element.style;

  if(vis.display=='' || vis.display=='none') {
	  vis.display = 'block';

	  nosub_link_element.style.display='';
  } else {
	  vis.display = 'none';

	  nosub_link_element.style.display='none';
  }

}

function processFormData()
{

  var maxSpeed_element = document.getElementById('txt_maxSpeed');
  var distance_element = document.getElementById('txt_distance');
  //var mail_format_element = document.getElementById('slt_mail_format');

  var maxSpeed = trim(maxSpeed_element.value);
  var distance = trim(distance_element.value);
  //var mail_format = mail_format_element.value;

  var error_message = 'The following fields had errors in them: \n\n';
  var data = 'Following properties are changed: \n\n';

  var error_flag = false;

  if(!checkNumber(maxSpeed)) {
	  error_message += 'Max Speed: Please enter a speed value\n';
	  error_flag = true;
  } else {
	  data += 'Max Speed: ' + maxSpeed+ '\n';
  }

  if(!checkNumber(distance)) {
	  error_message += 'Distance: Please enter a speed value';
	  error_flag = true;
  } else {
	  data += 'Distance: ' + distance+ '\n';
  }

  if(error_flag) {
	  alert(error_message);
  } else {
	  alert(data);
  }

}

    window.onload = toggleFormVisibility;