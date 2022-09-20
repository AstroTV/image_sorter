# image_sorter
Finds all jpg and png images in a folder and scans their name and EXIF data for a datastring to sort them accordingly

## How to use
Run the script with python3, the desired output folder can be defined with a command-line argument
```python3 imageSorter.py ~/Pictures/sorted```
If no argument is provided a new folder named **output** is created inside the input directory
```python3 imageSorter.py```

In order to move the images instead of copying replace `copyfile(...)` with `move(...)`

## Disclaimer
I am not responsible for any data loss that might occur. Use on your own risk.
