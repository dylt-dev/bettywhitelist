<html>
	<head>
		<link rel='stylesheet' href='https://www.bettywhitelist.com/style.css'>
		<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
		<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
		<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
		<link rel="manifest" href="/site.webmanifest">
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
