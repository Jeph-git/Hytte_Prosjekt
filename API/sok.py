import requests, urllib.parse, json
from time import sleep

def get_address(query):
    formatted_query = urllib.parse.quote(query.lower()) 
    # URL = f'https://ws.geonorge.no/adresser/v1/sok?sok={formatted_query}' 

    URL = f'https://ws.geonorge.no/adresser/v1/sok?adressetekst={formatted_query}'
    print(URL)

    response = requests.get(URL)

    if response.status_code == 200: 
        data = response.json()
        # antall_treff = data['metadata']['totaltAntallTreff']
        antall_treff = len(data['adresser'])
        if antall_treff == 0:
            print('Ingen treff')
        elif antall_treff <= 1:
            # Få adresse informasjon
            adresser = data['adresser'][0]
            adresse = adresser['adressetekst']
            post_nummer = adresser['postnummer']
            post_sted = adresser['poststed']

            # Få posisjons informasjon
            pos = adresser['representasjonspunkt']
            pos_lat,pos_lon= pos['lat'], pos['lon']
    
            print(f'{adresse} {post_nummer}, {post_sted}\nPosisjon: {pos_lat}, {pos_lon}')
            return adresse, post_nummer, post_sted, pos_lat, pos_lon

        # Løkke dersom det er flere adresser med samme navn
        elif antall_treff > 1:
            print(f'Antall resultat: {antall_treff}')

            # Løkke som viser poststedene
            for i in range(antall_treff):
                adresser = data['adresser'][i]
                print(f"{i+1} {adresser['poststed']}")

            velg_riktig_poststed = int(input('Velg riktig poststed: '))


            adresser = data['adresser'][velg_riktig_poststed-1]
            adresse = adresser['adressetekst']
            post_nummer = adresser['postnummer']
            post_sted = adresser['poststed']
            pos = adresser['representasjonspunkt']
            pos_lat,pos_lon= pos['lat'], pos['lon']

            print(f'{adresse} {post_nummer}, {post_sted}\nPosisjon: {pos_lat}, {pos_lon}')
            return adresse, post_nummer, post_sted, pos_lat, pos_lon
        

        else:
            print(f'Fant ingen treff på adressen {query}')


def få_antall_treff(URL):
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        antallTreff = data['metadata']['totaltAntallTreff']
        return antallTreff

def punktsok(func):
    # formatted_query = urllib.parse.quote(query.lower()) 
    # URL = f'https://ws.geonorge.no/adresser/v1/sok?sok={formatted_query}' 

    # URL = f'https://ws.geonorge.no/adresser/v1/punktsok?lat=60.387722439047906&lon=5.967762151782619&radius=1000'
    
    URL = f'https://ws.geonorge.no/adresser/v1/punktsok?lat=60.387722439047906&lon=5.967762151782619&radius=1000&koordsys=4258&utkoordsys=4258&treffPerSide={func}&side=0&asciiKompatibel=true'
    
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
    
        adresser = data['adresser'][0]
        adresse = adresser['adressetekst']
        print(adresse)



# få_antall_treff('https://ws.geonorge.no/adresser/v1/punktsok?lat=60.387722439047906&lon=5.967762151782619&radius=1000&koordsys=4258&utkoordsys=4258&treffPerSide=0&side=0&asciiKompatibel=true')
# punktsok(få_antall_treff('https://ws.geonorge.no/adresser/v1/punktsok?lat=60.387722439047906&lon=5.967762151782619&radius=1000&koordsys=4258&utkoordsys=4258&treffPerSide=0&side=0&asciiKompatibel=true'))


# punktsok(10)

# get_address('Samnangervegen 217')