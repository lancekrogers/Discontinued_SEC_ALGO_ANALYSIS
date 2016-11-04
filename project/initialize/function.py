from edgerdb import helper_functions as hlp
import pandas as pd


def create_csi_data_table(engine):
    '''
    Creates a table with the data from csidata.com
    Takes a sql_alchemy engine.
    Example:
    engine = create_engine('postgresql://analyst:@localhost:5432/test')
    '''
    conn = engine.connect()
    csi_stock_data = pd.read_csv('http://www.csidata.com/factsheets.php?type=stock&format=csv')
    csi_stock_data.columns = map(str.lower, csi_stock_data.columns)
    csi_stock_data = csi_stock_data.rename(columns={'name': 'company_name'})
    csi_stock_data['company_name'] = csi_stock_data['company_name'].str.upper()
    csi_stock_data['company_name'] = csi_stock_data['company_name'].str.strip()
    csi_stock_data = csi_stock_data.fillna(value="NONE")
    csi_stock_data.to_sql('csi_stock_data', engine)
    conn.close()



def create_table_with_cik_and_csi_data():
    '''
        Creates a table called cik_to_csi by joining filings and csi_stock_data tables on company_name
    '''
    join_ticker_to_cik = """select * into temp_cik_to_csi from (select fil.cik, fil.company_name,
                            csi.symbol, csi.exchange,
                            csi.isactive, csi.startdate, csi.enddate
                            from filings fil
                            join csi_stock_data csi on fil.company_name = csi.company_name) as foo;"""
    clean_ticker_to_cik_table = """select * into cik_to_csi
    from (select distinct cik, c.company_name, c.symbol, c.exchange, c.isactive, c.startdate, c.enddate  from temp_cik_to_csi c) as foo;"""
    hlp.clear_sessions('edgar', hlp.db())
    hlp.statement(join_ticker_to_cik, hlp.db(), output=False, commit=True)
    hlp.statement(clean_ticker_to_cik_table, hlp.db(), output=False, commit=True)
    hlp.statement("drop table temp_cik_to_csi;", hlp.db(), output=False, commit=True)
