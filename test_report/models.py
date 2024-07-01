import base64
import time
import uuid

class Step_class:
    def __init__(self, name: str, status: bool = False, description = None):
        self.name = name
        self.description = "" if description is None else description
        self.status = ""
        self.screenshot = None
        self.execution_time = time.time()

    def set_screenshot(self,png = None, path_to_png: str = None, png_in_base64: str = None):
        try:
            if png_in_base64 is not None:
                self.screenshot = png_in_base64 
            if png is not None:
                self.screenshot = base64.b64encode(png).decode('utf-8')
            else:
                with open(path_to_png, "rb") as image_file:
                    self.screenshot = base64.b64encode(image_file.read()).decode('utf-8')
        except :
            self.screenshot = ""

    def set_description(self, description: str):
        self.description = description

    def set_execution_time(self, time: int):
        self.execution_time = time - self.execution_time 
    
    def set_status(self, status=bool):
        self.status=status
    
    def get_formated_execution_time(self):
        total_seconds = self.execution_time 
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int((total_seconds - int(total_seconds)) * 1000)
        return f"{minutes:02}:{seconds:02}.{milliseconds:03}"

    def to_dict(self):
        return {
            "uuid": uuid.uuid4(),
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "screenshot": self.screenshot,
            "execution_time": self.execution_time,
            "formated_execution_time": self.get_formated_execution_time()
        }

class TestCase_class:
    def __init__(self, name: str):
        self.name = name
        self.steps = []
        self.status = False
        self.execution_time = 0

    def add_step(self, step: Step_class):
        self.steps.append(step)

    def set_status_result(self, status: bool):
        self.status = status

    def get_status_result(self):
        for step in self.steps:
                if not step.status:
                    return False  
        return True 


    def get_execution_time(self):
        return sum(step.execution_time for step in self.steps)
    
    def get_formated_execution_time(self):
        total_seconds = sum(step.execution_time for step in self.steps)
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int((total_seconds - int(total_seconds)) * 1000)
        return f"{minutes:02}:{seconds:02}.{milliseconds:03}"
    
    def to_dict(self):
        return {
            "uuid": uuid.uuid4(),
            "name": self.name,
            "status": self.get_status_result(),
            "steps": [step.to_dict() for step in self.steps],
            "execution_time": self.get_execution_time(),
            "formated_execution_time": self.get_formated_execution_time()
        }


class Scenario_class:
    def __init__(self, name: str):
        self.name = name
        self.status = False
        self.test_cases = []

    def add_test_case(self, test_case: TestCase_class):
        self.test_cases.append(test_case)

    def get_status_result(self) -> bool:
        for test_case in self.test_cases:
                if not test_case.get_status_result():
                    return False  
        return True 

    def get_execution_time(self) -> int:
        return sum(test_case.get_execution_time() for test_case in self.test_cases)
    
    def get_formated_execution_time(self):
        total_seconds = sum(test_case.get_execution_time() for test_case in self.test_cases)
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int((total_seconds - int(total_seconds)) * 1000)
        return f"{minutes:02}:{seconds:02}.{milliseconds:03}"
    
    def to_dict(self):
        return {
            "uuid": uuid.uuid4(),
            "name": self.name,
            "status": self.get_status_result(),
            "test_cases": [test_case.to_dict() for test_case in self.test_cases],
            "execution_time": self.get_execution_time(),
            "formated_execution_time": self.get_formated_execution_time()
        }
