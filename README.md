# Sphinx Auctions


## Overview

This project is my submission for the Commerce project, part of Harvard University's CS50W course: Web Programming with Python and JavaScript. The goal was to design an eBay-like e-commerce auction site that allows users to post auction listings, place bids, comment on listings, and add listings to a "watchlist."

## Features

- **Active Listings Page**: A dynamic overview of all active auction listings, displaying essential details such as title, description, current price, and image if available.
- **Listing Page**: Detailed view of a listing, including functionality for bidding, commenting, and watchlist management. Listing creators can close auctions, and winners are notified on this page.
- **User Registration and Authentication**: Enabling personalized experiences such as bidding, commenting, and watchlist management.
- **Create Listing**: Users can create new auction listings with titles, descriptions, starting bids, optional images, and category.
- **Watchlist**: Users can add or remove listings from a personal watchlist, with easy navigation to their watched auctions.
- **Categories**: Categorized listings for easier navigation and discovery based on interests.
- **Django Admin Interface**: An admin interface for site administrators to manage listings, comments, and bids.

## Prerequisites

- Python
- Django
- Git (Optional)

Ensure you have Python and Django installed on your system. If not, follow the instructions on [Python's official website](https://www.python.org/) and [Django's documentation](https://docs.djangoproject.com/en/stable/intro/install/) to get them installed.

## Getting Started
1. Clone the repo or download the zip file.
2. `cd Sphinx-Auctions`
3. Run `python manage.py makemigrations auctions` to make migrations for the `auctions` app.
4. Execute `python manage.py migrate` to apply migrations to the database.
5. Start the development server with `python manage.py runserver` and visit `http://127.0.0.1:8000/` in your web browser.
   
## Technologies

- **Frontend**: HTML, Bootsrap
- **Backend**: Django (Python)
- **Database**: SQLite (Django's default database)

## Project Structure

- `auctions/`: Django app containing models, views, templates, and URL configurations for the auction functionality.
- `commerce/`: Project directory with settings and root URL configurations.

## Models

- **User**: Inherits from `AbstractUser`, customized with additional fields as needed.
- **Listing**: Represents auction listings with fields for title, description, starting bid, image URL, and category.
- **Category**: Represents different categories under which listings can be classified (e.g., Electronics, Fashion, Home).
- **Bid**: Tracks bids on auction listings, including bid amount and the user who placed the bid.
- **Comment**: Allows users to comment on listings, with fields for the comment text and associated listing.
- **Watchlist**: Represents the user's watchlist, containing references to the User model and the Listing model.

## How to Contribute

This project is part of my coursework and is not currently open for external contributions. Feedback and suggestions are welcome.

## Acknowledgments

- Project idea and specifications provided by [CS50W](https://cs50.harvard.edu/web/).
- Inspiration from eBay for auction and bidding features.
