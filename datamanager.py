class DataManager:
    def saveListOfURLsToFile(self, list: list, fileName: str):
        with open(fileName, "w") as file:
            for item in list:
                file.write(item + "\n")
