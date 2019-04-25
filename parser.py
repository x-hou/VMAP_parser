import pandas as pd
import gzip
import struct
import csv


def unpack6(x):
    """
    Function used to unpack 6 byte integer.
    Reference: https://stackoverflow.com/questions/7949912/how-to-unpack-6-bytes-as-single-integer-using-struct-in-python
    :param x: Any packed 6 bytes number
    :return: Integer
    """
    x1, x2 = struct.unpack('<HI', x)
    return x1 | (x2 << 16)


def open_and_extract(file_path, output_filename):
    """
    Function for unpack data from gz file and save information needed into csv file.
    :param file_path: path point to itch 5.0 dataset
    :return: None
    """
    print("Unpacking file...")
    file = open(output_filename, 'w')
    writer = csv.writer(file)

    with gzip.open(file_path, 'rb') as f:
        reader = f.read(1)
        number_of_bytes = 1

        while reader:
            if reader == b'P':
                message = f.read(43)
                stock_locate    = struct.unpack('!H', message[0:2])[0]
                tracking_number = struct.unpack('!H', message[2:4])[0]
                timestamp       = unpack6(message[4:10])
                order_number    = struct.unpack('!Q', message[10:18])[0]
                buy_sell        = struct.unpack('!c', message[18:19])[0]
                shares_integer  = struct.unpack('!I', message[19:23])[0]
                stock_alpha     = struct.unpack('!8s', message[23:31])[0]
                alpha_price     = struct.unpack('!I', message[31:35])[0] / 1e4
                match_number    = struct.unpack('!Q', message[35:])[0]

                if order_number is 0 and buy_sell == b'B':
                    trade_data = [stock_locate, tracking_number, timestamp, order_number, buy_sell.decode(),
                                  shares_integer, stock_alpha.decode().strip(), alpha_price, match_number]
                    writer.writerow(trade_data)

            reader = f.read(1)
            number_of_bytes += 1

            size = number_of_bytes / 1048576
            if size % 100 == 0:
                print('{} MB files processed.'.format(size))
    print("Unpack Finish.")
    file.close()


def parse_vwap(trade_message_path, output_filename):
    """
    Based on data collected, calculate VWAP
    vwap = Cumulative(Volume x Typical Price)/Cumulative(Volume)
    Reference: https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:vwap_intraday
    :param trade_message_path: CSV file contains trade message
           output_filename: name of output csv file
    :return: None
    """
    print("Calculating VWAP...")
    trade_message = pd.read_csv(trade_message_path)
    trade_message.columns = ["stock_locate", "tracking_number", "timestamp", "order_number", "buy_sell",
                             "shares_integer", "stock_alpha", "alpha_price", "match_number"]

    trade_message["hour"] = trade_message["timestamp"] / 3600000000000.0
    trade_message = trade_message.sort_values(by=["stock_alpha", "timestamp"])
    # calculate Volume x Typical Price
    trade_message["V * P"] = trade_message["alpha_price"] * trade_message["shares_integer"]
    # Calculate cumulative sum for V * P
    trade_message["Total_VP"] = trade_message.groupby("stock_alpha")['V * P'].cumsum()
    # Calculate cumulative Volume
    trade_message["Total_volumn"] = trade_message.groupby("stock_alpha")['shares_integer'].cumsum()
    # vwap = Cumulative(Volume x Typical Price)/Cumulative(Volume)
    trade_message["vwap"] = trade_message['Total_VP'] / trade_message['Total_volumn']

    vwap = trade_message.groupby(['stock_alpha']).all()
    vwap = vwap.reset_index()[["stock_alpha"]]

    for hour in [9.5, 10, 11, 12, 13, 14, 15, 16]:
        df = trade_message[trade_message['hour'] <= hour].groupby(['stock_alpha']).tail(1)[["stock_alpha", "vwap"]]
        vwap = pd.merge(vwap, df, on='stock_alpha')

    vwap.columns = ['Stock', '09:30AM', '10:00AM', '11:00AM', '12:00PM', '01:00PM', '02:00PM', '03:00PM', '04:00PM']
    vwap.to_csv(output_filename, index=False)

    print("Done!")


def main():
    input_data = "01302019.NASDAQ_ITCH50.gz"
    trade_message_name = "trade_message.csv"
    vmap_file_name = "vwap_01302019.csv"
    open_and_extract(input_data, trade_message_name)
    parse_vwap(trade_message_name, vmap_file_name)


if __name__ == "__main__":
    main()






