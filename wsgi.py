from app import create_app

"""Main entry into application"""

if __name__ == "__main__":
    app = create_app("staging")
    app.run()
