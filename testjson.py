import json

class testjson():

  def execute(self):
    # Open the JSON file
    with open('data.json') as f:
      # Load the JSON data into a Python dictionary
      data = json.load(f)
    # Access the data
    print(data)

    # List of dates to filter for
    dates_to_print = ["2024-12-04", "2024-12-05", "2024-12-06"]
    
    # Parse the JSON string into a Python dictionary
    # data = json.loads(json_string)

    # Accessing the calendar data
    calendar = data['data']['calendar']

    for date, details in calendar.items():
      if date in dates_to_print:
        if details['sale_status'] != 2:
          print("hi")
        elif details['open_status'] != 1: 
          print("hqqi")

        print(f"Date: {date}")
        print(f"  Apply Type: {details['apply_type']}")
        print(f"  Sale Status: {details['sale_status']}")
        print(f"  Open Status: {details['open_status']}")
        print(f"  Holiday: {details['holiday']}")
        print(f"  Day Label: {details['day_label']}")
        print(f"  Temporary Closure: {details['is_temporary_closure']}")
        print(f"  Temporary Closure Time: {details['temporary_closure_time']}")
        print(f"  Holding: {details['is_holding']}")
        print("-" * 40)

        
if __name__== "__main__":
  taskMaster =  testjson()
  taskMaster.execute()