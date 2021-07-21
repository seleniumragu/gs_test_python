## Automation

### Setting up the environment

### Windows OS
1. Install [python] (https://www.python.org/downloads/)
2. Install Python 3.7.2 running.
3. Set the newly installed Python to be used globally running `python 3.7.2`.(add it to your Environment PATH. )
4. Download the [Chrome driver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for Selenium and add it to your Environment PATH.  

### Mac OS
1. Install [pyenv](https://github.com/pyenv/pyenv).
2. Install Python 3.7.2 running `pyenv install 3.7.2`.
3. Set the newly installed Python to be used globally running `pyenv global 3.7.2`.
4. Download the [Chrome driver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for Selenium and add it to your PATH.  
If you use macOS, you can do this via [Homebrew](https://brew.sh/) running `brew install chromedriver`.

##IDE need to installed
1. Install [pyCharm Professional Version] (https://www.jetbrains.com/pycharm/download/#section=windows)

## Plugins need to be updated

Install the plugins list from the requirements.txt file

### Run the tests

1. Go to the features directory  right click on an feature file and run
2. Go to the features directory open any feature right click on any step and run for a specific step

## Run the tests from Commandline (CMD)
1. Open command prompt -> navigate to the project folder 
2. Enter the below command
3. python -m behave --logging-level DEBUG --no-capture -f allure_behave.formatter:AllureFormatter -o ../../artifacts/allure --junit --junit-directory ../../artifacts/junit -t ~@skip -t @smoke_test -k -D browser=chrome -D env=test
4. If you want to run with different tag's just change the tag name in the command (for example @smoke_test, @test)
5. Note: You need to add the tag names in the  feature scenario before to use.
