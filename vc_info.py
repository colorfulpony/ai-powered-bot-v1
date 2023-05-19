import gspread
from vc_stages import get_vc_stages
from vc_industries import get_vc_industries
from portfolio_websites_info import get_portfolio_websites_info
from db import insert_into_db

try:
    gc = gspread.service_account('Scrap Website Recursively\work\secrets.json')
    spreadsheet = gc.open('VC Template')
    worksheet = spreadsheet.worksheet('Sheet1')
    
    for row in worksheet.get_all_values()[537:1064]:
        vc_name = ""
        vc_website_url = ""
        vc_linkedin_url = ""
        vc_investor_name = ""
        vc_investor_email = ""
        vc_industries = ""
        vc_stages = ""
        portfolio_website_name = ""
        portfolio_website_solution = ""
        portfolio_website_url = ""
        
        # get data from specific cells in the row
        row_number = worksheet.get_all_values().index(row) + 1
        vc_name = worksheet.cell(row_number, 1).value
        vc_website_url = worksheet.cell(row_number, 2).value
        vc_linkedin_url = worksheet.cell(row_number, 3).value
        vc_investor_name = worksheet.cell(row_number, 4).value
        vc_investor_email = worksheet.cell(row_number, 5).value
        vc_stages = worksheet.cell(row_number, 6).value
        vc_industries = worksheet.cell(row_number, 7).value
        
        try:
            if not vc_stages:
                vc_stages = get_vc_stages(vc_website_url)
        
            if not vc_industries:
                vc_industries = get_vc_industries(vc_website_url)
            
            portfolio_websites_data = get_portfolio_websites_info(vc_website_url)
        except Exception as e:
            print(f"Error getting data for {vc_website_url}: {e}")
            continue
        
        try:
            print(vc_name, vc_website_url, vc_linkedin_url, vc_investor_name, vc_investor_email, vc_stages, vc_industries, portfolio_websites_data)
            insert_into_db(vc_name, vc_website_url, vc_linkedin_url, vc_investor_name, vc_investor_email, vc_stages, vc_industries, portfolio_websites_data)
            print("done")
        except Exception as e:
            print(f"Error inserting data for {vc_website_url}: {e}")
            continue

except Exception as e:
    print(f"Error accessing Google Sheets: {e}")
