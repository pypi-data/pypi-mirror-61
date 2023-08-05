__all__ = ('collect_weather_tw', 'QueryFormat')

import csv
import datetime
import pandas as pd
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from enum import Enum
from io import StringIO
from pathlib import Path
import os
import dateutil.relativedelta

DEBUG_MODE = False


class QueryFormat(Enum):
    DAY = 'DAY'
    MONTH = 'MONTH'
    YEAR = 'YEAR'


def get_delta_day(step: int, query_format: QueryFormat):
    return dateutil.relativedelta.relativedelta(days=step) if query_format is QueryFormat.DAY else \
        dateutil.relativedelta.relativedelta(months=step) if query_format is QueryFormat.MONTH else \
        dateutil.relativedelta.relativedelta(years=step)


def generator_begin_to_end(begin: datetime.date, end: datetime.date,
                           query_format: QueryFormat, step=1):
    return range((end - begin).days + step) if query_format is QueryFormat.DAY else \
        range(end.month - begin.month + step) if query_format is QueryFormat.MONTH else \
        range(end.year - begin.year + step)


def get_query_url(url_format: QueryFormat):
    root = "https://e-service.cwb.gov.tw/HistoryDataQuery/"
    query_type = "DayDataController.do?" if url_format is QueryFormat.DAY else \
        "MonthDataController.do?" if url_format is QueryFormat.MONTH else "YearDataController.do?"
    tail = "command=viewMain&station="
    return f'{root}{query_type}{tail}'


def get_weather(date: datetime.date,
                station_id: int, station_name: str,
                query_format: QueryFormat,
                convert2num) -> tuple:
    """
    :return: (dict, list_title, list_title_detail)
    """
    # return variable
    dict_data = {}
    list_title = ""
    list_title_detail = ""

    # 兩次URL編碼
    url_station_name = urllib.parse.quote(urllib.parse.quote(station_name))

    date = date.strftime('%Y-%m-%d') if query_format is query_format.DAY else \
        date.strftime('%Y-%m') if query_format is query_format.MONTH else date.strftime('%Y')
    url = get_query_url(query_format) + str(station_id) + "&stname=" + url_station_name + "&datepicker=" + str(date)
    req = urllib.request.Request(url)
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f.read().decode('utf-8', 'ignore'), "lxml")
    result_set_data = soup.find_all('tr')
    if len(result_set_data) < 5:
        print(f'empty data of {station_name}') if DEBUG_MODE else None
        return dict_data, list_title, list_title_detail

    tag_sub_title = result_set_data[2]
    list_title_detail = [sub_title_col for sub_title_col in tag_sub_title.text.split('\n') if sub_title_col != '']
    del result_set_data[0:3]  # Delete three columns of not necessary data of title
    list_title = [title_col for title_col in result_set_data[0].get_text().split('\n') if title_col != '']
    for n_row, tag_tr in enumerate(result_set_data[1:]):
        data_list = []
        for td in tag_tr.findAll('td'):
            tr_text = td.get_text().rstrip()
            if convert2num:
                if tr_text == "T":
                    data_list.append(0.05)  # 有雨跡，降雨量小於0.01
                elif tr_text in ('X', 'V', '/'):  # 記錄錯誤, 風向不定, 風向不定
                    data_list.append(0)
                else:
                    data_list.append(str(tr_text))
                continue
            data_list.append(str(tr_text))
        if data_list:
            dict_data[n_row + 1] = data_list

    return dict_data, list_title, list_title_detail


def collect_weather_tw(station_csv_path: Path, output_path,
                       end_date: datetime.date, begin_date: datetime.date,
                       query_format,
                       convert2num):
    with open(str(station_csv_path), 'r', encoding='utf-8') as station_csv:
        list_data = [line for line in station_csv if not line.startswith('#')]  # ignore row of starts with '#'
        df = pd.read_csv(StringIO(''.join(list_data)))
        df = pd.DataFrame(df, columns=df.columns[0:2])  # get station_name and ID only

    os.makedirs(output_path.parent, exist_ok=True)
    with open(str(output_path.resolve()), 'w', encoding='utf-8-sig',  # utf8 with BOM
              newline='') as wf:  # newline='' Avoid unnecessary blank lines
        csv_writer = csv.writer(wf, delimiter=",",  # \t
                                lineterminator="\r\n")

        need_write_title = True
        for station_id, station_name in df.values:
            print(f'handling the {station_name} ...')

            headers = ["Date", 'station name']

            for delta in generator_begin_to_end(end_date, begin_date, query_format):
                day = begin_date + get_delta_day(delta, query_format)  # datetime.timedelta(days=delta)
                weather_dict, title_list, title_detail_list = get_weather(day, station_id, station_name,
                                                                          query_format, convert2num)

                if weather_dict == {}:
                    print(f'{day} empty data of {station_name} id:{station_id}')
                    print(f'{day} handle {station_name} failed!')
                    break

                if need_write_title:
                    csv_writer.writerow(headers + title_detail_list)
                    csv_writer.writerow(headers + title_list)
                    need_write_title = False

                row_data = [str(day), station_name]

                for record_id, value_list in weather_dict.items():
                    value_list = [str(_) for _ in value_list]
                    csv_writer.writerow(row_data + value_list)

                print(f'{day} {station_name} ok!')
        print("All Done!")


if __name__ == '__main__':
    STATION_CSV = '../config/CSV/station_test.csv'
    OUTPUT_PATH = Path(f'../temp/year_result.csv')
    BEGIN_DATE = datetime.date(2019, 10, 1)
    END_DATE = datetime.date(2019, 10, 2)
    QUERY_FORMAT = QueryFormat.DAY  # FIXME: If the format is the month, the interval must be the same year.
    CONVERT2NUM = True  # convert to number or not
    collect_weather_tw(Path(STATION_CSV), OUTPUT_PATH,
                       BEGIN_DATE, END_DATE,
                       QUERY_FORMAT,
                       CONVERT2NUM)
    os.startfile(OUTPUT_PATH)
