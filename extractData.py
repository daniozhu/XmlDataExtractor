import os
import os.path
from lxml import etree

result_path="C:/Temp/iMarkResult/Parts/result.csv"
rootdir = "C:/Temp/iMarkResult/Parts"
step = "Rebuild3"
step_xpath="//checkpoint[@label='%s']/datalist/data[@type='wallclocktime']/text()" % step
step_ondraw_xpath="//checkpoint[@label='%s']/checkpoint[@label='SMxSceneView::_OnDraw']/datalist/data[@type='wallclocktime']/text()" % step

if(os.path.exists(result_path)):
    os.remove(result_path)
    
resultfile = open(result_path,"w")
resultfile.write("RunSequence,%s,_OnDraw\n"%step)

for parent,dirnames,filenames in os.walk(rootdir):
    for f in filenames:
        file_parts=f.split('.',1)
        if(file_parts[1] != "xml"):
            continue
        
        file_without_ext = file_parts[0]
        run_sequence = file_without_ext.split('_',10)[-1][3:]
        #print(run_sequence)

        fullpath=os.path.join(parent,f) 
        #print(fullpath)
        selector=etree.parse(fullpath)
        nodes=selector.xpath(step_xpath)
        time_all=int(nodes[0])/1000
        #print(time_all)

        ondraw_nodes = selector.xpath(step_ondraw_xpath)
        time_ondraw=int(ondraw_nodes[0])/1000
        #print(time_ondraw)
        resultfile.write("%s,%s,%s\n" % (run_sequence, time_all, time_ondraw))
        
resultfile.close()
