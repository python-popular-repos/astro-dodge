from app import create_app

"""Main entry into application"""

if __name__ == "__main__":
    app = create_app("testing")
    app.run(host="0.0.0.0", port=8001)
