# -*- coding: utf-8-*-
import util
import constant
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class PARAM(dict):

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


    def genTd(self, fields, key):
        if fields.has_key(key) and fields[key] is not None:
            s = fields[key]
            if s == True or s == False:
                s = str(s)
            return util.filter_tags(s)
        else:
            return "-"

    def genParamsTable(self):

        tableMarkdown = "####参数列表" + constant.END_LINE
        tableMarkdown = tableMarkdown + constant.PARAMS_HEADER

        paramTable = []
        for paramTable in self.items():
            # print paramTable
            if len(paramTable) <= 0:
                continue
            for line in paramTable[1]:

                tableMarkdown = tableMarkdown + "|" + self.genTd(line, "field")
                tableMarkdown = tableMarkdown + "|" + self.genTd(line, "type")
                tableMarkdown = tableMarkdown + "|" + self.genTd(line, "optional")
                tableMarkdown = tableMarkdown + "|" + self.genTd(line, "description")
                tableMarkdown = tableMarkdown + "|" + constant.END_LINE

        tableMarkdown = tableMarkdown + constant.END_LINE

        return tableMarkdown







