import pymysql
import cred
from datetime import date
from decimal import Decimal

## Utilities for contracts

def calculate_aav(contractDetails):
    """Calculate the AAV of a given contract

    Keyword arguments:
    contractDetails -- A contract passed in... This is a tuple of tuples.
    ((ContractID, DetailID, PlayerId, Season, BaseSalary, SigningBonus, CurrentAAV, Slid, Age, SigningDate, ContractYear),
     (.....))
    """
    CONTRACT_ID = 0
    DETAIL_ID = 1
    PLAYER_ID = 2
    SEASON = 3
    BASE_SALARY = 4
    SIGNING_BONUS = 5
    CURRENT_AAV = 6
    SLID = 7
    BIRTHDAY = 8
    SIGNING_DATE = 9
    CONTRACT_YEAR = 10


    # 0. Determine any base information about the contract.
    # 0a. Did any years slide?
    # 0b. What is the length of the contract?
    # 0c. Does the Kovalchuk rule apply? Over 40, Signing Date >= '2010-09-04, Length over 5 years
    contractLength = 0
    hasSlide = False
    isKovalchuk = False
    isNormal = False
    for contractYear in contractDetails:
        contractLength += 1
        if contractYear[SLID] == 1:
            hasSlide = True
        signingDate = contractYear[SIGNING_DATE]
        if signingDate == None:
            signingDate = date(2010, 9, 4)
        if calc_age_june30(contractYear[SEASON], contractYear[BIRTHDAY]) > 40 and signingDate >= date(2010, 9, 4) and contractLength >= 5:
            isKovalchuk = True

    if not hasSlide and not isKovalchuk:
        isNormal = True

    #1. Create dictionary for cap information
    # DICTIONARY[DETAIL_ID] = [New_AAV, Current_AAV] --> Initialize new AAV as 0
    aav_dict = {}
    for contractYear in contractDetails:
        aav_dict[contractYear[DETAIL_ID]] = [0, contractYear[CURRENT_AAV]]

    #2. Run the Kovalchuk rule.
    # At this point, this should only be Chara
    if isKovalchuk:
        # Look at contract years where player <= 40 in isolation.
        running_total = 0
        year_count = 0
        for contractYear in contractDetails:
            if calc_age_june30(contractYear[SEASON], contractYear[BIRTHDAY]) <= 40:
                running_total += contractYear[BASE_SALARY] + contractYear[SIGNING_BONUS]
                year_count += 1
            # If not under 40, the AAV is just the salary + signing bonus
            else:
                aav_dict[contractYear[DETAIL_ID]][0] = contractYear[BASE_SALARY] + contractYear[SIGNING_BONUS]
        under41_aav = float(running_total)/year_count
        # Now that we have the AAV, loop back through and set it for the relevant years.
        for contractYear in contractDetails:
            if calc_age_june30(contractYear[SEASON], contractYear[BIRTHDAY]) <= 40:
                aav_dict[contractYear[DETAIL_ID]][0] = under41_aav

    # 1. Do calculation for contracts that slid.
    # We will assume that any contract that slid is a 3-year deal and the contract can slide a max of 2 times.
    if hasSlide:
        ## Calculate AAV for years 1-3
        tot_comp_y123 = 0
        for contractYear in contractDetails[0:3]:
            tot_comp_y123 += contractYear[BASE_SALARY] + contractYear[SIGNING_BONUS]
        aav_y123 = float(tot_comp_y123) / 3

        ## Calculate AAV for years 2-4
        tot_comp_y234 = 0
        for contractYear in contractDetails[1:4]:
            tot_comp_y234  += contractYear[BASE_SALARY] + contractYear[SIGNING_BONUS]
        aav_y234 = float(tot_comp_y234) / 3

        ## If the contract slid twice
        if contractLength > 4:
            tot_comp_y345 = 0
            for contractYear in contractDetails[2:5]:
                tot_comp_y345 += contractYear[BASE_SALARY] + contractYear[SIGNING_BONUS]
            aav_y345 = float(tot_comp_y345) / 3

            ## Set the AAVs
            for contractYear in contractDetails:
                if contractYear[CONTRACT_YEAR] == 1:
                    aav_dict[contractYear[DETAIL_ID]][0] = aav_y123
                elif contractYear[CONTRACT_YEAR] == 2:
                    aav_dict[contractYear[DETAIL_ID]][0] = aav_y234
                else:
                    aav_dict[contractYear[DETAIL_ID]][0] = aav_y345

        # Else, the contract slid once.
        else:
            ## Set the AAVs
            for contractYear in contractDetails:
                if contractYear[CONTRACT_YEAR] == 1:
                    aav_dict[contractYear[DETAIL_ID]][0] = aav_y123
                else:
                    aav_dict[contractYear[DETAIL_ID]][0] = aav_y234

    ## If neither of these special cases, calculate as normal.
    if isNormal:
        running_total = 0
        year_count = 0
        for contractYear in contractDetails:
            running_total += contractYear[BASE_SALARY] + contractYear[SIGNING_BONUS]
            year_count += 1
        aav = float(running_total) / year_count
        for contractYear in contractDetails:
            aav_dict[contractYear[DETAIL_ID]][0] = aav

    # If the AAVs are different, delete from dictionary
    to_update_dict = {}
    for detailId in aav_dict:
        if Decimal(aav_dict[detailId][0]) != aav_dict[detailId][1]:
            to_update_dict[detailId] = Decimal(aav_dict[detailId][0])

    return to_update_dict

