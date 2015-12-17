# PLOTS RESULTS FROM COMMITTED MINORITY SIMULATOR
# AUTHOR: Devon Brackbill
# 2015.08.28

library(ggplot2)
library(dplyr)
library(grid)
options(dplyr.print_max = 1e9)

# READ IN ALL .csv FILES IN DIRECTORY
file.names = list.files()
file.nums = grep('*csv', file.names)
file.names = file.names[file.nums]
results.df = do.call(rbind, lapply(paste0(file.names), read.csv))

results.df %>%
  group_by(popSize, prop_CM, maxMemory) %>%
  summarize(n=n())

############################################
# PLOT JUST THE NON-COMMITTED PROPORTION
############################################

png(file='Results.png',
    type = 'cairo', units = 'in',
    width = 5,  height = 5,  pointsize = 1,  res =200)

results.df$prop_CM = as.numeric(as.character(results.df$prop_CM))
results.df$proportionA_NoCM = 
  (results.df$proportionA -results.df$prop_CM ) / (1 - results.df$prop_CM)

ggplot(results.df, aes(x=prop_CM, y = proportionA_NoCM))+
  theme_bw()+
  facet_grid(.~popSize)+
  ylab('Proportion of Non-Committed Population\nAdopting New Norm at End\n')+
  xlab('\n Proportion of Population Initially Committed to New Norm')+
  theme(axis.title.y = element_text(size = 10),
        axis.title.x = element_text(size = 10),
        axis.text.x = element_text(size=10,angle = 0, vjust = 0),
        axis.text.y = element_text(size = 10),
        strip.text.y = element_text(size = 10),
        panel.grid.minor = element_blank(),
        plot.margin = unit(c(1,1,1,1), "cm")
        )+
  stat_summary(fun.y=median, colour="red", geom="point", 
               shape=18, size=3,show_guide = FALSE)+
  stat_summary(fun.y=median, colour="red", geom="line",
               size=.5,show_guide = FALSE)+
  scale_x_continuous(breaks = c(0.05, .1, .15, .2, .25, .3))+
  scale_y_continuous(breaks = c(0, 0.25, .5, 0.75, 1),
                     labels = c('0', '0.25', '.5', '0.75', '1'))+
  coord_cartesian(y=c(-.05,1.05),x=c(0.05,.16))
dev.off()
