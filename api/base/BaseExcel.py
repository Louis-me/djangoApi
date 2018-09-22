__author__ = 'shikun'
import xlsxwriter
import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class OperateReport:
    def __init__(self, wd):
        self.wd = wd

    def init(self, worksheet, data):
        # 设置列行的宽高
        worksheet.set_column("A:A", 15)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 20)
        worksheet.set_column("D:D", 20)

        worksheet.set_row(1, 30)
        worksheet.set_row(2, 30)
        worksheet.set_row(3, 30)
        worksheet.set_row(4, 30)
        worksheet.set_row(5, 30)
        worksheet.set_row(6, 30)
        worksheet.set_row(7, 30)

        define_format_H1 = get_format(self.wd, {'bold': True, 'font_size': 18})
        define_format_H2 = get_format(self.wd, {'bold': True, 'font_size': 14})
        define_format_H1.set_border(1)

        define_format_H2.set_border(1)
        define_format_H1.set_align("center")
        define_format_H2.set_align("center")
        define_format_H2.set_bg_color("blue")
        define_format_H2.set_color("#ffffff")

        worksheet.merge_range('A1:E1', '测试报告总概况', define_format_H1)
        worksheet.merge_range('A2:E2', '接口测试测试概括', define_format_H2)

        _write_center(worksheet, "A3", '测试日期', self.wd)
        _write_center(worksheet, "A4", '测试耗时', self.wd)
        _write_center(worksheet, "A5", '用例总数', self.wd)

        _write_center(worksheet, "B3", data['start_time'], self.wd)
        _write_center(worksheet, "B4", data['sum_time'], self.wd)
        _write_center(worksheet, "B5", data['sum_case'], self.wd)

        _write_center(worksheet, "C3", "通过总数", self.wd)
        _write_center(worksheet, "C4", "失败总数", self.wd)
        _write_center(worksheet, "C5", "未检测", self.wd)

        # data1 = {"test_sum": 100, "test_success": 80, "test_failed": 20, "test_date": "2018-10-10 12:10"}
        _write_center(worksheet, "D3", data['passed'], self.wd)
        _write_center(worksheet, "D4", data['failed'], self.wd)
        _write_center(worksheet, "D5", data['no_check'], self.wd)
        pie(self.wd, worksheet)

    def detail(self, worksheet, info):
        # 设置列行的宽高
        worksheet.set_column("A:A", 30)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 20)
        worksheet.set_column("D:D", 20)
        worksheet.set_column("E:E", 20)
        worksheet.set_column("F:F", 20)
        worksheet.set_column("G:G", 20)
        worksheet.set_column("H:H", 20)
        worksheet.set_column("I:I", 20)

        worksheet.set_row(1, 30)
        worksheet.set_row(2, 30)
        worksheet.set_row(3, 30)
        worksheet.set_row(4, 30)
        worksheet.set_row(5, 30)
        worksheet.set_row(6, 30)
        worksheet.set_row(7, 30)
        worksheet.set_row(8, 30)
        worksheet.set_row(9, 30)

        worksheet.merge_range('A1:I1', '测试详情', get_format(self.wd, {'bold': True, 'font_size': 18, 'align': 'center',
                                                                    'valign': 'vcenter', 'bg_color': 'blue',
                                                                    'font_color': '#ffffff'}))
        _write_center(worksheet, "A2", '请求', self.wd)
        _write_center(worksheet, "B2", '方法', self.wd)
        _write_center(worksheet, "C2", '请求参数', self.wd)
        _write_center(worksheet, "D2", '请求说明', self.wd)
        _write_center(worksheet, "E2", '期望值', self.wd)
        _write_center(worksheet, "F2", '响应码 ', self.wd)
        _write_center(worksheet, "G2", '实际结果 ', self.wd)
        _write_center(worksheet, "H2", '是否通过 ', self.wd)
        _write_center(worksheet, "I2", '耗时 ', self.wd)

        temp = 3
        for item in info:
            # print(item)
            _write_center(worksheet, "A" + str(temp), item["url"], self.wd)
            _write_center(worksheet, "B" + str(temp), item["method"], self.wd)
            _write_center(worksheet, "C" + str(temp), item["params"], self.wd)
            _write_center(worksheet, "D" + str(temp), item["name"], self.wd)
            _write_center(worksheet, "E" + str(temp), item["hope"], self.wd)
            _write_center(worksheet, "F" + str(temp), item["code"], self.wd)
            _write_center(worksheet, "G" + str(temp), item["fact"], self.wd)
            if item["result"] == 0:
                result = "通过"
            elif item["result"] == -1:
                result = "失败"
            else:
                result = "未检测"
            _write_center(worksheet, "H" + str(temp), result, self.wd)
            _write_center(worksheet, "I" + str(temp), item["sum_time"], self.wd)

            temp += 1

    def close(self):
        self.wd.close()


def get_format(wd, option={}):
    return wd.add_format(option)


# def link_format(wd):
#     red_format = wd.add_format({
#         'font_color': 'red',
#         'bold': 1,
#         'underline': 1,
#         'font_size': 12,
#     })
def get_format_center(wd, num=1):
    return wd.add_format({'align': 'center', 'valign': 'vcenter', 'border': num})


def set_border_(wd, num=1):
    return wd.add_format({}).set_border(num)


def _write_center(worksheet, cl, data, wd):
    return worksheet.write(cl, data, get_format_center(wd))


def set_row(worksheet, num, height):
    worksheet.set_row(num, height)

    # 生成饼形图


def pie(workbook, worksheet):
    chart1 = workbook.add_chart({'type': 'pie'})
    chart1.add_series({
        'name': '自动化测试统计',
        'categories': '=测试总况!$C$3:$C$5',
        'values': '=测试总况!$D$3:$D$5',
    })
    chart1.set_title({'name': '测试统计'})
    chart1.set_style(10)
    worksheet.insert_chart('A9', chart1, {'x_offset': 25, 'y_offset': 10})


if __name__ == '__main__':
    sum = {'testSumDate': '25秒', 'sum': 10, 'pass': 5, 'testDate': '2017-06-05 15:26:49', 'fail': 5,
           'appVersion': '17051515', 'appSize': '14M', 'appName': "'简书'"}
    info = [{"id": 1, "title": "第一次打开", "caseName": "testf01", "result": "通过", "phoneName": "三星"},
            {"id": 1, "title": "第一次打开",
             "caseName": "testf01", "result": "通过", "img": "d:\\1.PNG", "phoneName": "华为"}]
    workbook = xlsxwriter.Workbook('Report.xlsx')
    worksheet = workbook.add_worksheet("测试总况")
    worksheet2 = workbook.add_worksheet("测试详情")
    bc = OperateReport(wd=workbook)
    bc.init(worksheet, sum)
    bc.detail(worksheet2, info)
    bc.close()
    #
