"""
Creates a simple Gantt chart
Adapted from http://www.clowersresearch.com/main/gantt-charts-in-matplotlib/, which is based on https://bitbucket.org/DBrent/phd/src/1d1c5444d2ba2ee3918e0dfd5e886eaeeee49eec/visualisation/plot_gantt.py
"""
 
import pandas
import StringIO
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy
from matplotlib.backends.backend_pdf import PdfPages


class Gannt():
    def __init__(self):
        pass
    
    def clean(self,df):
        df.columns = df.columns.str.strip()
        for col in df:
            try:
                df[col] = df[col].str.strip()
            except:
                pass
        
        return df
    
    
    def convert_format(self,df,start_string,end_string):
        """Convert to gannt-ready format.
           Input df:
           
           time, event
           0,    RESTORE STARTED   X1
           0.5,    RESTORE STARTED   X3
           1,   RESTORE DONE  X1
           2,    RESTORE STARTED  X2
           2.5,   RESTORE DONE  X2
           3,   RESTORE DONE       X3

           output df:
           start, end, event
           0    , 1  , X1
           2    , 3  , X2

           args:
               df: the source df
               start_string: identifier for event start - RESTORE STARTED in the example above
               end_string: identifier for event end - RESTORE DONE in the example above
        """
        
        df = self.clean(df)
        df_restore_start = df[df.event.str.contains(start_string)]
        df_restore_end = df[df.event.str.contains(end_string)]
        
        df_restore_start.event = df_restore_start.copy().event.str.extract(start_string+"(.*)",expand=False).str.strip()
        df_restore_end.event = df_restore_end.copy().event.str.extract(end_string+"(.*)",expand=False).str.strip()
        
        assert(df_restore_start.isnull().sum().sum() == 0)
        assert(df_restore_end.isnull().sum().sum() == 0)
        
        
        df_restore_start.rename(columns={'time': 'start'}, inplace=True)
        df_restore_end.rename(columns={'time': 'end'}, inplace=True)
        
        df_restore_start = df_restore_start.set_index(df_restore_start.event)
        df_restore_end = df_restore_end.set_index(df_restore_end.event)
        
        merged_df = pandas.merge(df_restore_start,df_restore_end)
        
        if not (len(df_restore_start) == len(df_restore_end) == len(merged_df)):
            print "df_restore_start:"
            print df_restore_start
            print "df_restore_end:"
            print df_restore_end
            print "merged_df:"
            print merged_df
            raise(Exception("Cannot convert the format of the data frame."))
        merged_df.event = merged_df.copy().event.str.replace(':', '.').replace(" ","")
        return merged_df


    def draw_gannt(self,df,title,pdf=None,size=10):
        
        df = self.clean(df)
        for c in ["start","end","event"]:
            assert(c in df.columns)
        
        if not ("color" in df.columns):
            df["color"]="blue"
         
        # Initialise plot
         
        fig = plt.figure(figsize=(size, size))
        ax = fig.add_subplot(111)
        fig.suptitle(title, fontsize=20)
        
        # Plot the data
        for index, row in df.iterrows():
            start_date,end_date = row["start"], row["end"]
            color = row["color"].strip()
            duration = end_date - start_date
            ax.barh(index*0.5+0.5, duration, left=start_date, height=0.3, align='center', color=color, alpha = 0.75)
            
            annotation_x = start_date + 0.5*(end_date - start_date)
            ax.text(annotation_x, index*0.5+0.5+0.1, str(int(duration)), fontsize=15)
        
        # Format the y-axis
        y_labels_axis = numpy.arange(0.5,0.5*(len(df.event)+1),0.5)
        locsy, labelsy = plt.yticks(y_labels_axis,df.event)
        plt.setp(labelsy, fontsize = 14)
        
        # Format the x-axis
         
        ax.axis('tight')
        ax.set_ylim(ymin = -0.1, ymax = y_labels_axis.max()+0.5)
        ax.grid(color = 'g', linestyle = ':')
         
        labelsx = ax.get_xticklabels()
        plt.setp(labelsx, rotation=30, fontsize=12)
        
        #plt.figure(figsize=(12, 10))
         
        # Format the legend
         
        font = font_manager.FontProperties(size='small')
        ax.legend(loc=1,prop=font)
         
        # Finish up
        ax.invert_yaxis()
        fig.autofmt_xdate()
        #plt.savefig('gantt.svg')
        
        if pdf != None:
            pdf.savefig()
        #plt.close()
        plt.show()

