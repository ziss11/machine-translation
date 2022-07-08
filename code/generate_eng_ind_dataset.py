import csv
import re


class GenerateDataset:
    def __init__(self, filenames, columns):
        self._listSentences = list()
        self._filenames = filenames
        self._columns = columns
        self._getData()

    def _getData(self):
        filenames1 = f"datasets/translation/untidy/{self._filenames[0]}.txt"
        filenames2 = f"datasets/translation/untidy/{self._filenames[1]}.txt"

        languange1ListTexts = list()
        languange2ListTexts = list()

        with open(filenames1) as f:
            for lines in f.readlines():
                languange1ListTexts.append(lines.strip())

        with open(filenames2) as f:
            for lines in f.readlines():
                languange2ListTexts.append(lines.strip())

        for lang1Text, lang2Text in zip(languange1ListTexts, languange2ListTexts):
            dicti = dict()

            dicti[columns[0]] = lang1Text
            dicti[columns[1]] = lang2Text

            self._listSentences.append(dicti)

    def convertToCSV(self, filename):
        fileDir = f"datasets/translation/result/{filename}.csv"

        try:
            with open(fileDir, "a", encoding='utf8', newline="") as file:
                writer = csv.DictWriter(file, self._columns)
                writer.writeheader()
                for data in self._listSentences:
                    writer.writerow(data)
                print(f"File {filename} berhasil dibuat")
        except IOError:
            print(f"File {filename} gagal dibuat")


if __name__ == "__main__":
    txtFileName = ["PANL-BPPT-ECO-EN-150Kw.tok",
                   "PANL-BPPT-ECO-ID-150Kw.tok"]
    savedFileName = "eng-ind"
    columns = ["English", "Indonesia"]

    generator = GenerateDataset(txtFileName, columns)
    generator.convertToCSV(savedFileName)
