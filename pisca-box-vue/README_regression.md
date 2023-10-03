
# Regression Testing

### In the development version
```streamlit run app/home.py```
Beauti should work and the xml should load basically even if it doesn't fully run (if PISCA doesn't work).  
Using the tests/fixtures/datatype directories
1. /cnv/ create reg_ for both strict_small and belle data.
2. /acna/ create reg_ for both belle data.
3. /biallelic/ create reg_ for both patient1

### In docker build locally
```docker run --rm --name pisca-vue-dev -p 8001:8501 pisca-box-vue```
1. For each of the above xml files - run them and make sure they work
2. Do the whole thing again, create them AND run them

### In final build distributed
2. Do the whole thing again, create them AND run them
```docker run --rm --name pisca-vue-prod -p 8001:8501 rachelicr/pisca-box-vue```

