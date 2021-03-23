# README

## Test

Run tests:

    cd kmeans
    pip3 install -r requirements-testing.txt
    python setup.py nosetests --verbosity=2 

## Build Docker image
    
Build:    
    
    docker build . -t local/kmeans-flask:0.1

Try it:

    docker run --rm -it -p 5000:5000 -v /Users/gchatzi/Desktop/kMeans_Topio/logs:/var/local/kmeans/logs local/kmeans-flask:0.1

