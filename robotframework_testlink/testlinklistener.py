import re
from robot.api import logger as robot_logger
from testlink import TestlinkAPIClient
from testlink.testreporter import TestGenReporter
from testlink.testlinkerrors import TLResponseError
from testlink import TestLinkHelper
from .variables import Variables


class CustomGenReporter(TestGenReporter):
    """Ovveridden method to pass 3045 and 3046 exceptions"""

    def ensure_testcases_in_plan(self):
        # Get the platformid if possible or else addition will fail
        for testcase in self.testcases:
            # Can't check if testcase is in plan_tcids, because that won't work if it's there, but of the wrong platform
            try:
                self.tls.addTestCaseToTestPlan(
                    self.testprojectid, self.testplanid, testcase, self.get_latest_tc_version(testcase),
                    platformid=self.platformid
                )
            except TLResponseError as e:
                # Test Case version is already linked to Test Plan
                if e.code == 3046 or e.code == 3045:
                    pass
                else:
                    raise


class testlinklistener(object):
    ROBOT_LISTENER_API_VERSION = 3
    robot_variables = Variables()
    TESTCASE_SUFFIX = re.compile(r"-T\d+$")

    def __init__(self):
        """
        Listener class
        """

        self.also_console = False
        # This attributes will be overridden in self.start_suite.
        #   Because the RobotFramework variables are passed when testing started
        self.tls = None
        self.report_kwargs = None
        self.test_prefix = None

    def _get_testlink_status(self, test):
        # testlink accepts p/f for passed and failed
        status = 'f'
        if test.passed:
            status = 'p'
        return status

    def _get_prefix_from_testlink(self, projectname):
        for project in self.tls.getProjects():
            if project["name"] == projectname:
                return project["prefix"]

    def _get_reporter(self, test):
        """Update kwargs and get TestReporter"""
        self.report_kwargs['status'] = self._get_testlink_status(test)
        try:
            testcase = re.sub(r"-\w\d+$", re.findall(self.TESTCASE_SUFFIX, test.name)[0].replace("T", ""), test.name)
        except IndexError:
            testcase = []
        return CustomGenReporter(self.tls, testcase, **self.report_kwargs)

    def start_suite(self, data, result):
        self.robot_variables.check_variables()
        if self.tls is None:
            self.tls = TestLinkHelper(self.robot_variables.server, self.robot_variables.devkey).connect(TestlinkAPIClient)
        self.report_kwargs = self.robot_variables.get_report_kwargs()
        self.test_prefix = self._get_prefix_from_testlink(self.robot_variables.testprojectname)

    def end_test(self, data, test):
        # reporter = self._get_reporter(test)
        if self.tls is not None and self.report_kwargs is not None and self.test_prefix is not None:
            reporter = self._get_reporter(test)
            # This is supposed to default to true by the API spec, but doesn't on some testlink versions
            for result in reporter.reportgen():
                # Listeners don't show up in the xml log so setting also_console to False effectively means don't log
                # Listeners do log to ROBOT_SYSLOG_FILE in the end_test stage, however that isn't enabled by default
                robot_logger.info(result, also_console=self.also_console)
