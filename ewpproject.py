# -*- coding: utf-8 -*-

from lxml import objectify
    
class EWPProject (object):
    
    def __init__(self, path, xmlFile):
                
        self.project = {}
        self.path = path
        self.xmlFile = xmlFile
        xmltree = objectify.parse(xmlFile)
        self.root = xmltree.getroot()

    def parseProject(self):
        
        self.project['name'] = self.root.configuration.name
        
        self.project['chip'] = ''
    
        #TODO: parse into tree structure  
        self.project['srcs'] = []
        self.searchGroups(self.root, self.project['srcs'])
        
        self.project['defs'] = []
        self.project['incs'] = []
        
        for element in self.root.configuration.getchildren():
            
            if element.tag == 'settings':
                for e in element.data.getchildren():
     
                    if e.tag == 'option':                
                        if e.name.text == 'OGChipSelectEditMenu':                                          
                            self.project['chip'] = e.state 
                        elif e.name.text == 'CCDefines':
                            for d in e.getchildren():
                                if d.tag == 'state' and d.text != None:
                                    self.project['defs'].append(d.text)
                        elif e.name.text == 'CCIncludePath2':
                            for d in e.getchildren():
                                if d.tag == 'state' and d.text != None:
                                    self.project['incs'].append(d.text)
        
        for i in range(0, len(self.project['incs'])):
            self.project['incs'][i] = self.project['incs'][i].replace('$PROJ_DIR$', self.path)
            
          
    def displaySummary(self):
              
        print ('Project Name:' + self.project['name'])
        print ('Project chip:' + self.project['chip'])
        print ('Project includes: ' + ' '.join(self.project['incs']))
        print ('Project defines: ' + ' '.join(self.project['defs']))
        
        #print ('Groups: ')
        #print (self.sources)
        #for src in self.sources:
        #    self.printGroups(src)
            

    def printGroups(self, group):

        print ('Group name:' + group['name'])
        
        for file in group['files']:    
            print ('File: ' + file)
        
        for g in group['groups']:
            self.printGroups(g)

    def searchGroups(self, xml, sources):
        
        group = {}
        group['name'] = ''        
        group['files'] = []
        group['groups'] = []
        
        for element in xml.getchildren():
    
            if element.tag == 'group':
                group['name'] = element.name
                print ('File: ' + group['name'])
                self.searchGroups(element,group['groups'])                
                sources.append(group)
                
            elif element.tag == 'file':  
                print ('File: ' +  element.name)
                group['files'].append(element.name)
        