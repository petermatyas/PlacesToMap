import requests
import os


class GeolocatorFileDb():
    def __init__(self, eol='\n', outFileDelimiter=';'):
        self.eol = eol
        self.outFileDelimiter = outFileDelimiter
        self.directory = "geolocator"
        self.saveFilePath = f'./{self.directory}/geolocation_saved.csv'

        self.notFoundFilePath = f'./{self.directory}/not_found.txt'

        self.__createFolderIfNotExist(self.directory)
        self.saved_dict = self.__getSavedDict()
        self.not_found_list = self.__getNotFoundList()

        

    def __createFolderIfNotExist(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def __getSavedDict(self):
        saved_dict = dict()
        url = self.saveFilePath
        if os.path.exists(url):
            with open(url, 'r+', encoding="utf-8") as f:
                lines = f.readlines()
                for i in lines:
                    i = i.strip()
                    i = i.replace(',','')
                    i = i.split(self.outFileDelimiter)
                    saved_dict[i[0]] = (i[1],i[2])
        else:
            saved_dict = []
        return saved_dict

    def __getNotFoundList(self):
        url = self.notFoundFilePath
        if os.path.exists(url):
            with open(url, 'r+', encoding="utf-8") as f:
                lines = f.readlines()
            return [i.strip() for i in lines]
        else:
            return []

    def saveRecord(self, query:str, lat, lon):
        url = self.saveFilePath
        with open(url, 'a', encoding="utf-8") as f:
            f.write(query.lower()+self.outFileDelimiter+str(lat)+self.outFileDelimiter+str(lon)+self.eol)
    
    def saveNotFound(self, query:str):
        url = self.notFoundFilePath
        with open(url, 'a', encoding="utf-8") as f:
            f.write(query.lower()+self.eol)
    
    def isSaved(self, query:str):
        if query.lower() in self.saved_dict:
            return self.saved_dict[query]
        else:
            return None

    def isNotFound(self, query:str):
        if query.lower() in self.not_found_list:
            return True
        else:
            return False

class Geolocator(GeolocatorFileDb):
    def __init__(self, maxQuery=3):
        super().__init__()
        self.maxQuery = maxQuery

        self.__actualQueryNr = 0
        self.__originalQuery = ""
        self.__actualQuery = ""

    def reduceQuery(self):       
        delimiter = ' '
        if self.__actualQuery == "":
            return False
        else:
            if self.__actualQuery.count(delimiter) > 0:
                self.__actualQuery = ' '.join(self.__actualQuery.split(' ')[:-1])
            
    def nominatim(self, query, verbose=True):
        res = requests.get(f'https://nominatim.openstreetmap.org/search?format=json&limit=1&q={query}').json()
        if verbose:
            print(f'[geocoding] {query}' , 40*' ', end='\r')
        return res    

    def geocode(self, query:str, verbose=True):
        self.__originalQuery = query
        self.__actualQuery = query.lower().replace(',', '')

        cache = self.isSaved(self.__actualQuery)

        if self.__actualQuery != self.__actualQuery:  # res == Nan
            raise Exception("query is Nan")
        elif cache:
            return cache        
        elif self.isNotFound(self.__actualQuery):
            return (None, None)
        else:
            res = self.nominatim(self.__actualQuery, verbose)
            self.__actualQueryNr += 1
            while 'lat' in res and 'lon' in res and self.__actualQueryNr < self.maxQuery:
                self.__actualQuery = self.reduceQuery()
                res = self.nominatim(self.__actualQuery, verbose)
                self.__actualQueryNr += 1

            if res == []:
                self.saveNotFound(self.__originalQuery)
                return (None, None)
            if 'lat' in res[0] and 'lon' in res[0]:
                lat = float(res[0]["lat"])
                lon = float(res[0]["lon"])
                self.saveRecord(self.__originalQuery, lat, lon)
                return (lat, lon)
            else:
                if not self.isNotFound(self.__originalQuery):
                    self.saveNotFound(self.__originalQuery)
                return (None, None)
            

if __name__ == "__main__":
    geo = Geolocator()

    '''query = 'Szombathely'
    print(f'{query}: ', geo.geocode(query))

    query = 'Kőszeg'
    print(f'{query}: ', geo.geocode(query))'''
    query = 'Gulács, nemesgulács'
    print(f'{query}: ', geo.geocode(query))











