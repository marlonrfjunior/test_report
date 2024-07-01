import unittest
from test_report import *


@Step(name="First step", description="This is the first step in the test case.")
def first_step():
    pass

@Step(name="Second step", description="This is the second step in the test case.")
def second_step():
    pass

@Step(name="Third step", description="This is the third step in the test case.")
def third_step():
    raise AssertionError("Force the test to fail.")

@Test_case(name="First test case")
def first_test_case():
    first_step()
    second_step()

@Test_case(name="Second test case")
def second_test_case():
    first_step()
    second_step()

@Test_case(name="Third test case")
def third_test_case():
    first_step()
    second_step()
    third_step()

class Tests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
       pass

    @classmethod
    # @SetupReport(report_destination_path="results/", image_path="image.png")
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

    


