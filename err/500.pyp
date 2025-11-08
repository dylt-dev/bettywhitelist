<html>
    <head>
        <style>
        .badTitle {
            border: 1px solid pink;
            font-size: 2.5rem;
            padding: 1rem;
        }

        .errorCheckbox {
            display: none;

        }

        .errorDetail {
            visibility: hidden;

            div {
               padding: 0.5rem 0;
            }
        }

        .errorImage {
        }

        .errorImage > img {
            width: 250px;
        }

        .errorLabel {
            align-self: center;
        }

        .errorInfo {
            display: flex;
            flex-direction: column;
            align-items: start;
            justify-content: flex-start;
            gap: 1rem;
        }

        .errorInfo * {
            border: 0px solid gray;
        }
        
        .errorMessage {
            font-family: monospace;
            font-size: 2.0rem;
        }

        .errorTitle {
            font-size: 3rem;
        }

        .errorTrace {
            font-family: monospace;
            font-size: 1.1rem;
            line-height: 1.8rem;
            white-space: pre;
        }

        .flexVertCenter {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 3rem;
        }

        input[type='checkbox']:checked ~ .errorDetail {
            visibility: visible;
        }
        </style>
        <title>bwl - ohno</title>
    </head>
    <body>
        <div class='flexVertCenter'>
            <div class='errorTitle'>
            oh no!
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