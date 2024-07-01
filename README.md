# Test Report Generator Library 

## Overview 

The `test_report_generator` library is designed to facilitate the creation of automated test reports. It provides decorators for defining steps, test cases, scenarios, and generating reports.

## Installation 🚀

To install the `test_report_generator` library, use the following command:

```bash
pip install test_report_generator
```
## Usage 🛠️

### Decorators 🎨
The library includes several decorators to enhance your test cases and generate detailed reports.

- @Step: Defines a step within a test case.
- @TestCase: Defines a test case consisting of multiple steps.
- @Scenario: Defines a scenario that includes one or more test cases.
- @GenerateReport: Generates a test report after the tests are executed.
- @SetupReport: Sets up the report configuration before executing the tests.
- @GetScreenshot:

### Example 🌟
Here's an example of how to use the test_report library with unittest:

```python
import unittest
from test_report import *

@Step(name="First step", description="This is the first step in the test case.")
def first_step():
    pass

@Step(name="Second step", description="This is the second step in the test case.")
def second_step():
    pass

@Step(name="Third step", description="This is the third step in the test case.", get_screenshot=True)
def third_step():
    raise AssertionError("Force the test to fail.")

@TestCase(name="First test case")
def first_test_case():
    first_step()
    second_step()

@TestCase(name="Second test case")
def second_test_case():
    first_step()
    second_step()

@TestCase(name="Third test case")
def third_test_case():
    first_step()
    second_step()
    third_step()

class Tests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
       pass

    @classmethod
    @GenerateReport
    def tearDownClass(cls) -> None:
        pass

    @Scenario(name="First scenario")
    def test_first_scenario(self):
        first_test_case()

    @Scenario(name="Second scenario")
    def test_second_scenario(self):
        first_test_case()
        second_test_case()

    @Scenario(name="Third scenario")
    def test_third_scenario(self):
        first_test_case()
        second_test_case()
        third_test_case()

if __name__ == '__main__':
    unittest.main()
```

### How It Works 🧩
- **Steps**: Define the individual steps of your test cases using the `@Step` decorator.
  ```python
  @Step(name="Step Name", description="Step Description", get_screenshot=True)
  def step_function():
      # Step implementation
      pass
  ```
    - name (str): The name of the step.
    - description (str): A brief description of what the step does.
    - get_screenshot(bool): Whether a screenshot should be taken during the execution of the step. (It is necessary to implement a screenshot return function with the driver used returning the screenshot)

- **Test Cases**: Combine steps into test cases using the @TestCase decorator.

  ```python
  @TestCase(name="Test Case Name")
  def test_case_function():
      step_function()
  ```
    - name (str): The name of the test case.
- **Scenarios**: Group test cases into scenarios using the @Scenario decorator.

  ```python
  @Scenario(name="Scenario Name")
  def scenario_method(self):
    test_case_function()
  ```
    - name (str): The name of the scenario.
- **Generate Report**: Automatically generate a test report after executing the test suite by using the @GenerateReport decorator on the tearDownClass method.

  ```python
  @GenerateReport
  @classmethod
  def tearDownClass(cls):
    pass
  ```

- **Setup Report**: Configure report settings before executing the tests using the @SetupReport decorator. This decorator is optional and can be used to change the final destination of the report or include an image.

  ```python
  @SetupReport(report_destination_path="results/", image_path="image.png")
  @classmethod
  def setUpClass(cls):
    pass
  ```
    - report_destination_path (str): The path where the report will be saved.
    - image_path (str): Path to an image to be included in the report.

- **Get Screenshot**: Specify the function responsible for capturing a screenshot during the execution of a step using the @GetScreenshot decorator.

  ```python
  @GetScreenshot
    def get_screenshot(self):
            return self.driver.get_screenshot_as_png()
  ```

## Reporting 📄

The @GenerateReport decorator generates a detailed test report on html, including the results of each step and test case. This report can be customized and saved to a specified directory.

## Contributing 🤝

If you would like to contribute to the development of this library, please submit a pull request or open an issue on GitHub.

## License 📝

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please contact 
- 📧 [Email : marlonrfjunior@gmail.com](mailto:marlonrfjunior@gmail.com)
- 💼  [LinkedIn : Marlon Junior](https://www.linkedin.com/in/marlonrfjunior)