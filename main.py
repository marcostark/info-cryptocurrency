import urllib.request as urllib
import requests
import argparse
import json
import re

def cotation_cryto(moeda):

    ticker_url = "https://api.coinmarketcap.com/v1/ticker/"
    ticker_limit_url = "https://api.coinmarketcap.com/v1/ticker/?limit="

    if moeda.isdigit():
        request = requests.get(ticker_limit_url + moeda)
        data = request.json()
        show(data)
    
    else:
        ticker_url += '/'+moeda+'/'
        request = requests.get(ticker_url)
        data = request.json()
        show(data)

def get_parser():
    """Obter os argumentos via linha de comando."""
    parser = argparse.ArgumentParser(description="Informações sobre Criptomoedas")
    parser.add_argument("-c",
                        "--coin",
                        required = True,
                        dest="moeda",
                        help="Insira o nome da moeda que deseja consultar as informações")
    return parser

def show(data):
    for coin in data:
        name = coin['name']
        rank = coin['rank']
        symbol = coin['symbol']
        price = float(coin['price_usd'])

        print("Rank:\t\t\t" + rank)
        print("Nome:\t\t\t" + name)
        print("Simbolo:\t\t" + symbol)
        print("Valor USD:\t\t$ " + format(price))
        print("Valor BRL:\t\tR$ {:.2f}".format(convert_to_real(price)))
        print()

def convert_to_real(valor, regex='^.*nacional" value="([0-9,]+)"'):
    dolar_hoje = 'http://dolarhoje.com/'
    pagina = urllib.urlopen(dolar_hoje)
    s = pagina.read().decode('utf-8')

    m = re.match(regex, s, re.DOTALL)
    if m:
        dolar = float(m.group(1).replace(',', '.')) 
        return (dolar * valor)
    else:
        return 0

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    
    cotation_cryto(args.moeda)
    
    