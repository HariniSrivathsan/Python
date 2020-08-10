import sweetviz as sv
from pandas_profiling import ProfileReport
import pandas as pd

class EDA:
    def __init__(self, data_df=None, config=None, filename=None):
        self.data_df = data_df
        self.config = config
        self.name = filename

    def analyze(self):
        report = sv.analyze(self.data_df)
        report_name = self.name + '_eda.html'
        report.show_html(report_name)

    def gen_profile_report(self, name):
        report = ProfileReport(self.data_df)
        report_file = '../eda/' + name + '_profile.html'
        report.to_file(output_file=report_file)

    def find_total_nulls_in_columns(self, name):
        null_columns = self.data_df.columns[self.data_df.isnull().any()]
        print("\nNull Columns: ")
        df = self.data_df[null_columns].isnull().sum()
        df.to_csv('../eda/' + name + '_total_nulls.csv', index=True)

    def missing_data(self, name):
        total = self.data_df.isnull().sum().sort_values(ascending=False)
        percent = (self.data_df.isnull().sum()/self.data_df.isnull().count()).sort_values(ascending=False)
        missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
        missing_data['Percent'] = missing_data['Percent'].apply(lambda x: round(x, 4))
        if len(missing_data.index) > 0:
            missing_data.reset_index(inplace=True)
            missing_data_file = '../eda/' + name + '_missing_data.csv'
            missing_data.to_csv(missing_data_file, index=False)