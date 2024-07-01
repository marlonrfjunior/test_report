from .models import *
from .views  import *
import time
import os
from functools import wraps

class NoTestReportControllerFoundError(Exception):
    pass

class ReportManager:
    _instance = None
    screenshot_function = None
    image_path = None
    report_destination_path = ""

    @classmethod
    def get_controller(cls):
        if cls._instance is None:
            cls._instance = TestReportController()
        return cls._instance
    
    @classmethod
    def get_screenshot_function(cls):
        if cls.screenshot_function is None:
            print(
                        "\nError retrieving screenshot function. Check if your screenshot callback function is implemented "
                        "in the code with the @GetScreenshot decorator.\nFor example:\n\n"
                        "Appium:\n"
                        "    @GetScreenshot\n"
                        "    def get_screenshot(self):\n"
                        "        return self.driver.get_screenshot_as_png()")  
        return cls.screenshot_function
    
    @classmethod
    def set_screenshot_function(cls,function):
        cls.screenshot_function = function
      
    @classmethod
    def set_report_configurations(cls,image_path,report_destination_path):
        cls.image_path = image_path
        cls.report_destination_path = report_destination_path


def GetScreenshot(func):
    ReportManager.set_screenshot_function(func)
    return func
    

def Step(name: str, status: bool = False, description=None, get_screenshot=False):
    def decorator_function(original_function):
        @wraps(original_function)
        def wrapper_function(*args, **kwargs):
            instance = args[0] if args else None
            step = Step_class(name=name, status=status, description=description)
            controller = ReportManager.get_controller()
            try:
                result = original_function(*args, **kwargs)
                step.set_status(True)
            except Exception as e:
                step.set_status(False)
                step.set_description(f"Error executing '{name}': {str(e)}")
                step.set_screenshot(png=ReportManager.get_screenshot_function()(instance))
                raise 
            finally:
                if get_screenshot:
                    step.set_screenshot(png=ReportManager().get_screenshot_function()(instance))
                step.set_execution_time(time.time())
                controller.add_step(step)
            return result
        return wrapper_function
    return decorator_function

def Test_case(name: str):
    def decorator_function(original_function):
        @wraps(original_function)
        def wrapper_function(*args, **kwargs):
            test_case = TestCase_class(name=name)
            controller = ReportManager.get_controller()
            controller.add_test_case(test_case)
            try:
                result = original_function(*args, **kwargs)
            except Exception as e:
                raise 
            return result
        return wrapper_function
    return decorator_function

def Scenario(name: str):
    def decorator_function(original_function):
        @wraps(original_function)
        def wrapper_function(*args, **kwargs):
            scenario = Scenario_class(name=name)
            controller = ReportManager.get_controller()
            controller.add_scenario(scenario)
            try:
                result = original_function(*args, **kwargs)
            except Exception as e:
                raise 
            return result
        return wrapper_function
    return decorator_function

def GenerateReport(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            controller = ReportManager.get_controller()
            report_html = controller.generate_report()
            try:
                file_path = os.path.join(ReportManager.report_destination_path, "relatorio.html")
                directory = os.path.dirname(file_path)
                if not os.path.exists(directory):
                    os.makedirs(directory)
            except:
                file_path="relatorio.html"
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(report_html)
        except Exception as e :
            print(f"Report could not be generated: | Error : {e}")
        return func(*args, **kwargs)
    return wrapper

def SetupReport(image_path: str = None, report_destination_path : str= ""):
    def decorator_function(original_function):
        @wraps(original_function)
        def wrapper_function(*args, **kwargs):
            try:
                ReportManager.set_report_configurations(image_path,report_destination_path)
                result = original_function(*args, **kwargs)
            except Exception as e:
                raise 
            return result
        return wrapper_function
    return decorator_function

class TestReportController:
    def __init__(self):
        self.scenarios = []
        self.step = None

    def add_scenario(self, scenario: Scenario):
        self.scenarios.append(scenario)


    def add_test_case(self, test_case: TestCase_class):
        index = len(self.scenarios) - 1 if self.scenarios else None;
        if index == None : raise Exception("Empty Array")
        self.scenarios[index].test_cases.append(test_case)

    def add_step(self, step: Step_class):
        index = len(self.scenarios) - 1 if self.scenarios else None;
        if index == None : raise Exception("Empty Array")
        test_cases = self.scenarios[index].test_cases
        index = len(test_cases) - 1 if test_cases else None;
        if index == None : raise Exception("Empty Array")
        test_cases[index].steps.append(step)
        

    def generate_report_data(self):
        report_data = {
            "scenarios": [scenario.to_dict() for scenario in self.scenarios],
            "total_tests": sum(len(scenario.test_cases) for scenario in self.scenarios),
            "total_failures": sum(not test_case.get_status_result() for scenario in self.scenarios for test_case in scenario.test_cases),
            "total_execution_time": self.format_time(sum(scenario.get_execution_time() for scenario in self.scenarios)),
            "image_header_path": ReportManager.image_path
        }
        return report_data

    def generate_report(self):
        report_data = self.generate_report_data()
        return generate_report_html(report_data)
    
    def format_time(self,total_seconds):
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int((total_seconds - int(total_seconds)) * 1000)
        return f"{minutes:02}:{seconds:02}.{milliseconds:03}"