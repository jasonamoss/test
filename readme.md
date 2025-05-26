# Animal Boarding Calendar App

This repository contains a simple boarding calendar application built with
Python's `tkinter` GUI toolkit. The app provides a spreadsheet style
interface to manage cages and bookings for an animal boarding business.

## Features

- Calendar view of days with notes and cages as columns
- Add additional cages at runtime
- Join two cages into a single large cage or split joined cages
- Double-click any cell to edit its contents
- Quickly book a cage for multiple days using the **Book Stay** button
- Save the calendar to a CSV file
- Table now displays simple borders for better readability

## Requirements

The application requires Python 3 with the standard `tkinter` module
(which is included with most Python installations).

## Running

```
python3 boarding_app.py
```

A window will open where you can generate a calendar, manage cages and
enter bookings. To distribute a standalone macOS application you can use
tools like `py2app` or `PyInstaller` to bundle `boarding_app.py`.

