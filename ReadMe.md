# SWO Viewer

SWO Viewer is a Python project designed to parse and visualize Serial Wire Output (SWO) data from embedded systems.

The goal is to expand the project to make collection and visualization of SWO Trace data as simple as possible.

## Features

- Parse SWO data packets
- Visualize protocol states
- Handle various ITM protocol states

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/sidprice/swo_viewer.git
    cd swo_viewer
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the SWO Viewer, execute the following command:

```bash
python main.py
```

## Running Tests

To run the tests and check code coverage, use the following commands:

1. Run tests and check coverage:

    ```bash
    coverage run -m pytest
    ```

2. Generate a coverage report:

    ```bash
    coverage report
    ```

3. Generate an HTML coverage report:

    ```bash
    coverage html
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the GPLv3 License.
