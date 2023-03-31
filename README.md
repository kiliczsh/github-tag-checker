# GitHub Tag Checker 

This is a simple script that checks if a GitHub release tag exists. It gathers tags in a format to be used.

## Usage

Create a virtual environment and install the requirements.

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Run the script with the repository name as an argument.

```bash
$ python main.py LimeSurvey/LimeSurvey
```

Replace `LimeSurvey/LimeSurvey` with the repository you want to check.

## Sample Data

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