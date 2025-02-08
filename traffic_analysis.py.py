# Task A: Input Validation
def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
    # Validation logic goes here
    
    # Step 1: Initialized a dictionary called days_dict to validate the day which
    # user entered is included in the month or not.
    # I used the key as the number of the month and the value as the number of
    # maximum days included in that month.
    days_dict = {
        1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }

    # Step 2: Validated the day. I used infinite while loops to validate the
    # day,month and year.
    while True:
        day = input("Please enter the day of the survey in the format dd: ").replace(" ","")
        #replace() function removes all the unnecessary white spaces entered
        #by the user.
        try:
            if day != "": # Checks whether user inputs a value
                day = int(day)# Checks whether the user inputs an integer as the day.
            else:
                continue
        except: 
            print("Integer required") 
        
        else:
            if (1<=day<=31):
                # Checks whether the day user inputs is included in
                # the range of 1 and 31.
                break
            else:
                print("Out of range - values must be in the range 1 and 31.")

    
    # Step 3: Validate the month.
    while True:
        month = input("Please enter the month of the survey in the format mm: ").replace(" ","")
        try:
            if month != "":
                month = int(month)
            else:
                continue
        except:
            print("Integer required")
        
        else:

            if (1<=month<=12):
                if int(day) > days_dict[month]:
                    # Here I checked whether the day user gave is included in that month.
                    # I used the days_dict dictionary which I initialized in the
                    # beginning to do that.
                    
                    print("The day is not included in the month. Try another date.")
                    # If the day is not included in that month
                    # run the function again and get the day.
                    # So it becomes recursive function

                    return validate_date_input()
                    
                break

            
            else:
                print("Out of range - values must be in the range 1 and 12.")

    #Step 4: Validate the year
    while True:
        year = input("Please enter the year of the survey in the format yyyy: ").replace(" ","")
        try:
            if year != "":
                year = int(year)
            else:
                continue
        except:
            print("Integer required")
        
        else:
            #First I checked whether the year user gave is a leap year or not.
            is_leap = False #initialized a variable is_leap and set it into False.
            
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                # If condition checks whether the year is leap or not.
                is_leap = True
        
            if (2000<=year<=2024):
                #Checks whether the year is inside the given range of 2000 of 2024.
                
                #If the user has not entered a leap year but entered the
                #month as February and day as 29,
                #the code inside the if block is executed.

                if (is_leap == False) and (int(month) == 2) and (int(day) == 29):
                    days_dict[2] = 28
                    #sets the value of month february in the dictionary equal to 28.
                    print("This year is not a leap year. Enter a new date")

                    #Executes the function from the begin and ask the user for a new date
                    return validate_date_input()
                    
                break

            else:
                print("Out of range - values must be in the range 2000 and 2024.")
            

    #Step 5: Formatting the file and date strings including day,month and year.
    file =f"csvfiles/traffic_data{day:02d}{month:02d}{year}.csv"
    date = f"{day:02d}{month:02d}{year}"
    #:02d displays the day in 2 decimal integers.

    #Made a list including file and date because the date is useful for task D.
    file_lst = [file,date]
    return file_lst #returned the list

def validate_continue_input():
    """
    #Prompts the user to decide whether to load another dataset:
    #- Validates "Y" or "N" input
    """
    # Validation logic goes here
    while True:
        user_input = input("Do you want to select another data file for a different date? Y/N ").replace(" ","")
        if user_input.upper() == "Y":
            
            # This function executes the requirements only for task A,B,C.
            main_a_b_c()

        elif user_input.upper() == "N":
            print("End of run")
            break
        else:
            print("Please enter “Y” or “N”")
            continue
            

