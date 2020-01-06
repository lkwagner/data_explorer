# data_explorer
A template for using flask+altair to explore complex simulation data


# Quickstart

To get started with the example data, 

```
  cd example_run
  python3 he.py
```

This will create a bunch of hdf5 files in your `static/` directory. This is where all the static files accessed by the webserver should reside.

Now run 
```
    python3 webpage.py
```
and direct your browser to localhost:5000. 

# Modifying to fit your data

Most of what you need to change is in make_plots.py. 
There are three important functions there, which should be fairly obvious. 
At the time of this writing, you also need to modify the table display in templates/table.html to display what variables you are interested in. 
This could be fixed with intelligent jinja work.

If you'd like to generate more/different reports, you need to write functions in webpage.py and make_plots.py to either generate different charts or tables. 