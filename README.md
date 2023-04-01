# GitHub Tag Checker 

This is a simple script that checks if a GitHub release tag exists. It gathers tags in a format to be used.

## Usage

Create a virtual environment and install the requirements.

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Run the script with the repository name, per page and tag limit as arguments.

```bash
$ export GITHUB_TOKEN="YOUR_PERSONAL_ACCESS_TOKEN"
$ python main.py LimeSurvey/LimeSurvey 100 1000
# 100 tags per page, 1000 tags limit
# default values are 10 and -1 respectively if not provided
# -1 means no limit
```

Replace `LimeSurvey/LimeSurvey` with the repository you want to check.

## Sample Data

The following is a sample of the data that is returned for the following command.

```bash
$ python main.py LimeSurvey/LimeSurvey 100 > limesurvey.json
```

```json
[
    {
        "name": "5.6.12+230327",
        "date": 1679907465,
        "sha": "90f4efdd9912fadc733aad426524775c70b7d901",
        "zipball_url": "https://api.github.com/repos/LimeSurvey/LimeSurvey/zipball/refs/tags/5.6.12+230327",
        "tarball_url": "https://api.github.com/repos/LimeSurvey/LimeSurvey/tarball/refs/tags/5.6.12+230327"
    },
    ...
]
```