def test():
        
    TABLE_FORMAT1 = """
    5,    TASK STARTED   Task 1
    6,    TASK ENDED Task 1
    6,    TASK STARTED   Task 2
    8,    TASK ENDED Task 2
    7,    TASK STARTED   Task 3
    9,    TASK ENDED Task 3
    0,    TASK STARTED   Task 4
    3,    TASK ENDED Task 4
    2,    TASK STARTED   Task 5
    6,    TASK ENDED Task 5
    5,    TASK STARTED   Task 6
    6,    TASK ENDED Task 6
    6,    TASK STARTED   Task 7
    7,    TASK ENDED Task 7
    4,    TASK STARTED   Task 8
    8,    TASK ENDED Task 8
    4,    TASK STARTED   Task 9
    9,    TASK ENDED Task 9
    4,    TASK STARTED   Task 10
    10,    TASK ENDED Task 10
    4,    TASK STARTED   Task 11
    11,    TASK ENDED Task 11
    4,    TASK STARTED   Task 12
    12,    TASK ENDED Task 12
    4,    TASK STARTED   Task 13
    13,    TASK ENDED Task 13
    5,    TASK STARTED   Task 14
    18,    TASK ENDED Task 14
    9,    TASK STARTED   Task 15
    17,    TASK ENDED Task 15
    """
    
    
    df1 = pandas.read_csv(StringIO.StringIO(TABLE_FORMAT1),header=None, names=["time", "event"])
    g = Gannt()
    df2 = g.convert_format(df1,start_string="TASK STARTED", end_string="TASK ENDED")
    
    TABLE_FORMAT2 = """
    start,   end, event,  color
    5,6, Task 1, blue
    6,8, Task 2, blue
    7,9, Task 3, blue
    0,3, Task 4, red
    2, 6, Task 5, red
    5, 6, Task 6, green
    6,7, Task 7, green
    4, 8, Task 8, green
    4, 9, Task 9 , green
    4, 10, Task 10, green
    4, 11, Task 11, green
    4, 12, Task 12, green
    4, 13, Task 13, green
    5, 18, Task 14, green
    9, 17, Task 15, green
    
    """
    
    df = pandas.read_csv(StringIO.StringIO(TABLE_FORMAT2))
    df = g.clean(df)
    #check the conversion first
    assert (True == (df.sort_index(axis=1).drop("color",axis=1).sort_values("event") == df2.sort_index(axis=1).sort_values("event") ).all().all())

test()

    
def example():    
    TABLE = """
    start,   end, event,  color
    5,6, Task 1, blue
    6,8, Task 2, blue
    7,9, Task 3, blue
    0,3, Task 4, red
    2, 6, Task 5, red
    5, 6, Task 6, green
    6,7, Task 7, green
    4, 8, Task 8, green
    4, 9, Task 9 , green
    4, 10, Task 10, green
    4, 11, Task 11, green
    4, 12, Task 12, green
    4, 13, Task 13, green
    5, 18, Task 14, green
    9, 17, Task 15, green
    
    """
    pdf = PdfPages("test3.pdf")
    df = pandas.read_csv(StringIO.StringIO(TABLE))
    g = Gannt()
    
    g.draw_gannt(df,"example1",pdf)
    g.draw_gannt(df,"example2",pdf)
    
    pdf.close()
