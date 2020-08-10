import pandas as pd


class PreProcess:
    def __init__(self, data_df=None, config=None):
        self.data_df = data_df
        self.config = config


    def get_potential_messy_business_names(self):
        """
        Standardize dba_name based on lat/long.
        :return: A df with standardized dba_names.
        """
        df = self.data_df.groupby(['latitude', 'longitude']).size().reset_index(name='Num_Businesses')
        business_names_df = df[df['Num_Businesses'] >= 2]
        business_names_df.sort_values(by=['Num_Businesses'], ascending=False, inplace=True)
        business_names_df.to_csv('../processed/potentially_messy_business_names.csv', index=False)

    def get_all_7elevens(self):
        """
        Get all the different representations of 7-eleven business names.
        :return:
        """
        dba_names = self.data_df['dba_name'].values.tolist()
        dba_names = list(set(dba_names))
        print(f'Len of unique dba_names: {len(dba_names)}')
        dba_names = [x.lower() for x in dba_names]
        different_eleven_7_names = [x for x in dba_names if ('eleven' in x) and ('7' in x) and ("#" not in x)]
        print(different_eleven_7_names)


    def seven11_fn(self, x):
        y = x.lower()
        if 'eleven' in y and '7' in y and '#' not in y:
            return '7-Eleven'
        else:
            return x


    def cleanse_7elevens(self):
        """
        Standardize all the 7 eleven names to '7-Eleven'.
        :return: cleansed df.
        """
        self.data_df['dba_name'] = self.data_df['dba_name'].apply(self.seven11_fn)
        return self.data_df











