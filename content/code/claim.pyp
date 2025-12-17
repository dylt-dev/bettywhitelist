{% extends 'layout.pyp' %}
{% block title %}Claim a Star{% endblock title %}
{% block content %}
<div>
    Please enter your unique id. It will look like this: <span class='claimCode'>segment-argue-onward-hatchback</span>
</div>
<div>
    <form class='claimCodeForm' action='claimCodeAction' method='post'>
        <input class='claimCode' name='claimCode' autofocus/>
        <input type='submit' value='Submit'/>
    </form>
</div>
{% endblock %}
