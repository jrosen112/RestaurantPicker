# RestaurantPicker

I wanted to make a kind of restaurant journal where I can note which places I've been to and which places I plan on going to. Plus, people are always recommending certain place so I wanted to make something where I can jot those down!

# DONE
- Creating Restaurant and Address classes, for easy creation, validation, and implementation in the SQLite database
- Functions to create the restaurant and address table in the database
- Functions to add restaurants and addresses to their respective tables
- CSV parser for restaurant data

# IN PROGRESS
- CSV files of addresses for batch uploading to database
- Function to ingest these CSV files, create the proper objects with error-handling, and push into the database

# TODO
- Using latitude and longitude data in the restaurant table, create a local map of where these restaurants are
- Command-line interface that allows the user to browse eating options and filter on a few key attributes
