# welcome bot: A Probot App

Fill in the blank

## What it does

Frustration

## Getting started

1. [Install the bot](https://github.com/apps/welcome) on the intended repositories. The plugin requires the following **Permissions and Events**:

- Pull requests: Read & Write
- Issues: Read & Write

2. Create a .github/config.yml file to check for content of the comments:

```
# Configuration for welcome - https://github.com/behaviorbot/welcome

# Configuration for new-issue-welcome - https://github.com/behaviorbot/new-issue-welcome

# Comment to be posted to on first time issues
newIssueWelcomeComment: >
  Thanks for opening your first issue here! Be sure to follow the issue template!

# Configuration for new-pr-welcome - https://github.com/behaviorbot/new-pr-welcome

# Comment to be posted to on PRs from first time contributors in your repository
newPRWelcomeComment: >
  Thanks for opening this pull request! Please check out our contributing guidelines.

# Configuration for first-pr-merge - https://github.com/behaviorbot/first-pr-merge

# Comment to be posted to on pull requests merged by a first time user
firstPRMergeComment: >
  Congrats on merging your first pull request! We here at behaviorbot are proud of you!

# It is recommended to include as many gifs and emojis as possible!
```

You can opt out of having the bot comment on first time pull requests, pull request merges, or new issues by not filling in a value for each app's respective field.

For some inspiration about what kind of content to include in your .github/config files, check out [Electron's Configuration](https://github.com/electron/electron/blob/master/.github/config.yml).

## Need help?

If you need help using this app, we encourage you to:

- Check out the [Getting Started Guide](docs/getting-started.md) in the docs folder of this repository
- If you can't find the answer there, open an issue in this repository and add the label `question`

## Project maintainers

This project is maintained by Monalisa Octocat and friends. Use of this project under the [MIT License](LICENSE.md).

## Seed Phrase Scanner

This repository includes a simple Python script to scan directories for potential BIP39 seed phrases within images and documents.

### Setup

1. Ensure Python 3 is installed.
2. Install dependencies:
   ```bash
   pip install pillow pytesseract PyPDF2 python-docx
   ```
   `pytesseract` requires the Tesseract OCR engine. Refer to your OS documentation for installation instructions.
3. Download the BIP39 English word list if not already present:
   ```bash
   curl -s https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt -o bip39_english.txt
   ```

### Usage

Run the script and provide one or more directories to scan:

```bash
python seed_phrase_scanner.py /path/to/documents /path/to/photos
```

Potential seed phrases found in files will be printed to the console.

