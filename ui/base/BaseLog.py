import logging
import time
import os
from time import sleep
import threading

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class Log:
    def __init__(self, devices):
        # global logger, result_path, log_path
        self.check_no = 0
        result_path = PATH("../log/")
        # log_path = os.path.join(result_path, (devices + time.strftime('%Y%m%d%H%M%S', time.localtime())))
        self.log_path = os.path.join(result_path, devices)
        # if not os.path.exists(log_path):
        #     os.makedirs(log_path)
        # self.check_no = 0
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # create handler,write log
        fh = logging.FileHandler(self.log_path)
        # Define the output format of formatter handler
        formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)

    def build_start_line(self, case_no):
        """build the start log
        :param case_no:
        :return:
        """
        start_line = "----  " + case_no + "   " + "   " + \
                     "  ----"
        # startLine = "----  " + case_no + "   " + "START" + "   " + \
        #             "  ----"
        self.logger.info(start_line)

    def build_end_line(self, case_no):
        """build the end log
        :param case_no:
        :return:
        """
        end_line = "----  " + case_no + "   " + "END" + "   " + \
                   "  ----"
        self.logger.info(end_line)

    def write_result(self, result):
        """write the case result(OK or NG)
        :param result:
        :return:
        """
        report_path = os.path.join(self.log_path, "report.txt")
        flogging = open(report_path, "a")
        try:
            flogging.write(result + "\n")
        finally:
            flogging.close()
        pass

    def result_ok(self, case_no):
        self.write_result(case_no + ": OK")

    def case_ng(self, case_no, reason):
        self.write_result(case_no + ": NG--" + reason)

    def check_point_ok(self, info):
        self.check_no += 1
        self.logger.info("[CheckPoint_" + str(self.check_no) + "]: " + info + ": OK")

    def check_point_ng(self, driver, info, uid):
        """write the case's check_point_NG
        :param info:
        :param driver:
        :return:
        """
        self.check_no += 1

        self.logger.info("[CheckPoint_" + str(self.check_no) + "]: " + info + ": NG")
        # take shot
        return self.screenshot_ng(driver, uid)

    def screenshot_ng(self, driver, uid):
        """screen shot
        :param uid:
        :param driver:
        :return:
        """
        name = os.path.join(PATH("../log/"), "CheckPoint_" + str(self.check_no) + "_" + uid + "_NG.png")
        # wait for animations to complete before taking screenshot
        sleep(1)
        driver.get_screenshot_as_file(name)
        # return os.path.join(screenshotPath + screenshotName)
        return name
