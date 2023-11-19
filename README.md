# Algeo02-22014

## Project Description

## Project Structure
```
doc
src
    |
    flask-app
            |
            cHub
            downloaded_images
            txt
            uploads
            app.py
            CBIRTekstur.py
            CBIRWarna.py
            scrapper.py
            tempCodeRunnerFile.py
            util.py
    |
    -vue-app
            |
            public
            src
                |
                assets
                    |
                    img
                    logo.svg
                    main.css
                components
                        |
                        gambar-viewer
                View
                    |
                    AboutView.vue
                    CameraBased.vue
                    DocView.vue
                    HomeView.vue
                    ImageBased.vue
                    WebScraper.vue
                App.vue
                main.js
                router.js
backend.bat
frontend.bat
README.md
```

## How to run this project?
### Setup
Make sure that your computer has npm installed.

If you haven't already installed flask for python, run the following command
```
 pip install flask
 ```

This project need CORS to be enabled. If you haven't installed flask_cors yet, run the following command
```
pip install flask-cors
```

Finally, for web scrapping, you need to install **beautifulsoup4** and **request**. If you haven't installed them, run the following command
```
pip install beautifulsoup4
pip install requests
```

### Run
Open two terminal and make sure the directory is set to ``Algeo02-22014``.

In the first terminal, run ``frontend.bat``.

In the second terminal, run ``backend.bat``.

Wait for the ``frontend.bat`` to finish configuring.

Finally open ```http://localhost:5173/``` and you'll be good to go!


