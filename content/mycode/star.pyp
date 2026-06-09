{% extends 'layout.pyp' %}
{% block title %}{{ starClaim.name }}{% endblock title %}
{% block content %}
<table class='object-detail'>
	<tr> <td>Name</td> <td>{{ starClaim.name }}</td> </tr>
	<tr> <td>Token</td> <td>{{ starClaim.token }}</td> </tr>
	<tr> <td>Claimed By</td> <td>{{ starClaim.email }}</td> </tr>
	<tr> <td>Created On</td> <td>{{ starClaim.starCreatedOn }}</td> </tr>
	<tr> <td>Claimed On</td> <td>{{ starClaim.claimCreatedOn }}</td></tr>
</table>
{% endblock content %}