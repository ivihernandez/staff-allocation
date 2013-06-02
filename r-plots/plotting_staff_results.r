#results is one of the files obtained with the program "staff-allocation"
values <- results
values$forms <- values$throughput*3.2
values <- values[with(values, order(-resources,-forms)),]

#one file
myplot <- ggplot(values, aes(x=resources, y=forms, size=time)) 
myplot <- myplot + geom_point() + stat_smooth(legend=FALSE) 
myplot <- myplot + labs(size="Waiting Time (minutes)") + xlab("# of Staff") + ylab("Throughput (forms)")
myplot <- myplot + theme(axis.title.y = element_text( face='bold')) + theme(axis.title.x = element_text( face='bold'))
myplot <- myplot + theme_bw(18)
myplot <- myplot + theme(legend.position="top")


#multiple files (prescreened percentages) - continuous
myplot <- ggplot(values, aes(x=resources, y=forms, size=time)) 
myplot <- myplot + geom_point(aes(colour=prescreened)) 
myplot <- myplot + labs(size="Waiting Time (minutes)") + xlab("Staff Members") + ylab("Throughput (forms per hour)")
myplot <- myplot + labs(colour='Pre-screened (%)')
myplot <- myplot + theme(axis.title.y = element_text( face='bold')) + theme(axis.title.x = element_text( face='bold'))
myplot <- myplot + theme_bw(18)
myplot <- myplot + theme(legend.position="top")

#multiple files (prescreened percentages) - discrete
myplot <- ggplot(values, aes(x=resources, y=forms, size=time)) 
myplot <- myplot + geom_point(aes(colour=as.factor(prescreened))) 
myplot <- myplot + labs(size="Waiting Time (minutes)") + xlab("Staff Members") + ylab("Throughput (forms per hour)")
myplot <- myplot + labs(colour='Pre-screened (%)')
myplot <- myplot + theme(axis.title.y = element_text( face='bold')) + theme(axis.title.x = element_text( face='bold'))
myplot <- myplot + theme_bw(18)
myplot <- myplot + theme(legend.position="top")