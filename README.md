![420620970-14b2af5f-897d-4e63-9a6f-f23a6328ace3 (Pequeno)](https://github.com/user-attachments/assets/55799d92-e160-404f-8c2b-c774bf468c03)
# Alfredo
Export hundreds of DOCX and TXT files in seconds

## Why it was made?
I made this little python app because i hate to see my mom taking 5 hours of his time to make certificates for 10.000 people.

This app will make it much easier.

it was intended to be more than that, but i decided that it was way to much effort, so it only does that for now.

it *may* be updated with more features, but yea, do not expect much.

## How to install

This app requires **Flet**, **python-docx**, and **Python 3.12** or later (older versions may not work).

1. To install the packages type: `pip install flet[all] python-docx` *(if the app does not work with flet future versions, just check the pyproject files and download from there)*

Also, if you want to convert the files to **PDF** consider using the **docx2pdf** CLI tool that you can install with this command *(requires Word to be installed in your machine)*

2. To convert files to PDF install docx2pdf: `pip install docx2df`

3. Then type: `docx2pdf -h` (if this does not work, maybe python is not on your system path)

After that you are ready to go!

4. To run the app, **open the folder where main.py** is located and type: `flet run`

### Why not an executable?

For some reason Flet does some magic that breaks my multithreaded code... so nope.

Thats on you to find out :)

## How to use

1. Create an spreadsheet where the headers contain data like this: **[your_code_here]** ever time an match with your code is found, its going to be replaced.
2. Put the part you want to be replaced on your DOCX or TXT with your code.
3. Choose an Path to export.
4. SUCCESS! 🙌🥳🎉
