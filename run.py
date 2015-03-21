import os
from app import app

port = int(os.getenv('VCAP_APP_PORT', 8000))
if __name__ == "__main__":
	app.run(debug=True,port=int(port))