import pypyodbc as odbc

def insert_into_db(vc_name, vc_website_url, vc_linkedin_url, vc_investor_name, vc_investor_email, vc_stages, vc_industries, portfolio_websites_data):
    DRIVER_NAME = 'SQL SERVER'
    SERVER_NAME = 'DESKTOP-293732M\SQLEXPRESS'
    DATABASE_NAME = 'debonne_vcs'

    # Ensure required variables have values
    if not all([vc_name, vc_website_url, vc_stages, vc_industries, vc_investor_name, vc_investor_email]):
        raise ValueError('One or more required arguments are missing.')

    # uid=<username>;
    # pwd=<password>;
    connection_string = f"""
        DRIVER={{{DRIVER_NAME}}};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        Trust_Connection=yes;
    """ 

    try:
        # Create a connection and cursor
        connection = odbc.connect(connection_string)
        cursor = connection.cursor()

        print("vc_name: " + vc_name + " vc_website_url: " + vc_website_url + " vc_investor_name: " + vc_investor_name + " vc_investor_email: " + vc_investor_email + " vc_linkedin_url: " + vc_linkedin_url + " vc_industries: " + vc_industries + " vc_stages: " + vc_stages)
        # Insert the venture capital information
        cursor.execute('''INSERT INTO venture_capital (name, website_url, linkedin_url, industries, stages, analyst_name, analyst_email)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', (vc_name, vc_website_url, vc_linkedin_url, vc_industries, vc_stages, vc_investor_name, vc_investor_email))
        connection.commit()

        # Get the ID of the inserted venture capital
        cursor.execute("SELECT @@IDENTITY")
        vc_id = cursor.fetchone()[0]

        # Insert the portfolio website information
        portfolio_websites_ids = []
        print("PORTFOLIO WEBSITE DATA: {}".format(portfolio_websites_data))
        if portfolio_websites_data is not None:
            print("PORTFOLIO WEBSITE DATA: {}".format(portfolio_websites_data))
            for portfolio_website in portfolio_websites_data:
                cursor.execute('''INSERT INTO portfolio_website (name, website_url, solution)
                                VALUES (?, ?, ?)''', (portfolio_website[0], portfolio_website[2], portfolio_website[1]))
                connection.commit()

                # Get the ID of the inserted portfolio website
                cursor.execute("SELECT @@IDENTITY")
                portfolio_website_id = cursor.fetchone()[0]
                portfolio_websites_ids.append(portfolio_website_id)

                # Create the many-to-many relationship between VentureCapital and PortfolioWebsite
                cursor.execute('''INSERT INTO vc_pw (venture_capital_id, portfolio_website_id)
                                VALUES (?, ?)''', (vc_id, portfolio_website_id))
                connection.commit()

    except Exception as e:
        # Handle any errors that occur
        print(f'An error occurred while inserting data to the db: {str(e)}')
    finally:
        # Close the connection
        if 'connection' in locals():
            connection.close()
