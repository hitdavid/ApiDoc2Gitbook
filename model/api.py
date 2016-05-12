# -*- coding: utf-8-*-

import constant, parameter, result, util

class API(dict):

    parent = ''
    parentLink = ''

    success = {}


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



    def toMD(self):

        doc = self.genTitle() + self.genVersion() + constant.END_LINE
        doc = doc + self.gendesc() + constant.END_LINE

        doc = doc + constant.END_LINE
        doc = doc + self.genHttpMethod() + constant.END_LINE
        doc = doc + self.genUrl() + constant.END_LINE



        doc = doc + constant.END_LINE
        doc = doc + constant.END_LINE
        doc = doc + constant.END_LINE

        doc = doc + self.genParams()

        doc = doc + constant.END_LINE
        doc = doc + constant.END_LINE
        doc = doc + constant.END_LINE

        doc = doc + self.genResults()

        doc = doc + constant.END_LINE
        doc = doc + constant.END_LINE
        doc = doc + constant.END_LINE


        doc = doc + self.getFileName() + constant.END_LINE
        return doc

    def genTitle(self):
        title = ''
        if self.has_key('groupTitle') and self['groupTitle'] is not None:
            title = self['groupTitle'] + " - "
        if self.has_key('title') and self['title'] is not None:
            title = title + self['title']

        title = util.filter_tags(title)

        return "###" + title

    def gendesc(self):
        if self.has_key('description') and self['description'] is not None:
            return util.filter_tags(self['description'])
        else:
            return '';

    def genUrl(self):
        if self.has_key('url') and self['url'] is not None:
            return constant.INDENT + '' + self['url'] + ''
        else:
            return '';

    def genHttpMethod(self):
        if self.has_key('type') and self['type'] is not None:
            return "#### HTTP Method: " + self['type']
        else:
            return '';

    def getFileName(self):
        if self.has_key('filename') and self['filename'] is not None:
            self['filename'] = self['filename'].replace('/opt/apps/jenkins/jobs/','')
            return '####文件名称'.decode('utf-8') + constant.END_LINE + constant.END_LINE + constant.INDENT + '' + self['filename'] + ''
        else:
            return '';

    def genVersion(self):
        if self.has_key('version') and self['version'] is not None:
            return "(Ver. " + self['version'] + ")"
        else:
            return '';

    def genParams(self):
        if self.has_key('parameter') and self['parameter'] is not None:
            p = self["parameter"]
            if p.has_key('fields') and p['fields'] is not None:
                params = parameter.PARAM(p['fields'])

                return params.genParamsTable()

        return ''

    def genResults(self):
        if self.has_key('success') and self['success'] is not None:
            results = result.RESULT(self["success"])
            return results.genResultTable() + results.genResultExamples()

        return ''

