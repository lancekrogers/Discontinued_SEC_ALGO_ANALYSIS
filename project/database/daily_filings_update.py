from edgerdb import helper_functions as hlp




if __name__ == "__main__":
    daily_files = hlp.generate_daily_file_paths()

    last_date_in_db = int(hlp.latest_index_in_db('filings', hlp.db())[0])

    hlp.load_latest_files(daily_files, last_date=last_date_in_db)
