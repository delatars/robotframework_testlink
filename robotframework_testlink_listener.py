from robotframework_testlink.testlinklistener import testlinklistener
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class robotframework_testlink_listener(testlinklistener):
    """This is a customized listener to report a theoretical org's testlink status.

    The testplanid should be passed in as an arg to the listener like `testplanid=<testplanid>`.

    The platform name can be passed in as an arg `platformname=<platformname>` or it can be a variable
    `testlinkplatform` inside the test.
    """
    def __init__(self):
        """
        This org has an automation devkey, uses a externaltestcase prefix of 'abc' and wants this listener to only
        report on project 'MyProject'.
        So it sets logical defaults for the organization. i.e. server_url, automation_devkey, test_prefix

        Variables likely grabbed from the test:
            - ${testlinktestplanname}
            - ${testlinkplatformname}
        Variables likely grabbed from the commandline:
            testlinkbuildname: The build name to use/create.
        """
        super(robotframework_testlink_listener, self).__init__()
