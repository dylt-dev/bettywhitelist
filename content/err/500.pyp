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
            <div class='errorInfo'>
                    <label class='errorLabel' for="chkErrorMessage">ugly truth</label>
                    <input class='errorCheckbox' type='checkbox' id='chkErrorMessage'/>
                    <div class='errorDetail'> <div class='errorMessage'> {{- message }} </div>
                        <div class='errorTrace'>
                            {{- traceback }}
                        </div>
                    </div>
            </div>
        <div>
    </body>
</html>