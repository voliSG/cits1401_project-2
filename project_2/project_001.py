# Sean Peralta Garcia - 23088091


def main(csvfile):
    """
    docstring
    """
    country_data = {}
    continent_data = {}
    
    all_records, header_indices = extract_csv_data(csvfile)
    if all_records[0] == None:
        print(all_records[1])
        dict_country, dict_continent = None, None
        return dict_country, dict_continent
    
    for record in all_records:
        record = record.split(",")
        get_data("location", country_data, record, header_indices)
        get_data("continent", continent_data, record, header_indices)

        ''' dictionary schema after loop finishes running
            dict_country = {
                "country" : {"cases" : [[], [], [], [], [], [], [], [], [], [], [], []],

                             "deaths" : [[], [], [], [], [], [], [], [], [], [], [], []]
            }
        '''

    dict_country = process_data("country", country_data)
    dict_continent = process_data("continent", continent_data)
    return dict_country, dict_continent       
        

def extract_csv_data(csvfile):
    """
    docstring
    """
    try:
        # this is needed as open() method still creates a TextIOWrapper object when int or bool values are input
        # when the .read() method is called on this object, the python backend is terminated by thonny rather than raising an exception
        if type(csvfile) != type(""):
            raise TypeError
        
        with open(csvfile, 'r') as infile:
            all_records = infile.read().lower().split("\n")

        headers = all_records[0].split(",")
        # strip spaces from headers
        headers = [header.strip() for header in headers]
        
        valid_headers = ["continent", "location", "date", "new_cases", "new_deaths"]

        if not set(valid_headers).issubset(headers):
            missing_headers = [header for header in valid_headers if header not in headers]
            return [None,
                    f"\nError: the file does not contain the correct headers...\nHeaders missing: {missing_headers}...\nProgram Terminated"], None

    except FileNotFoundError:
        return [None,
                f"\nError: the file \"{csvfile}\" was not found... Program Terminated"], None
        
    except TypeError:
        return [None,
                f"\nError: csvfile input needs to be of string type, it is currently of type {type(csvfile)}... Program Terminated"], None
    
    except Exception:
        return [None,
                f"\nError: the file \"{csvfile}\" could not be opened... Program Terminated"], None
    
    else:
        header_indices = get_header_indices(headers, valid_headers)
        return all_records[1:-1], header_indices
    
    
def get_header_indices(headers, valid_headers):
    """
    docstring
    """
    indices = [headers.index(header) for header in valid_headers]
    return dict(zip(valid_headers, indices))
    

def get_data(criteria_filter, dict_data, record, header_indices):
    """
    docstring
    """
    # get name of country or continent, in order to sort
    criteria = record[header_indices[criteria_filter]].strip()
    
    # get month from record; check format and range
    try:
        date = record[header_indices["date"]].split("/")
        
        # will raise an IndexError if [day, month, year] not returned by .split()
        date = [int(date[i].strip()) for i in range(0,3)]

        # range check month (is month between 1 and 12 inclusive)
        if date[1] not in range(0, 13):
            raise Exception

    # if there is a problem with the format then return None, the next record will run
    except IndexError:
        return None
    except Exception:
        return None
    else:
        # subtract one for list index
        month = date[1] - 1
    
    # initialise if criteria (country/continent) is already in its respective dictionary
    if criteria not in dict_data:
        dict_data[criteria] = {"cases" : [[], [], [], [], [], [], [], [], [], [], [], []],

                               "deaths" : [[], [], [], [], [], [], [], [], [], [], [], []]}
        
    # type and range check new_cases
    try:
        if int(record[header_indices["new_cases"]]) >= 0:
            dict_data[criteria]["cases"][month].append(int(record[header_indices["new_cases"]]))
        else:
            dict_data[criteria]["cases"][month].append(0)
    except Exception:
        dict_data[criteria]["cases"][month].append(0)
    
    # type and range check new_deaths
    try:
        if int(record[header_indices["new_deaths"]]) >= 0:
            dict_data[criteria]["deaths"][month].append(int(record[header_indices["new_deaths"]]))
        else:
            dict_data[criteria]["deaths"][month].append(0)
    except Exception:
        dict_data[criteria]["deaths"][month].append(0)


def process_data(criteria_filter, dict_data):
    """
    docstring
    """
    # create dict that holds statistical data
    dict_return = {}
   
    # loop though dict keys and add them to dict_return??
    for item in dict_data:
        cases_data, cases_aboveAvg = process_month("cases", criteria_filter, item, dict_data)
        deaths_data, deaths_aboveAvg = process_month("deaths", criteria_filter, item, dict_data)
        
        dict_return[item] = [cases_data, deaths_data, cases_aboveAvg, deaths_aboveAvg]

    return dict_return


def process_month(data_type, criteria_filter, item, dict_data):
    """
    docstring
    """
    year_data = []
    year_aboveAvg = []
    
    for month in dict_data[item][data_type]:
        month_total = sum(month) 
        year_data.append(month_total)
        
        if criteria_filter == "country":
            
            # account for no data in month
            try:
                month_avg = month_total/len(month)
            except ZeroDivisionError:
                year_aboveAvg.append(0)
                return year_data, year_aboveAvg
                
        # if criteria_filter == "continent"
        else:
            month_avg = month_total/[31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][dict_data[item][data_type].index(month)]
        
        aboveAvg_count = 0
        for case in month:
            if case > month_avg:
                aboveAvg_count += 1

        year_aboveAvg.append(aboveAvg_count)
            
    
    return year_data, year_aboveAvg
    


if __name__ == "__main__":
    print(main("Covid-data-for-project-2-sample.csv"))
    #main("Covid-data-for-project-2-csv")
    #main("Covid-data-for-project-2-sample copy.csv")
    #main(True)
    
    
'''Outputs:
    * country dict
        - list containing total number of recorded positive cases of C19 for each month of the year
        - same as above but with deaths
        - list containing total no of days for each month of year
          when recorded positive cases is greater than average recorded positive cases of that month
        - list containing total no of days for each month of year
          when recorded deaths for that month is greater than average deaths for each month of the year
          
          (1+2 is one function)
          (3+4 is one function)
    
    * continent dict
        - same as above but account for all days in a month
    
   REQUIREMENTS:
    * all text converted to lowercase (can do that if using .read().lower())
    * averages are calculated only using days that have recorded data (COUNTRY OUTPUT ONLY)
    * assume data for all days of month exist for CONTINENT OUTPUT
        - i.e only 15 days have recorded cases... average is out of 15 days not 30
    * csvfile validation - cannot be found or opened
        - print message then return None
    * file data needs to be checked for validity
        - date must be in expected format else discard record
        - data is expected to be in the right type (else??)
            - any other recorded data(string where int expected)/no data is considered (0)
            - applies to negatives too
    * table headers are not in any specific order
    * if required headers are not included, terminate program

   Notes:
    * figure out required columns  
        - continent
        - location
        - date
        - new_cases
        - new_deaths
        
    # if country or continent is blank
    if criteria == "":
        return None
'''