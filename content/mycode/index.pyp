{% extends 'layout.pyp' %}
{% block title %}Home{% endblock title %}
<!DOCTYPE html>
{% block content %}
The </b>Betty White List</b> is the list of stars that we most want to make it to the end of 2020! <b>Betty White</b> is #1 on that list, obviously,
but there are plenty more.
<br><p>
Check out <a href='/code/list'>the list</a>, and if your star is not already on the list then you get to get first! If they <em>are</em> already on, we're working on
how to add your support, so check back!
<form method='post' action='/code/addStar'>
	<b>Please add</b> <input name='name' placeholder='(name of star)'> <input type='submit' value='+'/>
</form>
<br><p>
Let's all work together and let these folks know how we feel!
<br><p>
Thanks + Have a Great Day,
<br><p>
The Betty White List
<br><p>
<!-- <img src='https://globalgrind.com/wp-content/uploads/sites/16/2014/06/88433782.jpg' alt='https://globalgrind.com/3974753/betty-white-young-photos/' width='150px'> -->
<img src='img/rock-on.jpg' alt='Betty White says Rock On!' width='150px'>
{% endblock %}
