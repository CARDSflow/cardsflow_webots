#! /usr/bin/env python

import shutil
import os
import string
import sys
import xml
import parserURDF
#import trainingSDF
import writeProto

#from xacro import xacro

from xml.dom import minidom


xmlFile = sys.argv[1]
domFile = minidom.parse(xmlFile)

#extension = os.path.splitext(xmlFile)[1]
#if extension == '.xacro':
#    xacro.main()

for child in domFile.childNodes:
    '''
    if child.localName == 'gazebo':
        print 'this is a sdf file'
        robotName = trainingSDF.getModelName(domFile)
        protoFile = xmlFile.strip('.model')
        protoFile=open(protoFile+'.proto','w')
        writeProto.header(protoFile,xmlFile,robotName)
        writeProto.declaration(protoFile,robotName)
        for Node in domFile.getElementsByTagName('link'):
            writeProto.SDFLink(protoFile,Node)
        protoFile.write('       ]\n')
        protoFile.write('   }\n')
        protoFile.write('}\n')
        protoFile.close()
        exit(0)

    elif child.localName == 'robot':
        print 'this is an urdf file'''
    if child.localName == 'robot':
        robotName = parserURDF.getRobotName(child)
        protoFile = os.path.splitext(xmlFile)[0]
        robot = child
        protoFile = open(protoFile+'.proto','w')
        writeProto.header(protoFile,xmlFile,robotName)
        writeProto.declaration(protoFile,robotName)
        linkElementList = []
        jointElementList = []
        for child in robot.childNodes:
            if child.localName == 'link':
                linkElementList.append(child)
            elif child.localName == 'joint':
                jointElementList.append(child)

        linkList = []
        jointList = []
        parentList = []
        childList = []
        rootLink = parserURDF.Link()
        
        for joint in jointElementList:
            jointList.append(parserURDF.getJoint(joint))
            parentList.append(jointList[-1].parent.encode("ascii"))
            childList.append(jointList[-1].child.encode("ascii"))
        parentList.sort()
        childList.sort()
        for link in linkElementList:
            linkList.append(parserURDF.getLink(link))
            if parserURDF.isRootLink(linkList[-1].name,childList):
                rootLink = linkList[-1]
                print 'root link is ' + rootLink.name
        pluginList = parserURDF.getPlugins(robot)
        print 'there is ' + str(len(linkList)) + ' links, ' + str(len(jointList)) + ' joints and ' + str(len(pluginList)) + ' plugins'

        writeProto.URDFLink(protoFile, rootLink, 3, parentList, childList, linkList, jointList)
        protoFile.write('    ]\n')
        writeProto.basicPhysics(protoFile)
        protoFile.write('  }\n')
        protoFile.write('}\n')
        protoFile.close()
        exit(1)
print 'could not read file'