def update_contract_details(db, to_update):
    """Update contract detail records with AAV

    Keyword arguments:
    db - Database connection to update from
    to_update - a dictionary of the form {DetailID: NewAAV, ...} which contains detail IDs to be updated.
    """
    #print to_update
    cursor = db.cursor()
    update_query = "UPDATE ContractDetail SET AAV = %s WHERE DetailID = %s"
    for detail in to_update:
        cursor.execute(update_query, (to_update[detail], detail))
    cursor.close()

def calc_age_june30(seasonEnding, birthday):
    """Calculate age of a player on June 30 preceding the season.

    Keyword arguments:
    seasonEnding - The year the season ends. For the 2014-2015 season, this would be 2015.
    The date we calculate the age of for the "2015" season is 2014-06-30
    birthday - Birthday of the player
    """
    if birthday != None:
        if birthday.month > 6:
            age = (seasonEnding - 1) - birthday.year - 1
        else:
            age = (seasonEnding - 1) - birthday.year
    else:
        10
    return age


def close_db(db):
    db.close()
    return

def open_db():
    db = pymysql.connect(host=cred.mysql_server, user = cred.mysql_username,
                    passwd = cred.mysql_password, db=cred.mysql_dbname)
    return db

def grab_contract(db, playerId):
    cursor = db.cursor()
    sql_query = '''SELECT ContractId, DetailId, PlayerId, Season, BaseSalary, SigningBonus, AAV, Slid, Birthday, SigningDate, ContractYear
        FROM Contracts WHERE PlayerID = %s
        ORDER BY ContractId, ContractYear'''
    cursor.execute(sql_query, playerId)
    result = cursor.fetchall()
    cursor.close()
    return result

def calc_aav_all(db):
    cursor = db.cursor()
    sql_query = '''SELECT ContractId, DetailId, PlayerId, Season, BaseSalary, SigningBonus, AAV, Slid, Birthday, SigningDate, ContractYear
        FROM Contracts
        ORDER BY ContractId, ContractYear'''
    cursor.execute(sql_query)
    result = cursor.fetchall()
    cursor.close()
    contractHeader = []
    lastContract = result[0][0]
    for contractDetail in result:
        if lastContract == contractDetail[0]:
            contractHeader.append(contractDetail)
        else:
            to_update = calculate_aav(contractHeader)
            if len(to_update) > 0:
                update_contract_details(db, to_update)
            lastContract = contractDetail[0]
            contractHeader = []
            contractHeader.append(contractDetail)

db = open_db()
#contract = grab_contract(db, "reinhsa95")
# to_update = calculate_aav(contract)
# update_contract_details(db, to_update)
calc_aav_all(db)
db.commit()
close_db(db)