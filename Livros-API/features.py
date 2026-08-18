import pandas as pd
import textwrap 
import numpy as np

class Enginer:
    def __init__(self):
        self.cols = ["volumeInfo.imageLinks.thumbnail",
            "volumeInfo.infoLink",
            "volumeInfo.title", 
            "volumeInfo.authors", 
            "volumeInfo.publisher", 
            "volumeInfo.publishedDate", 
            "volumeInfo.pageCount", 
            "volumeInfo.printType",
            "volumeInfo.description",
            "saleInfo.isEbook",
            "volumeInfo.categories",
            "volumeInfo.subtitle",
            "volumeInfo.language",
            "saleInfo.country",
            "saleInfo.saleability",
        ]
    
    def fix_features(self, df):
        for col in self.cols:
            if col not in df.columns:
                df[col] = np.full([len(df)], fill_value="Não informado")
        df = df.loc[:, self.cols]
        df.columns = df.columns.str.replace("volumeInfo.", "").str.replace("accessInfo.", "").str.replace("saleInfo.", "").str.replace("retailPrice.","").str.strip()
        df = df.loc[:, ~df.columns.duplicated()]
        df[["authors", "categories", "publisher"]] = df[["authors", "categories","publisher"]].astype(str)
        df[["authors", "categories", "publisher"]] = df[["authors", "categories","publisher"]].fillna("Não informado")
        df["isEbook"] = df["isEbook"].astype("int64")
        df["pageCount"] = df["pageCount"].fillna(0)
        df["imageLinks.thumbnail"] = df["imageLinks.thumbnail"].fillna("book.jpg")
        df["pageCount"] = df["pageCount"].clip(lower=0)
        df[["infoLink","title","printType", "description", "language", "country"]] = df[["infoLink","title","printType", "description", "language", "country"]].fillna("Não informado")

        return df
    
    def format_date(self, df):
        df["publishedDate"] = pd.to_datetime(df["publishedDate"], format="mixed")
        month = df["publishedDate"].apply(lambda x : "" if x.month == 1 else x.month_name())
        year = df["publishedDate"].apply(lambda x : "" if x == 1111 else x.year)
        df.insert(1, "year" , year.astype("Int64"))
        df.insert(2, "month" , month)

        return df
    
    def format_text(self, df):
        df["authors"] = df["authors"].apply(lambda x : x.replace("[", "").replace("]", "").replace("'", ""))
        df["categories"] = df["categories"].apply(lambda x : x.replace("[", "").replace("]", "").replace("'", ""))
        df["isFree"] = df["saleability"].apply(lambda x : "Free" if x == "FREE" else "Sale")
        df["saleability"] = df["saleability"].apply(lambda x : 1 if x == "FOR_SALE" else 0)
        df["imageLinks.thumbnail"] = df["imageLinks.thumbnail"].apply(lambda x : x.replace("http://", "https://"))

        return df

    def clean_data(self, df):

        base_clean = pd.json_normalize(df)

        base_clean = self.fix_features(base_clean)
        base_clean = self.format_date(base_clean)
        base_clean = self.format_text(base_clean)

        return base_clean

    
    