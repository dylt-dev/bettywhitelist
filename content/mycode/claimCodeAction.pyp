{% extends 'layout.pyp' %}
{% block title %}The List{% endblock title %}
{% block content %}
<ol class='punchlist'>
    <li>
        <details>
            <summary>Get the claim code from `http.args`</summary>
            <p class='code'>
                claimCode={{ http.args.claimCode }}
            </p>
        </details>
    </li>
    <li>
        <details>
            <summary>Lookup rows in `v_star_claim` that match the claim code</summary>
            <p class='code'>
                starClaims<br/>
                {{ starClaims }}
            </p><br/>
        </details>
    </li>
    <li>
        <details>
            <summary autofocus>Validate row count</summary>
            <ul>
                <li>
                    <details>
                        <summary>0 (No star found) - simple response</summary>
                    </details> 
                </li>
                <li>
                    <details>
                        <summary>1 - Totally fine</summary>
                        <ul>
                            <li>Present a confirmation form</li>
                            <li>If yes, send an email for confirmation</li>
                            <li>If no, provide a nice place to enter why not</li>
                        </ul>
                    </details> 
                </li>
                <li>
                    <details>
                        <summary>>1 (Shouldn't happen) - error condition/500 w helpful response</summary>
                    </details> 
                </li>
            </ul>
        </details>
    </li>
    <li>
        <details>
            <summary>
        </details>
    </li>
</ol>
{% endblock %}
