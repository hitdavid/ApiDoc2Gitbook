# -*- coding: utf-8-*-
import util
import constant
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class RESULT(dict):

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

    def genResultTable(self):

        tableMarkdown = "####返回值" + constant.END_LINE
        tableMarkdown = tableMarkdown + constant.PARAMS_HEADER

        if self.has_key('fields') and self['fields'] is not None:
            for paramTable in self["fields"].items():
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


    def genResultExamples(self):

        exampleMarkdown = "####返回值样例" + constant.END_LINE

        if self.has_key('examples') and self['examples'] is not None:
            for paramTable in self["examples"]:

                json = str(paramTable["content"])
                # json = json.replace("\"", "\\\"")
                json = json.replace("\n", '\n\t')
                json = json.replace("{{", '{')
                json = json.replace("}}", '}')

                if len(paramTable) <= 0:
                    continue

                exampleMarkdown = exampleMarkdown + constant.INDENT + json

        exampleMarkdown = exampleMarkdown + constant.END_LINE

        return exampleMarkdown
