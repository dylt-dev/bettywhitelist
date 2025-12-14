{% extends 'layout.pyp' %}
{% block title %}The List{% endblock title %}
{% block content %}
	{% if d|length == 0: %}
	<p id='beFirst'>It looks like no one has been added to the list yet.<br><p><a href='https://www.bettywhitelist.com'>Be First!</a></p>
	{% else %}
	<table id='theList'>
		<tr> <th>Star</th> <th>Added</th> <th>Token</th> <th>Added on</th> <th>Claimed on</th> </tr>
		{% for o in d %}
			<tr>
				<td><a href='/code/star?id={{ o.idStar }}'>{{ o.name }}</a></td>
				<td>
					{% if o.email %}
						{{ o.email }}
					{% endif %}
				</td>
				<td>{{ o.token }}
<!--					<td>{{ o.star_created_on.strftime("%b %d %Y %-I:%M %p") }}</td> -->
				<td>{{ o.star_created_on }}</td>
				<td>
					{% if o.claim_created_on %}
						{{ o.claim_created_on }}
					{% endif %}
				</td>
			</tr>
		{% endfor %}
	</table>
	{% endif %}
{% endblock %}