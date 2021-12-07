# Cricinfo Scraper

A Web Scraping tool which can be used on [ESPNCricinfo](https://stats.espncricinfo.com/ci/engine/stats/index.html) to write the results obtained from your search query to a CSV file 
so that you can find your own cricket-related stats!

Simply run the file using the command

```
python CricInfoScraper.py
```

Then, enter the link and the Output File Name of your choice.

<br>

A new folder called **Output** will be generated in the same directory as your python file, which would contain your CSV file(If the folder doesn't already exist).

****NOTE:**** By default, the results of all pages will be taken into the CSV.

Some sample URLs: 
```
https://stats.espncricinfo.com/ci/engine/stats/index.html?class=3;team=6;template=results;type=team;view=results
```

```
https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;opposition=5;spanmin1=15+Mar+1995;spanval1=span;team=6;template=results;type=bowling
```
