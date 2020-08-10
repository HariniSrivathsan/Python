import pandas as pd


def to_sec(x):
    ftr = [3600, 60, 1]
    seconds = sum([a * b for a, b in zip(ftr, map(int, x.split(':')))])
    return seconds


def calculate_total_cost(row):
    """
    < 300 sec, 3 cents/sec
    >= 300 sec, 30 cents /sec
    longest call is free
    :param df:
    :return: df with total cost for each phone number
    """
    seconds = row['seconds']
    cost = 0.0
    if seconds < 300:
        cost = seconds * 0.03

    if seconds >= 300:
        cost = seconds * 0.30

    return cost/100



def promotion_fn(row, max_secs):
    cost = row['cost']
    if row['seconds'] == max_secs:
        cost = 0.0
    return cost


def main():
    record = []
    with open("../input/test.txt", "r", encoding='utf-8-sig') as fp:
        all_lines = fp.readlines()
        for line in all_lines:
            line = line.strip()
            splits = line.split(',')
            ts = splits[0]
            phone = splits[1]
            record.append((ts, phone))

    call_df = pd.DataFrame(record)
    #print(record)
    call_df.columns = ['ts', 'phone_number']
    print(call_df)
    # convert timestamp to seconds
    call_df['seconds'] = call_df['ts'].apply(lambda x: to_sec(x))
    print(call_df)

    # groupby phone number and sum
    seconds_df = call_df.groupby('phone_number')['seconds'].sum().reset_index(name='seconds')
    print(seconds_df)
    seconds_df['cost'] = seconds_df.apply(calculate_total_cost, axis=1)
    print(seconds_df)

    # look for all the highest time-duration phone-numbers and assign cost to zero.
    max_seconds = max(seconds_df['seconds'].values.tolist())
    print(max_seconds)

    # apply zero cost
    secondcd ..s_df['cost'] = seconds_df.apply(promotion_fn, args=(max_seconds, ), axis=1)

    print(seconds_df)

if __name__ == '__main__':
    main()