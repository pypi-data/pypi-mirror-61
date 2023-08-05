__all__ = ('collect_weather_tw', 'QueryFormat',)
__author__ = ['Carson', 'Sign.X.er']
__version__ = '4.1.0'


from .src.HistoricalWeatherTW import collect_weather_tw, QueryFormat
from datetime import datetime
from pathlib import Path
import os

from argparse import ArgumentParser, RawTextHelpFormatter
import yaml


def get_historical_weather_tw():
    global g_config
    input_dict = g_config.get('HistoricalWeatherTW')
    path_station_csv = Path(input_dict['STATION_CSV'])
    output_path = Path(input_dict['OUTPUT_PATH'])
    check_list = []
    for pth in (path_station_csv, output_path):
        check_list.append(pth) if pth.is_absolute() else \
            check_list.append(Path(__file__).parent / Path(pth))
    path_station_csv, output_path = check_list
    begin_date = datetime.strptime(input_dict['BEGIN_DATE'], '%Y-%m-%d')
    end_date = datetime.strptime(input_dict['END_DATE'], '%Y-%m-%d')
    query_format = eval(input_dict['QUERY_FORMAT'])
    convert2num = eval(input_dict['CONVERT2NUM'])
    collect_weather_tw(path_station_csv, output_path,
                       begin_date, end_date,
                       query_format,
                       convert2num)
    os.startfile(output_path)


if __name__ == '__main__':
    DESCRIPTION = 'This script is to crawl the information of CWB Observation Data Inquire System'
    script_description = '\n'.join([desc for desc in
                                    ['\n',
                                     f'python module.py [CONFIG.YAML]',
                                     ]])

    arg_parser = ArgumentParser(description=DESCRIPTION,
                                usage=script_description, formatter_class=RawTextHelpFormatter)

    arg_parser.add_argument('-c', '--config', default=Path(__file__).parent / 'config/config.yaml',
                            help="input the path of ``config.yaml``")
    g_args = arg_parser.parse_args()
    with open(Path(g_args.config)) as f:
        g_config = yaml.load(f.read(), Loader=yaml.SafeLoader)
    get_historical_weather_tw()
