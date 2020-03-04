function check_fields()
{
	var name = document.getElementById('name').value;
	
	var email = document.getElementById('email').value;

	var message = document.getElementById('message').value;

    var reEmail = /^(?:[\w\!\#\$\%\&\'\*\+\-\/\=\?\^\`\{\|\}\~]+\.)*[\w\!\#\$\%\&\'\*\+\-\/\=\?\^\`\{\|\}\~]+@(?:(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-](?!\.)){0,61}[a-zA-Z0-9]?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9\-](?!$)){0,61}[a-zA-Z0-9]?)|(?:\[(?:(?:[01]?\d{1,2}|2[0-4]\d|25[0-5])\.){3}(?:[01]?\d{1,2}|2[0-4]\d|25[0-5])\]))$/;

	if(name == "")
	{
		alert('Please enter your full name');
	}

	else if(email == "")
	{
		alert("Please enter your email address");
	}
    else if(!email.match(reEmail))
    {
        alert("Invalid email address");
    }
	else if(message == "")
	{
		alert('Please enter your message');
	}else{
		alert('Thank you! Your message has been received');
        document.getElementById('forms').reset()
	}
}

$(document).ready(function(){
	$('.gallery').fancybox();
});
