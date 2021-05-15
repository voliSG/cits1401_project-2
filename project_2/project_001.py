# Sean Peralta Garcia - 23088091


def main(csvfile):
    """
    docstring
    """
    dict_country = {}
    dict_continent = {}
    
    all_records, header_indices = extract_csv_data(csvfile)
    if all_records[0] == None:
        print(all_records[1])
        dict_country, dict_continent = None, None
        return dict_country, dict_continent
    

    
    
    
    
    #dict_country, dict_continent = get_cases(all_records, dict_country, dict_continent)


def extract_csv_data(csvfile):
    """
    docstring
    """
    try:
        # this is needed as open() method still creates a TextIOWrapper object when int or bool values are input
        # when the .read() method is called on this object, the python backend is terminated by thonny rather than throwing an exception
        if type(csvfile) != type(""):
            raise TypeError
        
        with open(csvfile, 'r') as infile:
            all_records = infile.read().lower().split("\n")

        headers = all_records[0].split(",")
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


def convert_csv_data(all_records, header_indices):
    """
    docstring
    """
    pass
    


def get_cases(all_records, dict_country, dict_continent):
    """
    docstring
    """
    # this is used for...
    empty_year = {"01": [], "02": [], "03": [], "04": [],
                  "05": [], "06": [], "07": [], "08": [],
                  "09": [], "10": [], "11": [], "12": []}
    
    
    ## go through each record and append
    #dict_year = empty_year.copy()
    #for record in all_records:
    #    pass
    
    



if __name__ == "__main__":
    main("Covid-data-for-project-2-sample.csv")
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
            (are negative numbers required to be converted to 0????)
    * table headers are not in any specific order
    * if required headers are not included, terminate program

   Notes:
    * figure out required columns  
        - continent
        - location
        - date
        - new_cases
        - new_deaths
'''