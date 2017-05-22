'''
Get list of all makes from www.kbb.com homepage
'''

from bs4 import BeautifulSoup
import urllib


def list_all_makes(url):

    try:
        page = urllib.urlopen(url)
    except:
        print('Failed to open url: {}'.format(url))
        return -1

    soup = BeautifulSoup(page, 'lxml')

    '''
    
    <ul class="contentlist by-make">
        <li>
            <a data-omn-page="buynew_${s.prop2}_make_acura" href="/acura/?vehicleclass=newcar&intent=buy-new">Acura</a>
        </li>
        <li>
            <a data-omn-page="buynew_${s.prop2}_make_alfa " href="/alfa-romeo/?vehicleclass=newcar&intent=buy-new">Alfa Romeo</a>
        </li>
        ...
    </ul>
    <ul class="contentlist by-make">
        ...
        ...
    </ul>

    '''
    all_lists = soup.find_all('ul', {'class':'by-make'})
    all_makes = []
    for ll in all_lists:
        for li in ll.contents:
            all_makes.append(li.a['href'].split('/')[1])

    return all_makes