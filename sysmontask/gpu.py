#!/usr/bin/env python3
# import gi
# gi.require_version("Gtk", "3.24")

from gi.repository import Gtk as g
import psutil as ps,cairo
from os import popen
from xml.etree.ElementTree import fromstring

try:
    from gi_composites import GtkTemplate
except:
    from sysmontask.gi_composites import GtkTemplate

if __name__=='sysmontask.gpu':
    from sysmontask.sysmontask import files_dir
else:
    from sysmontask import files_dir

@GtkTemplate(ui=files_dir+'/gpu.glade')
class gpuTabWidget(g.ScrolledWindow):

    # Required else you would need to specify the full module
    # name in mywidget.ui (__main__+MyWidget)
    __gtype_name__ = 'gpuTabWidget'
    
    gpuinfolabel = GtkTemplate.Child()
    gpuutildrawarea=GtkTemplate.Child()
    gpuvramdrawarea=GtkTemplate.Child()
    gpuencodingdrawarea=GtkTemplate.Child()
    gpudecodingdrawarea=GtkTemplate.Child()

    gpuvramlabelvalue=GtkTemplate.Child()
    gpuutilisationlabelvalue=GtkTemplate.Child()
    gpuvramusagelabelvalue=GtkTemplate.Child()

    gputemplabelvalue=GtkTemplate.Child()
    gpushaderspeedlabelvalue=GtkTemplate.Child()

    gpudriverlabelvalue=GtkTemplate.Child()
    gpucudalabelvalue=GtkTemplate.Child()
    gpumaxspeedlabelvalue=GtkTemplate.Child()
    gpuvramspeedlabelvalue=GtkTemplate.Child()
    gpuvrammaxspeedlabelvalue=GtkTemplate.Child()

    # Alternative way to specify multiple widgets
    #label1, entry = GtkTemplate.Child.widgets(2)

    def __init__(self):
        super(g.ScrolledWindow, self).__init__()
        
        # This must occur *after* you initialize your base
        self.init_template()
        # self.gpumxfactor=1             #for the scaling of maximum value on the graph

    def givedata(self,secondself):
        self.gpuutilArray=secondself.gpuUtilArray
        self.gpuvramArray=secondself.gpuVramArray
        self.gpuencodingArray=secondself.gpuEncodingArray
        self.gpudecodingArray=secondself.gpuDecodingArray
        self.gputotalvram=int(secondself.totalvram[:-3])

    @GtkTemplate.Callback
    def gpuutildrawarea_draw(self,dr,cr):
        #print("idsaf")
        cr.set_line_width(2)

        w=self.gpuutildrawarea.get_allocated_width()
        h=self.gpuutildrawarea.get_allocated_height()
        scalingfactor=h/100.0
        #creating outer rectangle
        cr.set_source_rgba(0,.454,.878,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()
        # creating grid lines
        verticalGap=int(h/10)
        horzontalGap=int(w/10)
        for i in range(1,10):
            cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
            cr.set_line_width(0.5)
            cr.move_to(0,i*verticalGap)
            cr.line_to(w,i*verticalGap)

            cr.move_to(i*horzontalGap,0)
            cr.line_to(i*horzontalGap,h)
            cr.stroke()
        cr.stroke()
        
        stepsize=w/99.0
        #print("in draw stepsize",stepsize)
        # for i in range(0,99):
        #     # not effcient way to fill the bars (drawing)
        #     cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.gpuutilArray[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-self.gpuutilArray[i+1]))
        #     cr.line_to((i+1)*stepsize,h)
        #     cr.line_to(i*stepsize,h)
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.gpuutilArray[i]))

        #     cr.fill()
        #     cr.stroke()
        #     # for outer line
        #     cr.set_line_width(1.5)
        #     cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.gpuutilArray[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-self.gpuutilArray[i+1]))
        #     cr.stroke()

        cr.set_line_width(1.5)
        cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
        cr.move_to(0,scalingfactor*(100-self.gpuutilArray[0]))
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(100-self.gpuutilArray[i+1]))
        cr.stroke_preserve()

        cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(100-self.gpuutilArray[0]))
        cr.fill()
        cr.stroke()


        return False        
    
    @GtkTemplate.Callback
    def gpuencodingdrawarea_draw(self,dr,cr):
        #print("idsaf")
        cr.set_line_width(2)

        w=self.gpuencodingdrawarea.get_allocated_width()
        h=self.gpuencodingdrawarea.get_allocated_height()
        scalingfactor=h/100.0
        #creating outer rectangle
        cr.set_source_rgba(0,.454,.878,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()
        # creating grid lines
        verticalGap=int(h/10)
        horzontalGap=int(w/10)
        for i in range(1,10):
            cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
            cr.set_line_width(0.5)
            cr.move_to(0,i*verticalGap)
            cr.line_to(w,i*verticalGap)

            cr.move_to(i*horzontalGap,0)
            cr.line_to(i*horzontalGap,h)
            cr.stroke()
        cr.stroke()
        
        stepsize=w/99.0
        #print("in draw stepsize",stepsize)
        # for i in range(0,99):
        #     # not effcient way to fill the bars (drawing)
        #     cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.gpuencodingArray[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-self.gpuencodingArray[i+1]))
        #     cr.line_to((i+1)*stepsize,h)
        #     cr.line_to(i*stepsize,h)
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.gpuencodingArray[i]))

        #     cr.fill()
        #     cr.stroke()
        #     # for outer line
        #     cr.set_line_width(1.5)
        #     cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.gpuencodingArray[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-self.gpuencodingArray[i+1]))
        #     cr.stroke()

        #efficient encoding drawing
        cr.set_line_width(1.5)
        cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
        cr.move_to(0,scalingfactor*(100-self.gpuencodingArray[0]))
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(100-self.gpuencodingArray[i+1]))
        cr.stroke_preserve()

        cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(100-self.gpuencodingArray[0]))
        cr.fill()
        cr.stroke()


        return False

    @GtkTemplate.Callback
    def gpudecodingdrawarea_draw(self,dr,cr):
        #print("idsaf")
        cr.set_line_width(2)

        w=self.gpudecodingdrawarea.get_allocated_width()
        h=self.gpudecodingdrawarea.get_allocated_height()
        scalingfactor=h/100.0
        #creating outer rectangle
        cr.set_source_rgba(0,.454,.878,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()
        # creating grid lines
        verticalGap=int(h/10)
        horzontalGap=int(w/10)
        for i in range(1,10):
            cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
            cr.set_line_width(0.5)
            cr.move_to(0,i*verticalGap)
            cr.line_to(w,i*verticalGap)

            cr.move_to(i*horzontalGap,0)
            cr.line_to(i*horzontalGap,h)
            cr.stroke()
        cr.stroke()
        
        stepsize=w/99.0
        #print("in draw stepsize",stepsize)
        # for i in range(0,99):
        #     # not effcient way to fill the bars (drawing)
        #     cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.gpudecodingArray[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-self.gpudecodingArray[i+1]))
        #     cr.line_to((i+1)*stepsize,h)
        #     cr.line_to(i*stepsize,h)
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.gpudecodingArray[i]))

        #     cr.fill()
        #     cr.stroke()
        #     # for outer line
        #     cr.set_line_width(1.5)
        #     cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.gpudecodingArray[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-self.gpudecodingArray[i+1]))
        #     cr.stroke()

        cr.set_line_width(1.5)
        cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
        cr.move_to(0,scalingfactor*(100-self.gpudecodingArray[0]))
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(100-self.gpudecodingArray[i+1]))
        cr.stroke_preserve()

        cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(100-self.gpudecodingArray[0]))
        cr.fill()
        cr.stroke()

        return False

    @GtkTemplate.Callback
    def gpuvramdrawarea_draw(self,dr,cr):
        # print('heloow  gpu')
        cr.set_line_width(2)

        w=self.gpuvramdrawarea.get_allocated_width()
        h=self.gpuvramdrawarea.get_allocated_height()
        scalingfactor=h/self.gputotalvram
        # print(self.gputotalvram)
        #creating outer rectangle
        cr.set_source_rgba(0,.454,.878,1)  ##need tochange the color
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()
        # creating grid lines
        verticalGap=int(h/10)
        horzontalGap=int(w/10)
        for i in range(1,10):
            cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
            cr.set_line_width(0.5)
            cr.move_to(0,i*verticalGap)
            cr.line_to(w,i*verticalGap)

            cr.move_to(i*horzontalGap,0)
            cr.line_to(i*horzontalGap,h)
        cr.stroke()
        
        stepsize=w/99.0
        #print("in draw stepsize",stepsize)
        # for i in range(0,99):
        #     # not effcient way to fill the bars (drawing)
        #     cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        #     cr.move_to(i*stepsize,scalingfactor*(self.gputotalvram-self.gpuvramArray[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(self.gputotalvram-self.gpuvramArray[i+1]))
        #     cr.line_to((i+1)*stepsize,h)
        #     cr.line_to(i*stepsize,h)
        #     cr.move_to(i*stepsize,scalingfactor*(self.gputotalvram-self.gpuvramArray[i]))

        #     cr.fill()
        #     cr.stroke()
        #     # for outer line
        #     cr.set_line_width(1.5)
        #     cr.set_source_rgba(.384,.749,1.0,1)   #for changing the outer line color
        #     cr.move_to(i*stepsize,scalingfactor*(self.gputotalvram-self.gpuvramArray[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(self.gputotalvram-self.gpuvramArray[i+1]))
        #     cr.stroke()

        cr.set_line_width(1.5)
        cr.set_source_rgba(.384,.749,1.0,1)   #for changing the outer line color
        cr.move_to(0,scalingfactor*(self.gputotalvram-self.gpuvramArray[0]))
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(self.gputotalvram-self.gpuvramArray[i+1]))
        cr.stroke_preserve()

        cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(self.gputotalvram-self.gpuvramArray[0]))
        cr.fill()
        cr.stroke()

        return False



def gpuinit(self):
    ##logic to determine the number of gpus but for now i just focusing on one gpu
    self.isNvidiagpu=1
    self.gpuUtilArray=[0]*100
    self.gpuEncodingArray=[0]*100
    self.gpuDecodingArray=[0]*100
    self.gpuVramArray=[0]*100
    try:
        p=popen('nvidia-smi -q -x')
        xmlout=p.read()
        p.close()
        gpuinfoRoot=fromstring(xmlout)
        print('okk')
        self.gpuWidget=gpuTabWidget()
        self.performanceStack.add_titled(self.gpuWidget,'gpuStack','GPU')
        self.gpuName=gpuinfoRoot.find('gpu').find('product_name').text
        self.gpuWidget.gpuinfolabel.set_text(self.gpuName)
        self.totalvram=gpuinfoRoot.find('gpu').find('fb_memory_usage').find('total').text
        self.gpuWidget.gpuvramlabelvalue.set_text(self.totalvram)
        self.gpuWidget.gpudriverlabelvalue.set_text(gpuinfoRoot.find('driver_version').text)
        self.gpuWidget.gpucudalabelvalue.set_text(gpuinfoRoot.find('cuda_version').text)
        self.gpuWidget.gpumaxspeedlabelvalue.set_text(gpuinfoRoot.find('gpu').find('max_clocks').find('graphics_clock').text)
        self.gpuWidget.gpuvrammaxspeedlabelvalue.set_text(gpuinfoRoot.find('gpu').find('max_clocks').find('mem_clock').text)

        self.gpuWidget.givedata(self)
    except:
        print('no nvidia gpu found')
        self.isNvidiagpu=0

    
def gpuUpdate(self):
    p=popen('nvidia-smi -q -x')
    xmlout=p.read()
    p.close()
    gpuinfoRoot=fromstring(xmlout)
    self.vramused=gpuinfoRoot.find('gpu').find('fb_memory_usage').find('used').text
    self.gpuutil=gpuinfoRoot.find('gpu').find('utilization').find('gpu_util').text
    self.gpuWidget.gpuutilisationlabelvalue.set_text(self.gpuutil)
    self.gpuWidget.gpuvramusagelabelvalue.set_text(self.vramused[:-3]+'/'+self.totalvram)
    gpu_temp=gpuinfoRoot.find('gpu').find('temperature').find('gpu_temp').text
    if gpu_temp[-1]=='C':
        gpu_temp =gpu_temp[:-1]+'°C'
    self.gpuWidget.gputemplabelvalue.set_text(gpu_temp)
    self.gpuWidget.gpushaderspeedlabelvalue.set_text(gpuinfoRoot.find('gpu').find('clocks').find('graphics_clock').text)
    self.gpuWidget.gpuvramspeedlabelvalue.set_text(gpuinfoRoot.find('gpu').find('clocks').find('mem_clock').text)

    ############ int conv bug solve ###################### 
    gpu_enc=gpuinfoRoot.find('gpu').find('utilization').find('encoder_util').text
    if gpu_enc[-1]=='%':
        gpu_enc=int(gpu_enc[:-1])
    else:
        gpu_enc=0

    gpu_dec=gpuinfoRoot.find('gpu').find('utilization').find('decoder_util').text
    if gpu_dec[-1]=='%':
        gpu_dec=int(gpu_dec[:-1])
    else:
        gpu_dec=0

    if self.update_graph_direction:
        self.gpuUtilArray.pop(0)
        self.gpuUtilArray.append(int(self.gpuutil[:-1]))
        self.gpuVramArray.pop(0)
        self.gpuVramArray.append(int(gpuinfoRoot.find('gpu').find('fb_memory_usage').find('used').text[:-3]))
        self.gpuEncodingArray.pop(0)
        
        self.gpuEncodingArray.append(gpu_enc)
        self.gpuDecodingArray.pop(0)
        
        self.gpuDecodingArray.append(gpu_dec)
    else:
        self.gpuUtilArray.pop()
        self.gpuUtilArray.insert(0,int(self.gpuutil[:-1]))
        self.gpuVramArray.pop()
        self.gpuVramArray.insert(0,int(gpuinfoRoot.find('gpu').find('fb_memory_usage').find('used').text[:-3]))
        self.gpuEncodingArray.pop()
        self.gpuEncodingArray.insert(0,gpu_enc)
        self.gpuDecodingArray.pop()
        self.gpuDecodingArray.insert(0,gpu_dec)

    self.gpuWidget.givedata(self)