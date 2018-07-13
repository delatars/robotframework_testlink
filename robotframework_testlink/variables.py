from robot.libraries.BuiltIn import BuiltIn


class Variables(object):
    """Container for listener settings."""
    # dict with attributes {reportTCResult_api_method_attribute : RobotFramework variable}
    # See testlink api documentation for all available reportTCResult api method attributes.
    ROBOT_MANDATORY_VARS = {'server': 'RT_SERVER',
                            'devkey': 'RT_APIKEY',
                            'testprojectname': 'RT_PROJECT',
                            'testplanname': 'RT_TESTPLAN',
                            'buildname': 'RT_BUILD',
                            'platformname': 'RT_PLATFORM'}
    ERROR = False

    def __init__(self):
        self.server = None
        self.devkey = None
        self.testprojectname = None
        self.testplanname = None
        self.buildname = None
        self.platformname = None
        self.execduration = None
        self.steps = None
        self.user = None
        self.notes = None

    def check_variables(self):
        """Check input variables for listener.
        Example: pybot --listener robotframework_testlink_listener -v RT_APIKEY:93kasldh8a23ls9das
        Parameters list:
        RT_SERVER - <url> for connection with Testlink api.
                      Example: http://testlink.drw/lib/api/xmlrpc/v1/xmlrpc.php
        RT_APIKEY - apikey for connection with Testlink api.
        RT_PLATFORM - platform name in Testlink.
        RT_PROJECT - project name in Testlink.
        RT_TESTPLAN - testplan name in Testlink.
        RT_BUILD - build version which wil be created automatically or used existed.
        """
        # Check for mandatory variables
        errors = []
        for testlink_var, robot_var in Variables.ROBOT_MANDATORY_VARS.items():
            robot_var_value = get_variable(robot_var, default=None)
            if robot_var_value is None:
                errors.append(robot_var)
                self.ERROR = True
            else:
                setattr(self, testlink_var, robot_var_value)
        if self.ERROR:
            raise AssertionError(
                    "Missing parameters %s for robot run\n"
                    "You should pass -v <variable>:<value>" % errors)
        # Set other values
        self.execduration = get_variable("RT_EXEC_DURATION", default=None)
        self.steps = get_variable("RT_STEPS", default=None)
        self.user = get_variable("RT_USER", default=None)
        self.notes = get_variable("RT_NOTES", default=None)

    def get_report_kwargs(self):
        report_kwargs = {attr: val for attr, val in self.__dict__.items()
                         if not attr.startswith('_') and attr != "server" and val is not None}
        return report_kwargs


def get_variable(robot_variable, default=None):
    """Returns the found robot variable, defaults to None."""
    return BuiltIn().get_variable_value("${" + str(robot_variable) + "}", default=default)


def get_input_as_list(input_):
    if isinstance(input_, list):
        return input_
    else:
        return [input_]