# Task B: Processed Outcomes
def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    # Logic for processing data goes here
    import csv
    try:

        #Opened the file and saved the file object as file_obj.
        file_obj = open(file=file_path)

        file_reader = csv.DictReader(file_obj)
        #Reads the file line by line and converts each row to a dictionary,
        #ignoring the 1st row which is the header.
        #file_reader object is a sequence of dictionaries.
    
    except FileNotFoundError:
        #If the file is not available, this except block handles
        #the FileNotFound error.
        
        print("File not found. Enter a new date")

        # This function executes the requirements only for task A,B,C.
        main_a_b_c()

    else:
        #Initialized all the parameters they are asking in task B to 0.
        
        #Total number of vehicles
        vehicle_count = 0
        #Total number of trucks
        truck_count = 0
        #Total number of electric vehicles
        electric_count = 0
        #Total number of two wheeled vehicles
        two_wheeled_count = 0
        #The total number of Busses leaving Elm Avenue/Rabbit Road heading North.
        total_buss_north = 0
        # Total number of bikes
        bicycle_count = 0
        #Total number of Vehicles recorded as over the speed limit.
        speed_limit_exc = 0
        #Total number of vehicles recorded through Elm Avenue/Rabbit Road junction.
        elm_rbt = 0
        #Total number of vehicles recorded through Hanley Highway/Westway junction
        hanley_west = 0
        #Total number of scooters recorded through Elm Avenue/Rabbit Road junction.
        elm_rbt_sct = 0
        #The total number of Vehicles through both junctions not turning left or right
        straight_count = 0
        #Total number of hours of rain.
        total_rain_hours = 0
        
        #Initialized 2 empty dictionaries for both junctions to get the hour count.
        #Here key is the hour and value is the number of vehicles in each hour.
        hour_count_han = {} 
        hour_count_elm = {} #This dictionary is useful for task D.

        #Initialized an empty set to get the total number of rain hours.
        rain_set = set()


        #Iterated through each row and updated the parameters that I initialized first.
        for row in file_reader:
            vehicle_count += 1
            if row["elctricHybrid"] == "True":
                electric_count += 1
            if row["VehicleType"] == "Truck":
                truck_count += 1
            
            if (row["VehicleType"] == "Bicycle") or (row["VehicleType"] == "Motorcycle") or (row["VehicleType"] == "Scooter"):
                two_wheeled_count += 1
            if (row["JunctionName"] == "Elm Avenue/Rabbit Road") and (row["travel_Direction_out"] == "N") and (row["VehicleType"] == "Buss"):
                total_buss_north += 1
            if row["VehicleType"] == "Bicycle":
                bicycle_count += 1
            if float(row["VehicleSpeed"]) > float(row["JunctionSpeedLimit"]):
                speed_limit_exc += 1
            if row["JunctionName"] == "Elm Avenue/Rabbit Road":
                elm_rbt += 1
            if row["JunctionName"] == "Hanley Highway/Westway":
                hanley_west += 1
            if (row["JunctionName"] == "Elm Avenue/Rabbit Road") and (row["VehicleType"] == "Scooter"):
                elm_rbt_sct += 1
            

            if row["JunctionName"] == "Hanley Highway/Westway":
                
                #Got the index of the : using find() function
                index = row["timeOfDay"].replace(" ","").find(":") 
                hour = row["timeOfDay"][:index] # Sliced the string until that index and got the hour.

                if hour not in hour_count_han:
                    hour_count_han[hour] = 1
                else:
                    hour_count_han[hour] += 1
            
                # Used the max() function to get the hour with maximum value
                max_hour_begin = max(hour_count_han, key=hour_count_han.get)
                max_hour_end = int(max_hour_begin) + 1

                # Got the number of vehicles that passed in the maximum hour
                vehicles_in_max_hour = hour_count_han[max_hour_begin]

            # Made the dictionary for Elm Avenue. It is useful for Task D.
            if row["JunctionName"] == "Elm Avenue/Rabbit Road":
                index = row["timeOfDay"].replace(" ","").find(":")
                hour = row["timeOfDay"][:index]

                if hour not in hour_count_elm:
                    hour_count_elm[hour] = 1
                else:
                    hour_count_elm[hour] += 1
            
            if row["travel_Direction_in"] == row["travel_Direction_out"]:
                straight_count += 1

            if "RAIN" in row["Weather_Conditions"].upper():

                #Got the last index position of the hour part of the time string.              
                index_hour = row["timeOfDay"].replace(" ","").find(":")

                #Filtered the hour and converted it to an integer
                hour = int(row["timeOfDay"][:index_hour])
                rain_set.add(hour)#Added the hour to the set.
        
        
        #Got the percentage of trucks and rounded it to the nearest integer.
        truck_pct = (truck_count/vehicle_count)*100
        truck_pct_rnd = round(truck_pct)
        
        #Got the average number of bikes per hour and rounded it to the nearest integer.
        avg_bicycle = bicycle_count/24
        avg_bicycle_rnd  = round(avg_bicycle)

        #Got the percentage of scooters recorded through Elm Avenue/Rabbit Road.
        elm_sct_pct = (elm_rbt_sct/elm_rbt)*100
        elm_sct_pct_rnd = int(elm_sct_pct)

        #Found the index of traffic word and assigned it to index_file variable.
        index_file = file_path.find("traffic")
        #Then sliced the string from that index when displaying the out_string.

        #Total rain hours is equal to the length of the set.
        total_rain_hours = len(rain_set)

        #Formatted the output string.
        out_string = f"""
***************************
data file selected is {file_path[index_file:]}
***************************
The total number of vehicles recorded for this date is {vehicle_count}
The total number of trucks recorded for this date is {truck_count}
The total number of electric vehicles for this date is {electric_count}
The total number of two-wheeled vehicles for this date is {two_wheeled_count}
The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {total_buss_north}
The total number of Vehicles through both junctions not turning left or right is {straight_count}
The percentage of total vehicles recorded that are trucks for this date is {truck_pct_rnd}%
the average number of Bikes per hour for this date is {avg_bicycle_rnd}


The total number of Vehicles recorded as over the speed limit for this date is {speed_limit_exc}
The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {elm_rbt} 
The total number of vehicles recorded through Hanley Highway/Westway junction is {hanley_west}
{elm_sct_pct_rnd}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.

The highest number of vehicles in an hour on Hanley Highway/Westway is {vehicles_in_max_hour}
The most vehicles through Hanley Highway/Westway were recorded between {max_hour_begin}:00 and {max_hour_end:02d}:00
The number of hours of rain for this date is {total_rain_hours}
"""
        #hour_count_han and hour_count_elm dictionaries are useful for task D.
        #I put the 2 dictionaries and the string to a single list and assigned that
        #list into a variable called outcomes.
        outcomes = [out_string,hour_count_han,hour_count_elm]
        
        file_obj.close() #Closed the file_obj object.
        return outcomes #returned the list.

