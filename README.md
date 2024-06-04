# pyexpenses
## Expense Tracker implemented in Python

## Table of Content
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Getting Started
- It consists of an expense tracker implemented in Python in CLI mode.
- It consists of two main modes: Register or Login.
- After the user successfully logs in, the user can continously operate for expenses including operations like Adding Expenses, Viewing Expenses, Editing Expenses and Deleting Expenses. It also includes a quit option.
- It is connected with the database using [cs50](https://www.pypi.org/project/cs50).
- It includes a password hashing feature implemented using [werkzeug](https://www.pypi.org/project/werkzeug).
- It includes [PrettyTable](https://www.pypi.org/project/prettytable) feature for displaying the table on the console in a beautified manner.
- For getting the password, it implements [getpass4](https://www.pypi.org/project/getpass4) in a secure manner.

## Usage
Downloading the github repository

```bash
git clone https://www.github.com/nishant-2908/pyexpenses.git
```

Downloading the dependencies
```bash
pip install -r requirements.txt
```
Running the program
```bash
python main.py
```

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
Feel free to customize this README.md file to provide more specific details about your project.
Let me know if there's anything else I can help you with!