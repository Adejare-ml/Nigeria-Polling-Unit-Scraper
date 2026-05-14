import pandas as pd
import os
import logging
from .config import COLUMN_MAPPING

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, output_dir="data/processed"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def process_to_csv(self, wards_data, pus_data):
        """Save raw scraped lists to comprehensive CSVs."""
        wards_df = pd.DataFrame(wards_data, columns=['State', 'LGA', 'Ward'])
        pus_df = pd.DataFrame(pus_data, columns=['State', 'LGA', 'Ward', 'Polling Unit'])
        
        lgas_df = wards_df[['State', 'LGA']].drop_duplicates().sort_values(['State', 'LGA'])
        
        lgas_df.to_csv(os.path.join(self.output_dir, 'All_LGAs.csv'), index=False)
        wards_df.to_csv(os.path.join(self.output_dir, 'All_LGA_Wards.csv'), index=False)
        pus_df.to_csv(os.path.join(self.output_dir, 'All_Wards_PUs.csv'), index=False)
        
        logger.info("Saved comprehensive CSV files to processed directory.")
        return pus_df

    def generate_state_reports(self, df):
        """
        Generates a multi-sheet Excel file for each state.
        Handles the hierarchical sorting: State -> LGA -> Ward -> PU.
        """
        states = df['State'].unique()
        
        for state in states:
            state_df = df[df['State'] == state].copy()
            file_path = os.path.join(self.output_dir, f"{state}_Report.xlsx")
            
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Sheet 1: State & LGA combinations
                state_lga = state_df[['State', 'LGA']].drop_duplicates().sort_values(['State', 'LGA'])
                state_lga.to_excel(writer, sheet_name='State_LGA', index=False)
                
                # Sheet 2: LGA & Ward combinations
                lga_wards = state_df[['LGA', 'Ward']].drop_duplicates().sort_values(['LGA', 'Ward'])
                lga_wards.to_excel(writer, sheet_name='LGA_Wards', index=False)
                
                # Sheet 3: Full PU hierarchy
                full_data = state_df[['LGA', 'Ward', 'Polling Unit']].sort_values(['LGA', 'Ward', 'Polling Unit'])
                full_data.to_excel(writer, sheet_name='LGA_Wards_PUs', index=False)
            
            logger.info(f"Generated report for {state}: {file_path}")

def clean_data(df):
    """Standard cleaning: whitespace removal and duplicate dropping."""
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df = df.drop_duplicates()
    return df
