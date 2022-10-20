import requests
import time
import datetime
import smtplib
import os

# It should run every minute to check the location of International Space Station
while True:
    time.sleep(60)

    # Pulling longitude and latitude values of the ISS from the API
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    values = response.json()
    longitude = float(values['iss_position']['longitude'])
    latitude = float(values['iss_position']['latitude'])

    # Pulling sunrise and sunset times of current location(Melbourne) from another API
    coordinates = {'lat': -37.41509078969461, 'lng': 144.66703774386993, 'formatted': 0}
    response_2 = requests.get(url='https://api.sunrise-sunset.org/json', params=coordinates)
    response_2.raise_for_status()
    data_2 = response_2.json()
    sunrise = (int(data_2['results']['sunrise'].split('T')[1].split(':')[0]) - 14) % 24
    sunset = (int(data_2['results']['sunset'].split('T')[1].split(':')[0]) - 14) % 24
    print(f'Latitude: {latitude}\nLongitude: {longitude}')

    # Current Time
    current_time = datetime.datetime.now()
    current_hour = int(current_time.hour)

    # If the location of ISS in near current address, sends email to given email address
    if -42 < latitude < -32 and 139 < longitude < 149 and (sunrise > current_hour or current_hour > sunset):
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=os.environ['USER'], password=os.environ['PASSWORD'])
            connection.sendmail(from_addr=os.environ['USER'],
                                to_addrs='example@gmail.com',
                                msg='Subject: ISS is Here \n\n Look Up!!'
                                )
            print('Email Sent')




