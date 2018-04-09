# Contribution guidelines

First of all, thanks for thinking of contributing to this project. :smile:

Before sending a Pull Request, please make sure that you're assigned the task on a GitHub issue.

- If a relevant issue already exists, discuss on the issue and get it assigned to yourself on GitHub.
- If no relevant issue exists, open a new issue and get it assigned to yourself on GitHub.

Please proceed with a Pull Request only after you're assigned. It'd be sad if your Pull Request (and your hardwork) isn't accepted just because it isn't ideologically compatible.

# Developing the library

1. Install PsyNLP locally, with the help of [these installation guidelines](README.md#installation-guidelines).

2. Make your changes in a different git branch (say, `add-new-pipeline`).

3. Run the tests.

    ```sh
    py.test
    ```

4. Lint the code.

    ```sh
    autopep8 --in-place path/to/new/pipeline.py
    ```
5. Send a PR, and patiently wait for a review. :tada:
