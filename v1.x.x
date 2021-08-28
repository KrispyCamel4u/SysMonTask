for i in range(0,self.numOfDisks):
        try:
            # Calclulating the difference between current and previous disk state
            diskDiff=[x2-x1 for x1,x2 in zip(self.diskstate1[i],self.diskstate2[i])]

            # Disk active(utilisation) percentage
            self.diskActiveString.append(f'{int(diskDiff[i][8]/(10*timediskDiff))}%')

            # Setting the info labels
            self.diskWidgetList[i].diskactivelabelvalue.set_text(self.diskActiveString[i])
            self.diskWidgetList[i].diskreadlabelvalue.set_text("{:.1f} MiB/s".format(diskDiff[i][2]/(timediskDiff*1048576)))
            self.diskWidgetList[i].diskwritelabelvalue.set_text("{:.1f} MiB/s".format(diskDiff[i][3]/(timediskDiff*1048576)))

            # updating the sample data holding array depending upon the direction 1: newer on right
            if self.update_graph_direction:
                self.diskActiveArray[i].pop(0)
                self.diskActiveArray[i].append((diskDiff[i][8])/(10*timediskDiff))##

                self.diskReadArray[i].pop(0)
                self.diskReadArray[i].append(diskDiff[i][2]/(timediskDiff*1048576))

                self.diskWriteArray[i].pop(0)
                self.diskWriteArray[i].append(diskDiff[i][3]/(timediskDiff*1048576))
            else:
                self.diskActiveArray[i].pop()
                self.diskActiveArray[i].insert(0,(diskDiff[i][8])/(10*timediskDiff))##

                self.diskReadArray[i].pop()
                self.diskReadArray[i].insert(0,diskDiff[i][2]/((timediskDiff)*1048576))

                self.diskWriteArray[i].pop()
                self.diskWriteArray[i].insert(0,diskDiff[i][3]/((timediskDiff)*1048576))

            # passing data to the disk tab widget class
            self.diskWidgetList[i].givedata(self,i)
        except Exception as e:
            print(f'error in  disk update: {e}')