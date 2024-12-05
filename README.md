# Animal Migratory Pattern Tracking Module: Gang Beasts

## File Structure 
At the top level directory there are 3 files and 3 subdirectories. 
- README.md: The current file you're viewing 
- Data_Visualization.py: streamlit appliactions require the default page of 
the application to exist in the top level directory in order to understand 
what to run as the main page. This is that main page 
- requirements.txt: A list of all 3rd party modules that were utilized 

Then the purpose for each subdirectory.

- data_analysis: Where we conduct all of our data analysis, processing, and graphing of our selected datasets. It's also where we locally store said datasets. All modualized functions are in .py files, where the actual visualizations and usages are in ipynb files.
- pages: Hosts the additional pages within our website 
- test: For standalone test scripts 

## Running our Application 

To run the website, direct to the top level directory and run 

``` bash
streamlit run `.\Data_Visualization.py`
```


To run all data analysis visualization and EDA of the datasets, go to direcorty ./data_analysis/test_code/

- To run the EDA of red_fox, run 'red_fox_test.ipynb'
- To run the correlation analysis of red_fox, run 'red_fox_correlate.ipynb'
- To run the EDA and correlation analysis of jaguar, run 'jaguar_test.ipynb'


## Third Party Modules 

All third party modules are listed within the requirements.txt file, but to list the most notable ones 
- folium
- pandas 
- geopy 
- numpy 
- plotly 
- scikit-learn 
- scipy 
- tabulate 
- matplotlib
- geopandas 

## Additional Notes

Thank you for the Quarter! It was really enjoyable and we learned a lot in reference to Python, and we hope to always learn more! 
