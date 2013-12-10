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
myplot


#multiple files (prescreened percentages) - continuous
myplot <- ggplot(values, aes(x=resources, y=forms, size=time)) 
myplot <- myplot + geom_point(aes(colour=prescreened)) 
myplot <- myplot + labs(size="Waiting Time (minutes)") + xlab("Staff Members") + ylab("Throughput (forms per hour)")
myplot <- myplot + labs(colour='Pre-screened (%)')
myplot <- myplot + theme(axis.title.y = element_text( face='bold')) + theme(axis.title.x = element_text( face='bold'))
myplot <- myplot + theme_bw(18)
myplot <- myplot + theme(legend.position="top")
myplot

#multiple files (prescreened percentages) - discrete
# myplot <- ggplot(values, aes(x=resources, y=forms, size=time)) 
# myplot <- myplot + geom_point(aes(colour=as.factor(prescreened))) 
# myplot <- myplot + labs(size="Waiting Time (minutes)") + xlab("Staff Members") + ylab("Throughput (forms per hour)")
# myplot <- myplot + labs(colour='Pre-screened (%)')
# myplot <- myplot + theme(axis.title.y = element_text( face='bold')) + theme(axis.title.x = element_text( face='bold'))
# myplot <- myplot + theme_bw(18)
# myplot <- myplot + theme(legend.position="top")
# myplot

#staff vs throughopu, faceting by prescreened
myplot <- ggplot(data=values) + geom_point(aes(x=resources, y=forms, size=time))
myplot <- myplot + geom_line(aes(x=resources, y=forms))
myplot <- myplot + facet_wrap(~prescreened)
myplot <- myplot + labs(size="Waiting Time (minutes)") + xlab("Staff Members") + ylab("Throughput (forms per hour)")
myplot <- myplot + theme(axis.title.y = element_text( face='bold')) + theme(axis.title.x = element_text( face='bold'))
myplot <- myplot + theme_bw(18)
myplot <- myplot + theme(legend.position="top")
myplot

#barplot staff
melted <- melt(values, id=c('resources','throughput','time','prescreened','forms'))
myplot <- ggplot(data=melted) + geom_bar(stat='identity',aes(x=variable, y=value))
myplot <- myplot + xlab("Staff Type") + ylab("Number")
myplot <- myplot + theme(axis.title.y = element_text( face='bold')) + theme(axis.title.x = element_text( face='bold'))
myplot <- myplot + theme_bw(18)
myplot

#barplot staff, stratified by prescreened
melted <- melt(values, id=c('resources','throughput','time','prescreened','forms'))
myplot <- ggplot(data=melted) + geom_bar(stat='identity',aes(x=variable, y=value))
myplot <- myplot + xlab("Staff Type") + ylab("Number")
myplot <- myplot + theme(axis.title.y = element_text( face='bold')) + theme(axis.title.x = element_text( face='bold'))
myplot <- myplot + theme_bw(18)
myplot <- myplot + facet_wrap(~prescreened) + theme(axis.text.x=element_text(angle=90))
myplot

#dot plots, stratified by staff type
# myplot <- ggplot(data=melted) + geom_point(aes(x=variable, y=value))
# myplot <- myplot + xlab("Staff Type") + ylab("Number")
# myplot <- myplot + theme(axis.title.y = element_text( face='bold')) + theme(axis.title.x = element_text( face='bold'))
# myplot <- myplot + theme_bw(18)
# myplot <- myplot + facet_wrap(~prescreened) + theme(axis.text.x=element_text(angle=90))
# myplot

