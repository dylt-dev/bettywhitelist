<html lang="en">
	<head>
		<link rel="icon" type="image/png" sizes="16x16" href="/img/favicon-16x16.png">
		<link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32x32.png">
		<link rel='stylesheet' href='/style.css'>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>The BWL - The List</title>
	</head>
	<body>
		<div class='title'> The Betty White List </div>
		<br/><p/>
		{% if d|length == 0: %}
		<p id='beFirst'>It looks like no one has been added to the list yet.<br><p><a href='https://www.bettywhitelist.com'>Be First!</a></p>
		{% else %}
		<table id='theList'>
			<tr> <th>Star</th> <th>Added</th> </tr>
			{% for o in d %}
				<tr> <td>{{ o.name }}</td> <td>{{ o.created_on.strftime("%b %d %Y %-I:%M %p") }} </td> </tr>
			{% endfor %}
		</table>
		{% endif %}
	</body>
</html>