def display_outcomes(outcomes): 
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    out_string = outcomes[0]#Accessed the formatted string from the outcomes list and printed it.
    print(out_string)

# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    # File writing logic goes here

    with open(file_name, 'a') as newfile:
        #Opened a file called results.txt in append mode and assigned the file object
        #to a variable called newfile.
        newfile.write(outcomes[0])#Appended the string to results.txt file using write() method.
        
    print("Data has been written to 'results.txt'.")


def main_a_b_c():
    # This function executes the requirements only for task A,B,C.
    # After calling this function it executes all the functions used
    # in task A,B,C that is given in the template.
    
    import sys

    file_lst = validate_date_input()
    outcomes = process_csv_data(file_lst[0])
    display_outcomes(outcomes)
    save_results_to_file(outcomes,"results.txt")
    validate_continue_input()
    sys.exit() #This method in sys library terminates the program smoothly.


# Task D: Histogram Display

# Imported evey class in graphics module
from graphics import *  

class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data 
        self.date = date
        self.win = None # This initializes the window for the histogram

        # Specifications of the window and x axis.
        self.width = 1000 # Width of the window
        self.height = 600 # Height of the window
        self.x_offset = 50 # Left and right margins
        self.y_offset = 50 # Bottom margin

        # Distance to 0 from the left corner of the x axis.
        # This is same to the distance to 23 from the right corner of the x axis.
        self.x_value_margin = 20 

        # Width of the histogram.
        self.chart_width = self.width - 2 * self.x_offset

        # Height of the histogram.
        self.chart_height = self.height - 2 * self.y_offset

        # Horizontal distance between 2 consecutive values of the x axis.
        self.x_value_interval = (self.chart_width - (self.x_value_margin * 2))/23

        # Horizontal distance to 0 from the border of the GUI window.
        self.x_zero_distance = self.x_offset + self.x_value_margin

        # Vertical distance between the x axis line and the values.
        self.x_axis_value_distance = 10 

        # Specifications of the rectangles(bars)
        # Horizontal distance of the empty space between 2 bars.
        self.bar_spacing = 10

        # Width of a bar.
        self.rect_width = (self.x_value_interval - self.bar_spacing)/2

        # Horizontal distance between 2 bottom left corner points of the green bars.
        self.green_bottom_interval = (self.rect_width * 2) + self.bar_spacing

        # Maximum value in the values of combined_dict
        # dictionary that is used to normalize the length of bars.
        self.max = None

        # Specifications of the colour boxes in the top left corner.
        # Length of the colour box.
        self.squarelength = 15

        # Vertical distance of the space between 2 colour boxes.
        self.space = 10 

        # Colours of the bars
        # Colour of the bar of elm junction.
        self.bar_elm_col = "light green"

        # Colour of the bar of hanley junction.
        # This is the colour code for light red.
        self.bar_han_col = "#FF4D4D" 
        
        

    def setup_window(self):
        """
        Sets up the Graphics.py window and canvas for the histogram.
        """
        # Setup logic for the window
        self.win = GraphWin("Histogram", self.width, self.height) #I set the GUI window.
        self.win.setCoords(0, 0, self.width, self.height)  # I set a coordinate system.

    def draw_histogram(self):
        """
        Draws the histogram using the graphics.py library.
        """
        # Drawing logic goes here
        
        # Found the maximum value in the dataset to normalize the length of bars.
        # First, I initialized the maximum value to 0
        max_value = 0

        # Iterated through each value in the dictionary and found the maximum value.
        for values in self.traffic_data.values():
            current_max = max(values)
            if current_max > max_value:
                max_value = current_max
                
        self.max = max_value
        
        # Drew x-axis
        x_axis = Line(Point(self.x_offset, self.y_offset), Point(self.width - self.x_offset, self.y_offset))
        x_axis.setWidth(2)
        x_axis.draw(self.win)

        # Drew bars and labels.
        
        # Looped through the dictionary with index equal to 'i', key equal to 'hour', and value equal to 'values'
        for i, (hour, values) in enumerate(self.traffic_data.items()):
            # 'enumerate()' adds an index to each item in the dictionary's key-value pairs.
            # So I can access the index, keys and values in the value list.
            
            # Added hour labels below the bars.
            label = Text(Point(self.x_zero_distance + (i * self.x_value_interval), self.y_offset - self.x_axis_value_distance), hour)
            label.setSize(8)
            label.draw(self.win)

            # Calculated normalized heights for the bars.
            height_red = (values[0] / max_value) * self.chart_height
            height_green = (values[1] / max_value) * self.chart_height
            
            # Calculated x coordinates of bottom left, bottom middle and upper right points of rectangular bars.
            # For red bars.
            x_red_bottom_left = self.rect_width + self.x_offset + (self.green_bottom_interval * i)
            x_red_bottom_right = x_red_bottom_left + self.rect_width
            x_red_mid = (x_red_bottom_right + x_red_bottom_left)/2

            #For green bars.
            x_green_bottom_left = x_red_bottom_left - self.rect_width
            x_green_bottom_right = x_red_bottom_left
            x_green_mid = (x_green_bottom_right + x_green_bottom_left)/2

            # Drew green bars.
            bar1 = Rectangle(Point(x_green_bottom_left, self.y_offset), Point(x_green_bottom_right, self.y_offset + height_green))
            bar1.setFill(self.bar_elm_col)
            bar1.draw(self.win)

            # Added value labels on top of each bar.
            green_value = Text(Point(x_green_mid, self.y_offset + height_green + 10), str(values[1]))
            green_value.setSize(8)
            green_value.draw(self.win)

            # Drew red bars.
            bar2 = Rectangle(Point(x_red_bottom_left, self.y_offset), Point(x_red_bottom_right, self.y_offset + height_red))
            bar2.setFill(self.bar_han_col)
            bar2.draw(self.win)

            # Added value labels on top of each bar.
            red_value = Text(Point((x_red_mid), self.y_offset + height_red + 10), str(values[0]))
            red_value.setSize(8)
            red_value.draw(self.win)

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        # Logic for adding a legend

        # Calculated the x and y coordinates of red and green boxes in top left corner.
        # For red box.
        x_red_sq_bottom_left = self.x_offset
        y_red_sq_bottom_left = self.y_offset + 450
        x_red_sq_top_right = x_red_sq_bottom_left + self.squarelength
        y_red_sq_top_right = y_red_sq_bottom_left + self.squarelength

        # For green box.
        x_green_sq_bottom_left = self.x_offset
        y_green_sq_bottom_left = y_red_sq_top_right + self.space
        x_green_sq_top_right = x_green_sq_bottom_left + self.squarelength
        y_green_sq_top_right = y_green_sq_bottom_left + self.squarelength

        # Calculated the x and y coordinates of texts mentioned from
        # red and green boxes.
        # For text mentioned from red box.
        x_red_name = x_red_sq_top_right + 80
        y_red_name = y_red_sq_top_right - (self.squarelength/2)

        #For text mentioned from green box.
        x_green_name = x_green_sq_top_right + 80
        y_green_name = y_green_sq_top_right - (self.squarelength/2)
        
        
        # Drawed the green box.
        legend_green = Rectangle(Point(x_green_sq_bottom_left,y_green_sq_bottom_left), Point(x_green_sq_top_right,y_green_sq_top_right))
        legend_green.setFill(self.bar_elm_col)
        legend_green.draw(self.win)

        # Added the label of green box.
        legend_green_label = Text(Point(x_green_name,y_green_name), "Elm Avenue/Rabbit Road")
        legend_green_label.setSize(10)
        legend_green_label.draw(self.win)

        # Drawed the red box.
        legend_red = Rectangle(Point(x_red_sq_bottom_left, y_red_sq_bottom_left), Point(x_red_sq_top_right, y_red_sq_top_right))
        legend_red.setFill(self.bar_han_col)
        legend_red.draw(self.win)

        # Added the label of the red box.
        legend_red_label = Text(Point(x_red_name, y_red_name), "Hanley Highway/Westway")
        legend_red_label.setSize(10)
        legend_red_label.draw(self.win)

        # Added the title.
        # Calculated the coordinates.
        x_title = self.x_offset + 238
        y_title = self.height - 20

        #Added the text.
        day = self.date[0:2]
        month = self.date[2:4]
        year  = self.date[4:8]
        title = Text(Point(x_title,y_title), f"Histogram of Vehicle Frequency per Hour ({day}/{month}/{year})")
        title.setSize(15)
        title.draw(self.win)

        # Added the name of the x_axis.
        # Calculated the coordinates.
        x_x_axis_name = (self.chart_width/2) + self.x_offset
        y_x_axis_name = self.y_offset/2

        #Added the text.
        x_name = Text(Point(x_x_axis_name,y_x_axis_name), "Hours 00:00 to 24:00")
        x_name.setSize(10)
        x_name.draw(self.win)

    def run(self):
        """
        Runs the program to display the histogram.
        """
        # Called to the above methods to draw the histogram.
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        
        # If the user wants to annalyse the differences between multiple datasets,
        # the user has to get multiple histograms for different datasets simultanously.

        # To do that I made a new object of MultiCSVProcessor class.
        newprocessor = MultiCSVProcessor()

        # Called process_files() method in MultiCSVProcessor class
        # to prompt the user to enter a new date to get a new dataset.
        # This method prompts the user to enter a new date while the
        # current histogram is open.
        newprocessor.process_files()
        
        while True:
            try:
                # Wait for a mouse click and returns an object made of Point class
                # which includes the coordinates of the clicked point.
                # When the user clicks the red cross in the GUI it raises an error.
                self.win.getMouse()
                
            except:
                break

# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.date = None
        self.file = None
        self.histogram = None
        self.current_data = None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        # File loading and data extraction logic

        # First I loaded,annalysed, displayed and saved the results to
        # results.txt file by calling to the respective functions.

        ret = process_csv_data(file_path)
        # ret is a list.
        # ret[0] contains the formatted string.
        # ret[1] and ret[2] containe dictionaries which the key represents the hour and
        # the value represents the number of vehicles passed through that hour in
        # hanley and elm junctions respectively.
        
        display_outcomes(ret)
        save_results_to_file(ret,"results.txt")

        # Assigned the 2 dictionaries for 2 different variables.
        han_hour = ret[1]
        elm_hour = ret[2]

        # Made a combined dictionary which the key represents the hour
        # and each value is a list with 2 items.
        # The items are the number of vehicles passed through that hour
        # in hanley and elm junctions respectively.
        combined_dict = {}

        # Got the union of the keys of both dictionaries and built a set.
        # So that each key is unique.
        all_keys = set(han_hour.keys()).union(set(elm_hour.keys()))

        for key in all_keys:
            # Got the value from ret[1] dictionary, defaulting to 0 if the key is not present.
            val1 = han_hour.get(key, 0)
            # Got the value from ret[2] dictionary, defaulting to 0 if the key is not present.
            val2 = elm_hour.get(key, 0)
            
            # Added the combined values to the combined_dict dictionary.
            combined_dict[key] = [val1, val2]

        # Sorted the dictionary by its keys and returned a new dictionary.
        sorted_dict = {}
        for key in sorted(combined_dict):
            # Sorted(combined_dict) sorts the dictionary by its keys and returns
            # a list of sorted keys.

            sorted_dict[key] = combined_dict[key]

        combined_dict = sorted_dict

        # This dictionary is the dataset used to make the histogram.
        return combined_dict

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        # Logic for clearing data

        self.current_data = None

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        # Logic for user interaction
        # The entire flow of the program goes here.
        
        while True:
            # First I validated the date by calling to the
            # validate_date_input() function.
            file_lst = validate_date_input()
            
            # Seperated the file and date.
            self.date = file_lst[1]
            self.file = file_lst[0]
            
            try:
                #Checked whether the file is available.
                open(file=self.file)
                break
        
            except FileNotFoundError:
            #If the file is not available, this except block handles
            #the FileNotFound error.
                print("File not found. Enter a new date")

        # Cleared previous data.
        self.clear_previous_data()

        # Got the dataset which is used to make the histogram by
        # calling the load_csv_file() method.
        self.current_data = self.load_csv_file(self.file)

        # Passed the dataset and the date as parameters of the HistogramApp
        # class and made a object using that class.
        self.histogram = HistogramApp(self.current_data,self.date)

        # Called the run() method in that class to draw the histogram and
        # prompt the user for another dataset.
        self.histogram.run()

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        # Loop logic for handling multiple files
        
        while True:
            user_input = input("Do you want to select another data file for a different date? Y/N ").replace(" ","")

            if user_input.upper() == "Y":
                # Called the hande_user_interaction() method to draw the histogram for
                # another dataset.
                self.handle_user_interaction()
                break
                
            elif user_input.upper() == "N":
                print("End of run")
                break
            else:
                print("Please enter “Y” or “N”")
                continue

if __name__ == "__main__":
    #__name__ is a special built in variable in python. If the script runs directly
    #__name__ is set to "__main__"
    #If the script is imported as a module __name__ is set to the file name.
    #If the program runs directly it has to execute the body below.

    # Made a object using MultiCSVProcessor class and assigned
    # it to the variable called processor.
    processor = MultiCSVProcessor()

    # Called the handle_user_interaction() method in that class.
    processor.handle_user_interaction()
                
