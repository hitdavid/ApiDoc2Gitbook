# -*- coding: utf-8-*-
__author__ = 'David'
import os, hashlib
import unirest
import json
import model.api
import constant
import shutil



uriArray = [
    'http://172.18.4.3:8213/apidoc1/apidocs/comment/api_data.js',
    'http://172.18.4.3:8213/apidoc1/apidocs/favorite/api_data.js',
    'http://172.18.4.3:8213/apidoc1/apidocs/relation/api_data.js',
    'http://172.18.4.3:8213/apidoc1/apidocs/notify/api_data.js',
    'http://172.18.4.3:8213/apidoc1/apidocs/quan-web/api_data.js',
    'http://172.18.4.3:8213/apidoc1/apidocs/quan-rest/api_data.js',
    'http://172.18.4.3:8213/apidoc1/apidocs/account/api_data.js',
    'http://172.18.4.3:8213/apidoc1/apidocs/app/api_data.js'
]

def generateMarkdownFile(summary):

    summaryText = '#SUMMARY' + constant.END_LINE
    appendixText = '#APPENDIX' + constant.END_LINE + constant.API_LIST_HEADER

    # print summary

    keys = sorted(summary.keys())

    # print keys

    for key in keys :

        createDir(key)

        summaryText = summaryText + constant.OUTER_LIST_START  + '[' +  key + '](' + ')' + constant.END_LINE

        topLevelTopics = summary[key]

        for subTitle in topLevelTopics:

            parseApiItem(topLevelTopics[subTitle])

            subTitle = correctPath(subTitle)

            createMDFile(key, subTitle, parseApiItem(topLevelTopics[subTitle]))

            summaryText = summaryText + constant.INDENT + constant.LIST_START + '[' + subTitle + '](' + genLink(key, subTitle) + ')' + constant.END_LINE

            appendixText = genAppendixText(appendixText, key, subTitle, topLevelTopics)

    summaryText = summaryText + '- [API列表](appendix.md)'

    genSummary(summaryText)

    genReadme(appendixText)

    genAppendix(appendixText)


def genAppendixText(appendixText, key, subTitle, topLevelTopics):

    appendixText = appendixText + "|" + '[' + subTitle + '](' + genLink(key, subTitle) + ')'
    appendixText = appendixText + "|" + key
    appendixText = appendixText + "|" + model.api.API(topLevelTopics[subTitle]).gendesc()
    appendixText = appendixText + "|" + constant.END_LINE

    return appendixText


def genSummary(text):
    dest = open('./gitbook/SUMMARY.md', 'w')
    dest.write(text)
    dest.close()

def genReadme(text):
    dest = open('./gitbook/README.md', 'w')
    dest.write(text)
    dest.close()

def genAppendix(text):
    dest = open('./gitbook/appendix.md', 'w')
    dest.write(text)
    dest.close()

def parseApiItem(item):
    # print item
    return item.toMD()


def genLink(path, name):
    return '/'+ path + '/' + name + ".md"


def createDir(name):
    os.mkdir('./gitbook/'+name)


def createMDFile(path, name, content):
    dest = open('./gitbook/'+ path + '/' + name + ".md", 'w')
    dest.write(content.encode('utf-8'))
    dest.close()


def cleanFiles():
    if os.path.exists("./gitbook/"):
        shutil.rmtree("./gitbook/")
    os.mkdir('./gitbook/')


def correctPath(title):
    if title.find("/") != -1:
        title = title.replace("/", "_")
        if title.index("_") == 0:
            title = title[1:]
    return title


def main():

    summary = {}

    apis = []

    cleanFiles()

    for currentUri in uriArray:

        response = unirest.get(currentUri)


        jsonString = response.body
        objectStartIndex = jsonString.index('[')
        objectEndIndex = jsonString.rfind('}')
        jsonString = jsonString[objectStartIndex:objectEndIndex]

        jsonDocument = json.loads(jsonString)


        for apiJsonDocument in jsonDocument:
            # print item
            apis.append(apiJsonDocument)

            apiObject = model.api.API(apiJsonDocument)

            if apiJsonDocument.has_key("group") and apiJsonDocument["group"] is not None:

                #忽略处理内部API
                if apiObject.group.find('_') == 0:
                    continue

                if not summary.has_key(apiObject.group.upper()):
                    summary[apiObject.group.upper()] = dict()

                chapter = summary[apiObject.group.upper()]
                if apiJsonDocument.has_key("title") and apiJsonDocument["title"] is not None:
                    apiObject.title = correctPath(apiObject.title)
                    chapter[apiObject.title] = apiObject
                else:
                    continue
            else:
                continue

    generateMarkdownFile(summary)

main()



