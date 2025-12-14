<html>
    <head>
		<link rel="icon" type="image/png" sizes="16x16" href="/img/favicon-16x16.png">
		<link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32x32.png">
		<link rel='stylesheet' href='/style.css'>
        <title>bwl - oh dear</title>
    </head>
    <body>
        <div class='flexVertCenter'>
            <div class='errorTitle'>
            oh dear!
            </div>
            <div class='errorImage'>
                <img src='/img/500.jpg'/>
            </div>
            
            <details class='errorDetails'>
                <summary class='errorMessage' autofocus>{{- message }}</summary>
                <div class='errorTrace'>
                    {{- traceback }}
                </div>
            </details>
        </div>
    </body>
</html>