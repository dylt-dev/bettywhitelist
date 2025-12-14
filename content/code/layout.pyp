<!DOCTYPE html>
<html lang="en">
	<head>
		<link rel="icon" type="image/png" sizes="16x16" href="/img/favicon-16x16.png">
		<link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32x32.png">
		<link rel='stylesheet' href='/style.css'>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>The BWL - {% block title %}{% endblock %}</title>
	</head>
	<body>
        <header>
            <div class='title'>The Betty White List</div>
            <ul>
                <li><a href='/'>Home</a></li>
                <li><a href='/list'>The List</a></li>
                <li><a href='/claim'>Claim a Star</a></li>
            </ul>
        </header>
        {% block content %}{% endblock %}
    </body>
</html>
