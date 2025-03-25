# Start Stafee App 

## Start VS Code.  

## Clone repository from:
https://github.com/alrudniy/staffee-s25.git


## Create a new virtual environment:
python -m venv venv

## Activate the Virtual Environment:
### On Windows:
venv\Scripts\activate
### On macOS/Linux:
source venv/bin/activate

## Install Dependencies. With the virtual environment active, install your project’s dependencies from your requirements.txt.
pip install -r requirements.txt


# In order to run the project with briefcase (android)
# 1. ensure you are in the child folder of staffee (if not -> run 'cd staffee')
# 2. 'briefcase create android' -> briefcase downloads java JDK + android SDK
# 3. 'briefcase build android' -> briefcase build command compiles project to into android APK app file
# 4. 'briefcase run android' -> runs the application 
