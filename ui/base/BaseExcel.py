# -*- coding=utf-8 -*-
import json

__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class OperateReport:
    def __init__(self, wd):
        self.wd = wd

    def init(self, worksheet, data):
        self.__init_title(worksheet)
        self.__write_center(worksheet, "A3", '测试日期')
        self.__write_center(worksheet, "A4", '测试耗时')
        self.__write_center(worksheet, "A5", '用例总数')
        self.__write_center(worksheet, "B3", data['start_time'])
        self.__write_center(worksheet, "B4", data['sum_time'])
        self.__write_center(worksheet, "B5", data['sum_case'])

        self.__write_center(worksheet, "C3", "通过总数")
        self.__write_center(worksheet, "C4", "失败总数")
        self.__write_center(worksheet, "C5", "浏览器")
        self.__write_center(worksheet, "D3", data['passed'])
        self.__write_center(worksheet, "D4", data['failed'])
        self.__write_center(worksheet, "D5", "chrome")
        self.__pie(worksheet)

    def __init_title(self, worksheet):
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

        define_format_H1 = self.__get_format({'bold': True, 'font_size': 18})
        define_format_H2 = self.__get_format({'bold': True, 'font_size': 14})
        define_format_H1.set_border(1)

        define_format_H2.set_border(1)
        define_format_H1.set_align("center")
        define_format_H2.set_align("center")
        define_format_H2.set_bg_color("blue")
        define_format_H2.set_color("#ffffff")

        worksheet.merge_range('A1:E1', '测试报告总概况', define_format_H1)
        worksheet.merge_range('A2:E2', '测试测试概括', define_format_H2)

    def detail(self, worksheet, info):
        # print("=datail=%s=" % info)
        self.__detail_title(worksheet)
        temp = 3
        for item in info:
            # print(item)
            self.__write_center(worksheet, "A" + str(temp), item["name"])
            self.__write_center(worksheet, "B" + str(temp), item["step"])
            self.__write_center(worksheet, "C" + str(temp), item["hope"])
            self.__write_center(worksheet, "E" + str(temp), item["extend"])
            if item["result"] == 0:
                result = "通过"
            elif item["result"] == -1:
                result = "失败"
            else:
                result = "未检测"
            self.__write_center(worksheet, "D" + str(temp), result)


            if item.get("img", "false") == "false":
                self.__write_center(worksheet, "F" + str(temp), "")
                worksheet.set_row(temp, 30)
            else:
                worksheet.insert_image('F' + str(temp), item["img"],
                                       {'x_scale': 0.1, 'y_scale': 0.1, 'border': 1})
                worksheet.set_row(temp - 1, 110)
            self.__write_center(worksheet, "G" + str(temp), item["sum_time"])

            temp += 1

    def __detail_title(self, worksheet):
        # 设置列行的宽高
        worksheet.set_column("A:A", 30)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 20)
        worksheet.set_column("D:D", 20)
        worksheet.set_column("E:E", 20)
        worksheet.set_column("F:F", 20)
        worksheet.set_column("G:G", 20)

        worksheet.set_row(1, 30)
        worksheet.set_row(2, 30)
        worksheet.set_row(3, 30)
        worksheet.set_row(4, 30)
        worksheet.set_row(5, 30)
        worksheet.set_row(6, 30)
        worksheet.set_row(7, 30)

        worksheet.merge_range('A1:G1', '测试详情', self.__get_format({'bold': True, 'font_size': 18, 'align': 'center',
                                                                    'valign': 'vcenter', 'bg_color': 'blue',
                                                                    'font_color': '#ffffff'}))
        self.__write_center(worksheet, "A2", '用例名')
        self.__write_center(worksheet, "B2", '步骤')
        self.__write_center(worksheet, "C2", '检查点')
        self.__write_center(worksheet, "D2", '是否通过 ')
        self.__write_center(worksheet, "E2", '备注 ')
        self.__write_center(worksheet, "F2", '截图 ')
        self.__write_center(worksheet, "G2", '耗时 ')

    def close(self):
        self.wd.close()

    def __get_format(self, option={}):
        return self.wd.add_format(option)

    def __write_center(self, worksheet, cl, data):
        return worksheet.write(cl, data, self.__get_format_center())

    def __get_format_center(self, num=1):
        return self.wd.add_format({'align': 'center', 'valign': 'vcenter', 'border': num})

    # 生成饼形图
    def __pie(self, worksheet):
        chart1 = self.wd.add_chart({'type': 'pie'})
        chart1.add_series({
            'name': '自动化测试统计',
            'categories': '=测试总况!$C$3:$C$4',
            'values': '=测试总况!$D$3:$D$4',
        })
        chart1.set_title({'name': '测试统计'})
        chart1.set_style(10)
        worksheet.insert_chart('A9', chart1, {'x_offset': 25, 'y_offset': 10})


if __name__ == '__main__':
    pass
